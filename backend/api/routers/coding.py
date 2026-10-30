"""Router for Coding/Dev (coding)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "coding",
    "Coding/Dev",
    "Software engineering agents, code review, test generation, dependency analysis, and deployment runbooks.",
)

__all__ = ["router"]
