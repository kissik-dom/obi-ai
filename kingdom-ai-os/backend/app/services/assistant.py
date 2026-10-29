"""Live model catalog, per-workspace assistants, and the OpenRouter chat router."""
from __future__ import annotations

import base64
import io
import json
import os
import time
from pathlib import Path
from typing import Any

import httpx

OPENROUTER_BASE = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
SNAPSHOT = next((p / "registries" / "model_catalog_snapshot.json" for p in Path(__file__).resolve().parents if (p / "registries").is_dir()), Path("registries/model_catalog_snapshot.json"))
# Tried in order when the chosen model fails; all exist in the live OpenRouter catalog.
DEFAULT_MODEL = os.getenv("KAIOS_DEFAULT_MODEL", "google/gemini-2.5-flash")
FALLBACK_MODELS = [m.strip() for m in os.getenv("KAIOS_FALLBACK_MODELS", "openai/gpt-4o-mini,deepseek/deepseek-v4.1-flash").split(",") if m.strip()]
WEB_SEARCH_TABS = {"research", "legal", "osint", "finance", "investments", "real-estate", "news-magazines", "leads", "city-urban-planning", "web-scraping"}

BASE_RULES = (
    "You are Obi, the assistant inside Kingdom AI OS. Be warm, clear and practical. "
    "Use short headings and bullet points when they help. Never invent facts, sources, numbers or quotes; "
    "if you are unsure, say so. When web results are provided, cite them inline like [1], [2]. "
    "Refuse to help with impersonation, fake accounts, harassment, surveillance of private people, or stealing credentials."
)
TAB_FOCUS: dict[str, str] = {
    "home": "You are the command center: help the user plan, decide which workspace fits, and get things done.",
    "models": "You help the user choose and compare AI models by cost, context length, speed and quality.",
    "research": "You are a careful research analyst. Give source-backed answers with citations and separate facts from interpretation.",
    "legal": "You explain legal topics in plain language with sources. You are not a lawyer; say when a licensed attorney is needed.",
    "osint": "You do ethical open-source research on companies, public records and public topics only. Do not profile private individuals.",
    "finance": "You are a finance analyst: budgets, cash flow, statements, models. Show your math. Not financial advice.",
    "investments": "You research investments with sources, risks and scenarios. Not financial advice; flag uncertainty.",
    "real-estate": "You analyze real estate deals, markets, comps and cash flow with clear assumptions.",
    "business-crm": "You help run the business: customers, pipelines, offers, SOPs and follow-ups.",
    "leads": "You help find and qualify business leads from public, legitimate sources and write respectful outreach.",
    "city-urban-planning": "You help with city and urban planning research: zoning, infrastructure, permits and community impact.",
    "engineering-ghidra": "You are an engineering assistant: systems design, physics, hardware and authorized reverse engineering.",
    "coding-dev": "You are a senior software engineer. Give working, tested code and explain how to run it.",
    "web-scraping": "You help plan lawful web data collection that respects robots.txt and site terms, and summarize public pages.",
    "news-magazines": "You summarize current news with sources and help write articles and magazine features.",
    "social-marketing": "You help plan authentic social media content, captions, calendars and campaigns for the user's real accounts.",
    "fashion": "You are a fashion creative director: trends, lookbooks, collections, styling and product descriptions.",
    "images-visual-ai": "You help plan visual projects and write strong image-generation prompts.",
    "video-ugc": "You help write scripts, shot lists and storyboards for video, UGC, TV and film.",
    "music-audio": "You help with songwriting, arrangement, mixing notes and audio production.",
    "agents-communications": "You help design AI agents, workflows, emails and messages.",
    "tasks": "You turn goals into clear task lists with owners, priorities and due dates.",
    "open-source-apps": "You help find, compare and evaluate open-source tools: license, activity, install steps and fit.",
    "security-admin": "You are a defensive security advisor: hardening, access control, backups and incident response.",
}

_catalog_cache: dict[str, Any] = {"at": 0.0, "models": [], "source": ""}


def api_key() -> str:
    return os.getenv("OPENROUTER_API_KEY", "").strip()


def _normalize(m: dict[str, Any]) -> dict[str, Any]:
    if "architecture" in m:  # live OpenRouter shape
        arch = m.get("architecture") or {}
        pricing = m.get("pricing") or {}
        def per_m(v: Any) -> float | None:
            try:
                return round(float(v) * 1_000_000, 4)
            except (TypeError, ValueError):
                return None
        return {"id": m["id"], "name": m.get("name") or m["id"], "context": m.get("context_length"),
                "input_modalities": arch.get("input_modalities") or ["text"],
                "price_in": per_m(pricing.get("prompt")), "price_out": per_m(pricing.get("completion"))}
    return {"id": m.get("providerModelId") or m.get("id"), "name": m.get("canonicalName") or m.get("id"),
            "context": m.get("contextTokens"), "input_modalities": m.get("modalities") or ["text"],
            "price_in": m.get("costPer1MInput"), "price_out": m.get("costPer1MOutput")}


async def catalog(force: bool = False) -> dict[str, Any]:
    if not force and _catalog_cache["models"] and time.time() - _catalog_cache["at"] < 3600:
        return _catalog_cache
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(OPENROUTER_BASE + "/models")
        r.raise_for_status()
        rows = [_normalize(m) for m in r.json().get("data", []) if isinstance(m, dict) and m.get("id")]
        source = "openrouter_live"
    except (httpx.HTTPError, ValueError):
        rows = [_normalize(m) for m in json.loads(SNAPSHOT.read_text("utf-8"))] if SNAPSHOT.exists() else []
        source = "bundled_snapshot"
    rows = [r for r in rows if not r["id"].endswith(":batch")]
    for r in rows:
        r["free"] = r["id"].endswith(":free") or (r["price_in"] == 0 and r["price_out"] == 0)
        r["vision"] = "image" in (r["input_modalities"] or [])
    rows.sort(key=lambda r: r["name"].casefold())
    _catalog_cache.update(at=time.time(), models=rows, source=source)
    return _catalog_cache


def system_prompt(tab_id: str, tab_name: str) -> str:
    focus = TAB_FOCUS.get(tab_id, f"You are the assistant for the '{tab_name}' workspace.")
    return f"{BASE_RULES}\n\nWorkspace: {tab_name}. {focus}"


def extract_text(name: str, data_b64: str) -> str:
    raw = base64.b64decode(data_b64, validate=False)
    lower = name.casefold()
    if lower.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        return "\n\n".join((p.extract_text() or "") for p in reader.pages[:300])
    if lower.endswith(".docx"):
        from docx import Document
        return "\n".join(p.text for p in Document(io.BytesIO(raw)).paragraphs)
    return raw.decode("utf-8", errors="replace")


class ProviderError(RuntimeError):
    pass


async def _call(model_id: str, messages: list[dict[str, Any]], web: bool, max_tokens: int) -> dict[str, Any]:
    payload: dict[str, Any] = {"model": model_id, "messages": messages, "max_tokens": max_tokens}
    if web:
        payload["plugins"] = [{"id": "web", "max_results": 5}]
    headers = {"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json",
               "HTTP-Referer": os.getenv("KAIOS_PUBLIC_URL", "https://kingdom-ai-os.local"), "X-Title": "Kingdom AI OS"}
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post(OPENROUTER_BASE + "/chat/completions", headers=headers, json=payload)
    if r.status_code != 200:
        try:
            msg = (r.json().get("error") or {}).get("message", "")
        except ValueError:
            msg = ""
        raise ProviderError(f"{model_id}: HTTP {r.status_code} {msg}"[:300])
    data = r.json()
    choice = (data.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    content = message.get("content") or ""
    if not content.strip():
        raise ProviderError(f"{model_id}: empty response")
    citations = []
    for a in message.get("annotations") or []:
        uc = a.get("url_citation") if isinstance(a, dict) else None
        if uc and uc.get("url") and uc["url"] not in [c["url"] for c in citations]:
            citations.append({"url": uc["url"], "title": uc.get("title") or uc["url"]})
    return {"content": content, "model_id": data.get("model") or model_id, "citations": citations, "usage": data.get("usage") or {}}


async def answer(model_id: str | None, messages: list[dict[str, Any]], web: bool, max_tokens: int = 4000) -> dict[str, Any]:
    """Try the chosen model, then fall back through the default chain."""
    if not api_key():
        raise ProviderError("OPENROUTER_API_KEY is not configured on the server")
    chain = [m for m in [model_id or DEFAULT_MODEL, DEFAULT_MODEL, *FALLBACK_MODELS] if m]
    seen: list[str] = []
    errors: list[str] = []
    for m in chain:
        if m in seen:
            continue
        seen.append(m)
        try:
            result = await _call(m, messages, web, max_tokens)
            result["requested_model"] = model_id or DEFAULT_MODEL
            result["fell_back"] = m != (model_id or DEFAULT_MODEL)
            result["errors"] = errors
            return result
        except (ProviderError, httpx.HTTPError) as exc:
            errors.append(str(exc)[:300])
    raise ProviderError("All models failed: " + " | ".join(errors))
