"""Tab router factory and registry for Kingdom AI OS.

Every one of the 24 tabs exposes the identical ten-piece grammar:

Chat | Agents | Open Tasks | Completed Tasks | Training | Knowledge | Files | Tools | Outputs | Settings
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Header, HTTPException, Query, Request
from pydantic import BaseModel, Field

TAB_DEFINITIONS: List[Dict[str, str]] = [
    {"slug": "home", "title": "Home/Command Center", "description": "Mission control for the Kingdom AI OS: aggregate status, live queues, idle capacity, and one-click dispatch."},
    {"slug": "llm", "title": "LLM/Models", "description": "Model registry, Tier S/B/V routing, OpenRouter key rotation, fallback chains, VRAM filters, and inference cost controls."},
    {"slug": "research", "title": "Research", "description": "Deep research pipelines with Perplexica, Haystack, LangChain, LlamaIndex, DSPy, web search, and citation graphs."},
    {"slug": "legal", "title": "Legal", "description": "Legal research, contract review, compliance checklists, jurisdiction packs, and privilege-aware document handling."},
    {"slug": "osint", "title": "OSINT", "description": "Open source intelligence collection with SpiderFoot, theHarvester, Maltego transforms, Sherlock, and evidence custody."},
    {"slug": "finance", "title": "Finance", "description": "Finance analytics, portfolio data, ledger ingestion, market signals, and guardrailed financial vault outputs."},
    {"slug": "investments", "title": "Investments", "description": "Investment pipeline, deal scoring, cap tables, due diligence, and scenario simulations."},
    {"slug": "real_estate", "title": "Real Estate", "description": "Property underwriting, title/parcel research, zoning, comps, cashflow models, and document packages."},
    {"slug": "business", "title": "Business/CRM", "description": "Business automation, CRM entities, pipeline stages, deal rooms, and client lifecycle signals."},
    {"slug": "leads", "title": "Leads", "description": "Lead enrichment, scoring, routing, cadence orchestration, and reply generation from CRM sources."},
    {"slug": "urban_planning", "title": "City/Urban Planning", "description": "Urban planning maps, zoning, census layers, infrastructure models, GHG and traffic impact analysis."},
    {"slug": "engineering_ghidra", "title": "Engineering GHIDRA Anti-Gravity", "description": "Reverse engineering and anti-gravity engineering sandbox with GHIDRA, FreeCAD, OpenSCAD, Blender, and KiCad."},
    {"slug": "coding", "title": "Coding/Dev", "description": "Software engineering agents, code review, test generation, dependency analysis, and deployment runbooks."},
    {"slug": "web_scraping", "title": "Web/Scraping", "description": "Scraping with Apify, Scrapy, Playwright, Selenium, queue fairness, robots policy, and schema extraction."},
    {"slug": "news", "title": "News/Magazines", "description": "News monitoring, magazine pipelines, source credibility scoring, article extraction, and archives."},
    {"slug": "social_marketing", "title": "Social/Marketing", "description": "Social listening, campaign generation, content calendars, A/B copy, and brand-safe publishing."},
    {"slug": "fashion", "title": "Fashion", "description": "Fashion trend research, lookbooks, product data, image consistency, and collection briefs."},
    {"slug": "images_visual", "title": "Images/Visual AI", "description": "Image generation with FLUX.1, Juggernaut, SAM2, ControlNet, and vision models; visual QA and consistency."},
    {"slug": "video_ugc", "title": "Video/UGC/TV/Movies", "description": "UGC and cinematic video with MiniMax Hailuo-02, Wan 2.1, LTX-Video, Kling 2.0, FFmpeg stitching, and shot lists."},
    {"slug": "music_audio", "title": "Music/Audio Vocal Tuning", "description": "Music and audio vocal tuning with GSnap, MAutoPitch, Spleeter, Demucs, RVC, and mixing tools."},
    {"slug": "agents_comms", "title": "Agents/Communications", "description": "Agent fleet and messaging with WAHA, Baileys, Evolution API, CUA spaces, and Hermes routing."},
    {"slug": "tasks", "title": "Tasks", "description": "Task intake, sandbox orchestration, idempotency, requests/finished folders, and completion receipts."},
    {"slug": "open_source", "title": "Open Source/Apps", "description": "Open source app catalog, app runtime sandboxes, dependency scanning, and one-click deployments."},
    {"slug": "security_admin", "title": "Security/Admin", "description": "CrowdSec, Wazuh, Suricata, Falco, Tetragon, Vault HSM, WireGuard, Cowrie, CompreFace, and admin controls."},
]

GRAMMAR: List[str] = [
    "Chat",
    "Agents",
    "Open Tasks",
    "Completed Tasks",
    "Training",
    "Knowledge",
    "Files",
    "Tools",
    "Outputs",
    "Settings",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class GrammarResponse(BaseModel):
    tab: str
    title: str
    grammar: List[str]
    now: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=200_000)
    model: str = Field(default="tier-s-auto", max_length=200)
    session_id: str = Field(default="", max_length=200)
    turnoff_flags: Dict[str, bool] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    tab: str
    message: str
    model: str
    accepted: bool
    request_id: str
    sandbox_id: str | None = None
    now: str


class SettingsRequest(BaseModel):
    settings: Dict[str, Any] = Field(default_factory=dict)


class IdempotentResponse(BaseModel):
    accepted: bool
    request_id: str
    duplicate: bool = False


def make_tab_router(slug: str, title: str, description: str) -> APIRouter:
    """Build the identical ten-section API grammar for one tab."""
    router = APIRouter(prefix=f"/api/{slug}", tags=[slug])

    @router.get("", response_model=GrammarResponse, summary=f"{title}: grammar")
    def tab_root() -> GrammarResponse:
        return GrammarResponse(tab=slug, title=title, grammar=GRAMMAR, now=_now())

    @router.get("/chat", response_model=GrammarResponse, summary=f"{title}: chat surface")
    def chat_get() -> GrammarResponse:
        return GrammarResponse(tab=slug, title=title, grammar=GRAMMAR, now=_now())

    @router.post("/chat", response_model=ChatResponse, status_code=202, summary=f"{title}: submit chat")
    async def chat_post(
        payload: ChatRequest,
        request: Request,
        x_idempotency_key: str = Header(default="", max_length=200),
    ) -> ChatResponse:
        request_id = x_idempotency_key or request.headers.get("x-request-id", f"{slug}-{int(datetime.now().timestamp() * 1000)}")
        # Real deployments persist idempotency keys in Redis before dispatch.
        return ChatResponse(
            tab=slug,
            message=payload.message,
            model=payload.model,
            accepted=True,
            request_id=request_id,
            sandbox_id=None,
            now=_now(),
        )

    @router.get("/agents", response_model=Dict[str, Any], summary=f"{title}: agents")
    def agents() -> Dict[str, Any]:
        return {"tab": slug, "agents": ["BugFix", "Testing", "External Scout", "Internal Optimizer", "CUA Fleet"], "now": _now()}

    @router.get("/tasks/open", response_model=Dict[str, Any], summary=f"{title}: open tasks")
    def open_tasks(status: str = Query(default="open", pattern="^(open|all)$")) -> Dict[str, Any]:
        return {"tab": slug, "status": status, "items": [], "now": _now()}

    @router.get("/tasks/completed", response_model=Dict[str, Any], summary=f"{title}: completed tasks")
    def completed_tasks() -> Dict[str, Any]:
        return {"tab": slug, "status": "completed", "items": [], "now": _now()}

    @router.get("/training", response_model=Dict[str, Any], summary=f"{title}: training")
    def training() -> Dict[str, Any]:
        return {"tab": slug, "repository": f"knowledge/{slug}/training", "policies": ["no PII", "human review required"], "now": _now()}

    @router.get("/knowledge", response_model=Dict[str, Any], summary=f"{title}: knowledge")
    def knowledge() -> Dict[str, Any]:
        return {"tab": slug, "repository": f"knowledge/{slug}", "vector_store": f"qdrant:{slug}", "now": _now()}

    @router.get("/files", response_model=Dict[str, Any], summary=f"{title}: files")
    def files() -> Dict[str, Any]:
        return {"tab": slug, "sandbox_bucket": "kingdom-sandboxes", "finished_folder": f"finished/{slug}", "now": _now()}

    @router.get("/tools", response_model=Dict[str, Any], summary=f"{title}: tools")
    def tools() -> Dict[str, Any]:
        return {"tab": slug, "tool_catalog": f"docs/TOOL_REGISTRY.md", "categories": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"], "now": _now()}

    @router.get("/outputs", response_model=Dict[str, Any], summary=f"{title}: outputs")
    def outputs() -> Dict[str, Any]:
        return {"tab": slug, "outputs_folder": f"finished/{slug}", "formats": ["json", "markdown", "parquet", "pdf"], "now": _now()}

    @router.get("/settings", response_model=Dict[str, Any], summary=f"{title}: settings")
    def settings() -> Dict[str, Any]:
        return {"tab": slug, "turnoff_flags": {"sandbox": False, "agents": False, "gpu": False, "video": False, "image": False}, "now": _now()}

    @router.put("/settings", response_model=IdempotentResponse, status_code=202, summary=f"{title}: update settings")
    async def settings_put(
        payload: SettingsRequest,
        x_idempotency_key: str = Header(default="", max_length=200),
    ) -> IdempotentResponse:
        request_id = x_idempotency_key or f"{slug}-settings-{int(datetime.now().timestamp() * 1000)}"
        return IdempotentResponse(accepted=True, request_id=request_id)

    return router


__all__ = ["TAB_DEFINITIONS", "GRAMMAR", "make_tab_router"]
