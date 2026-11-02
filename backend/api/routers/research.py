"""Router for Research (research)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "research",
    "Research",
    "Deep research pipelines with Perplexica, Haystack, LangChain, LlamaIndex, DSPy, web search, and citation graphs.",
)

__all__ = ["router"]
