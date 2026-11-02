"""Router for News/Magazines (news)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "news",
    "News/Magazines",
    "News monitoring, magazine pipelines, source credibility scoring, article extraction, and archives.",
)

__all__ = ["router"]
