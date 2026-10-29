"""Free model catalog (self-hosted Ollama + free OpenRouter models), per-workspace assistants, chat router."""
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
# Self-hosted open-source models (Ollama on the same server). No key needed.
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "").rstrip("/")
OLLAMA_DEFAULT = os.getenv("OLLAMA_DEFAULT_MODEL", "qwen2.5:3b")
# Free-only mode (default ON): paid models are hidden and blocked.
FREE_ONLY = os.getenv("KAIOS_FREE_ONLY", "true").strip().lower() not in ("0", "false", "no", "off")
SNAPSHOT = next((p / "registries" / "model_catalog_snapshot.json" for p in Path(__file__).resolve().parents if (p / "registries").is_dir()), Path("registries/model_catalog_snapshot.json"))
# Free OpenRouter models (need only a free OpenRouter account key, no credit card).
_OR_FREE_DEFAULT = "openrouter/free"
_OR_FREE_FALLBACKS = "google/gemma-4-31b-it:free,nvidia/nemotron-3.5-super-vl:free"
_ENV_DEFAULT = os.getenv("KAIOS_DEFAULT_MODEL", "").strip()
_ENV_FALLBACKS = [m.strip() for m in os.getenv("KAIOS_FALLBACK_MODELS", _OR_FREE_FALLBACKS).split(",") if m.strip()]
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


def ollama_base() -> str:
    return os.getenv("OLLAMA_BASE_URL", OLLAMA_BASE).rstrip("/")


def chat_ready() -> bool:
    return bool(api_key() or ollama_base())


def default_model() -> str:
    if _ENV_DEFAULT:
        return _ENV_DEFAULT
    if ollama_base():
        return "ollama/" + os.getenv("OLLAMA_DEFAULT_MODEL", OLLAMA_DEFAULT)
    return _OR_FREE_DEFAULT


def fallback_models() -> list[str]:
    chain: list[str] = []
    if ollama_base():
        chain.append("ollama/" + os.getenv("OLLAMA_DEFAULT_MODEL", OLLAMA_DEFAULT))
    if api_key():
        chain += [_OR_FREE_DEFAULT, *_ENV_FALLBACKS]
    return [m for m in chain if m != default_model()]


def is_free(model_id: str) -> bool:
    if model_id.startswith("ollama/") or model_id.endswith(":free") or model_id == _OR_FREE_DEFAULT:
        return True
    hit = next((r for r in _catalog_cache["models"] if r["id"] == model_id), None)
    return bool(hit and hit["free"])


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
                "output_modalities": arch.get("output_modalities") or ["text"], "provider": "openrouter",
                "price_in": per_m(pricing.get("prompt")), "price_out": per_m(pricing.get("completion"))}
    return {"id": m.get("providerModelId") or m.get("id"), "name": m.get("canonicalName") or m.get("id"),
            "context": m.get("contextTokens"), "input_modalities": m.get("modalities") or ["text"], "provider": "openrouter",
            "price_in": m.get("costPer1MInput"), "price_out": m.get("costPer1MOutput")}


async def _ollama_models() -> list[dict[str, Any]]:
    base = ollama_base()
    if not base:
        return []
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            r = await client.get(base + "/v1/models")
        r.raise_for_status()
        ids = [m["id"] for m in r.json().get("data", []) if isinstance(m, dict) and m.get("id")]
    except (httpx.HTTPError, ValueError, KeyError):
        return []
    return [{"id": "ollama/" + i, "name": f"{i} (on your server)", "context": None, "input_modalities": ["text"],
             "output_modalities": ["text"], "provider": "ollama", "price_in": 0.0, "price_out": 0.0} for i in ids]


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
    rows = [r for r in rows if not r["id"].endswith(":batch") and "text" in (r.get("output_modalities") or ["text"])]
    local = await _ollama_models()
    rows = local + rows
    for r in rows:
        r["free"] = r["provider"] == "ollama" or r["id"].endswith(":free") or (r["price_in"] == 0 and r["price_out"] == 0)
        r["vision"] = "image" in (r["input_modalities"] or [])
    if FREE_ONLY:
        rows = [r for r in rows if r["free"]]
    rows.sort(key=lambda r: (r["provider"] != "ollama", r["name"].casefold()))
    # If the local model server is still starting, re-check in 5 minutes instead of 1 hour.
    fetched_at = time.time() if local or not ollama_base() else time.time() - 3300
    _catalog_cache.update(at=fetched_at, models=rows, source=source)
    return _catalog_cache


async def web_search(query: str, limit: int = 5) -> list[dict[str, str]]:
    """Free web search (DuckDuckGo HTML results). No key, no cost."""
    import html as _html
    import re
    from urllib.parse import parse_qs, unquote, urlparse
    try:
        async with httpx.AsyncClient(timeout=12.0, headers={"User-Agent": "Mozilla/5.0 (KingdomAIOS)"}) as client:
            r = await client.post("https://html.duckduckgo.com/html/", data={"q": query[:300]})
        r.raise_for_status()
    except httpx.HTTPError:
        return []
    out: list[dict[str, str]] = []
    blocks = re.findall(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>(.*?)(?=class="result__a"|$)', r.text, re.S)
    for href, title, rest in blocks:
        href = _html.unescape(href)
        if "uddg=" in href:
            href = unquote(parse_qs(urlparse(href).query).get("uddg", [href])[0])
        if not href.startswith("http") or "duckduckgo.com" in href or any(o["url"] == href for o in out):
            continue
        snip = re.search(r'class="result__snippet"[^>]*>(.*?)</a>', rest, re.S)
        clean = lambda t: _html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
        out.append({"url": href, "title": clean(title) or href, "snippet": clean(snip.group(1)) if snip else ""})
        if len(out) >= limit:
            break
    return out


def system_prompt(tab_id: str, tab_name: str) -> str:
    focus = TAB_FOCUS.get(tab_id, f"You are the assistant for the '{tab_name}' workspace.")
    today = time.strftime("%A, %B %d, %Y")
    return f"{BASE_RULES}\n\nToday is {today}. Workspace: {tab_name}. {focus}"


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
    if model_id.startswith("ollama/"):
        if not ollama_base():
            raise ProviderError(f"{model_id}: no self-hosted model server (OLLAMA_BASE_URL) is configured")
        url, wire_model = ollama_base() + "/v1/chat/completions", model_id[len("ollama/"):]
        headers = {"Content-Type": "application/json"}
        timeout = 600.0
    else:
        if FREE_ONLY and not is_free(model_id):
            raise ProviderError(f"{model_id}: paid model blocked (free-only mode)")
        if not api_key():
            raise ProviderError(f"{model_id}: needs a free OpenRouter account key (OPENROUTER_API_KEY)")
        url, wire_model = OPENROUTER_BASE + "/chat/completions", model_id
        headers = {"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json",
                   "HTTP-Referer": os.getenv("KAIOS_PUBLIC_URL", "https://kingdom-ai-os.local"), "X-Title": "Kingdom AI OS"}
        timeout = 120.0
    payload: dict[str, Any] = {"model": wire_model, "messages": messages, "max_tokens": max_tokens}
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(url, headers=headers, json=payload)
    if r.status_code != 200:
        try:
            err = r.json().get("error")
            msg = err.get("message", "") if isinstance(err, dict) else str(err or "")
        except ValueError:
            msg = ""
        raise ProviderError(f"{model_id}: HTTP {r.status_code} {msg}"[:300])
    data = r.json()
    choice = (data.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    content = message.get("content") or ""
    if not content.strip():
        raise ProviderError(f"{model_id}: empty response")
    returned = data.get("model") or wire_model
    if model_id.startswith("ollama/") and not str(returned).startswith("ollama/"):
        returned = "ollama/" + str(returned)
    return {"content": content, "model_id": returned, "citations": [], "usage": data.get("usage") or {}}


async def answer(model_id: str | None, messages: list[dict[str, Any]], web: bool, max_tokens: int = 4000) -> dict[str, Any]:
    """Try the chosen model, then fall back through the free default chain. Web search is free (DuckDuckGo)."""
    if not chat_ready():
        raise ProviderError("No model server is configured: set OLLAMA_BASE_URL (self-hosted) or OPENROUTER_API_KEY (free account)")
    citations: list[dict[str, str]] = []
    if web:
        question = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        citations = await web_search(question.split("\n\nAttached files:")[0])
        if citations:
            ctx = "\n".join(f"[{i}] {c['title']} — {c['url']}\n{c['snippet']}" for i, c in enumerate(citations, 1))
            messages = [*messages[:-1], {"role": "system", "content": "Web results (cite as [n]):\n" + ctx}, messages[-1]]
    wanted = model_id or default_model()
    chain = [wanted, default_model(), *fallback_models()]
    seen: list[str] = []
    errors: list[str] = []
    for m in chain:
        if m in seen:
            continue
        seen.append(m)
        try:
            result = await _call(m, messages, web, max_tokens)
            result["citations"] = result.get("citations") or [{"url": c["url"], "title": c["title"]} for c in citations]
            result["requested_model"] = wanted
            result["fell_back"] = m != wanted
            result["errors"] = errors
            return result
        except (ProviderError, httpx.HTTPError) as exc:
            errors.append(str(exc)[:300] or type(exc).__name__)
    raise ProviderError("All models failed: " + " | ".join(errors))
