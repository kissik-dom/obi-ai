"""Router for Social/Marketing (social_marketing)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "social_marketing",
    "Social/Marketing",
    "Social listening, campaign generation, content calendars, A/B copy, and brand-safe publishing.",
)

__all__ = ["router"]
