"""Router for LLM/Models (llm)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "llm",
    "LLM/Models",
    "Model registry, Tier S/B/V routing, OpenRouter key rotation, fallback chains, VRAM filters, and inference cost controls.",
)

__all__ = ["router"]
