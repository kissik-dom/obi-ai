"""Working chat API: conversations per workspace tab, live models, attachments."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services import assistant, store
from app.services.model_probe import probe_model

API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
router = APIRouter(prefix=API_PREFIX)
_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "registries").is_dir()), Path("."))


def _tabs() -> dict[str, str]:
    path = _ROOT / "registries" / "tabs.json"
    rows = json.loads(path.read_text("utf-8")) if path.exists() else []
    return {r["id"]: r["name"] for r in rows}


@router.get("/status")
async def status() -> dict[str, Any]:
    cat = await assistant.catalog()
    return {
        "chat_ready": bool(assistant.api_key()),
        "provider": "openrouter",
        "provider_configured": bool(assistant.api_key()),
        "database": store.health(),
        "default_model": assistant.DEFAULT_MODEL,
        "fallback_models": assistant.FALLBACK_MODELS,
        "catalog_source": cat["source"],
        "catalog_count": len(cat["models"]),
    }


@router.get("/catalog/models")
async def catalog_models(q: str | None = Query(default=None, max_length=200), free: bool = False, vision: bool = False,
                         limit: int = Query(default=60, ge=1, le=600)) -> dict[str, Any]:
    cat = await assistant.catalog()
    checks = store.model_checks()
    rows = cat["models"]
    if q:
        n = q.casefold()
        rows = [r for r in rows if n in r["id"].casefold() or n in r["name"].casefold()]
    if free:
        rows = [r for r in rows if r["free"]]
    if vision:
        rows = [r for r in rows if r["vision"]]
    items = [{**r, "check": (checks.get(r["id"]) or {}).get("status", "not_run")} for r in rows[:limit]]
    return {"source": cat["source"], "total": len(rows), "items": items, "default_model": assistant.DEFAULT_MODEL}


class NewConversation(BaseModel):
    tab_id: str = Field(min_length=1, max_length=80)
    title: str = Field(default="New chat", max_length=200)


@router.get("/conversations")
async def conversations(tab_id: str | None = Query(default=None, max_length=80)) -> list[dict[str, Any]]:
    return store.list_conversations(tab_id)


@router.post("/conversations")
async def new_conversation(payload: NewConversation) -> dict[str, Any]:
    if payload.tab_id not in _tabs():
        raise HTTPException(404, "Unknown workspace tab")
    return store.create_conversation(payload.tab_id, payload.title)


@router.get("/conversations/{cid}")
async def conversation(cid: str) -> dict[str, Any]:
    conv = store.get_conversation(cid)
    if conv is None:
        raise HTTPException(404, "Conversation not found")
    return conv


@router.delete("/conversations/{cid}")
async def remove_conversation(cid: str) -> dict[str, bool]:
    if not store.delete_conversation(cid):
        raise HTTPException(404, "Conversation not found")
    return {"deleted": True}


class Attachment(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    text: str = Field(max_length=400_000)


class SendMessage(BaseModel):
    content: str = Field(min_length=1, max_length=40_000)
    model_id: str | None = Field(default=None, max_length=200)
    web_search: bool | None = None
    attachments: list[Attachment] = Field(default_factory=list, max_length=10)


@router.post("/conversations/{cid}/messages")
async def send_message(cid: str, payload: SendMessage) -> dict[str, Any]:
    conv = store.get_conversation(cid)
    if conv is None:
        raise HTTPException(404, "Conversation not found")
    if not assistant.api_key():
        raise HTTPException(503, "Chat is not switched on yet: the server needs an OPENROUTER_API_KEY.")
    tabs = _tabs()
    web = payload.web_search if payload.web_search is not None else conv["tab_id"] in assistant.WEB_SEARCH_TABS
    history: list[dict[str, Any]] = [{"role": "system", "content": assistant.system_prompt(conv["tab_id"], tabs.get(conv["tab_id"], conv["tab_id"]))}]
    for m in conv["messages"][-20:]:
        history.append({"role": m["role"], "content": m["content"]})
    user_text = payload.content
    if payload.attachments:
        files = "\n\n".join(f"--- File: {a.name} ---\n{a.text[:120_000]}" for a in payload.attachments)
        user_text = f"{payload.content}\n\nAttached files:\n{files}"
    history.append({"role": "user", "content": user_text})
    user_msg = store.add_message(cid, "user", payload.content, attachments=[a.name for a in payload.attachments])
    if not conv["messages"]:
        store_title = payload.content.strip().splitlines()[0][:80]
        with store._LOCK, store._connect() as c:  # first message names the chat
            c.execute("UPDATE conversations SET title=? WHERE id=?", (store_title, cid))
    try:
        result = await assistant.answer(payload.model_id, history, web)
    except assistant.ProviderError as exc:
        raise HTTPException(502, f"The AI provider did not answer. {exc}") from exc
    store.record_model_check(result["model_id"], "passed", {"via": "chat"})
    reply = store.add_message(cid, "assistant", result["content"], model_id=result["model_id"],
                              citations=result["citations"], usage=result["usage"])
    return {"user": user_msg, "assistant": reply, "fell_back": result["fell_back"], "web_search": web}


class ExtractRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    data_b64: str = Field(min_length=1, max_length=30_000_000)


@router.post("/files/extract")
async def extract(payload: ExtractRequest) -> dict[str, Any]:
    allowed = (".pdf", ".docx", ".txt", ".md", ".csv", ".json", ".html", ".py", ".ts", ".tsx", ".js")
    if not payload.name.casefold().endswith(allowed):
        raise HTTPException(415, "Supported files: PDF, DOCX, TXT, MD, CSV, JSON, HTML and code files")
    try:
        text = assistant.extract_text(payload.name, payload.data_b64)
    except Exception as exc:  # noqa: BLE001 - parser errors vary by format
        raise HTTPException(422, "Could not read that file") from exc
    return {"name": payload.name, "chars": len(text), "text": text[:400_000]}


class CheckRequest(BaseModel):
    model_id: str = Field(min_length=1, max_length=200)


@router.post("/catalog/check")
async def check_model(payload: CheckRequest) -> dict[str, Any]:
    """Send one tiny test prompt to a model and remember whether it answered."""
    result = await probe_model("openrouter", payload.model_id)
    if result.get("status") in ("passed", "failed"):
        store.record_model_check(payload.model_id, result["status"], result)
    return result
