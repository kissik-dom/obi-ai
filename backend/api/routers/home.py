"""Router for Home/Command Center (home)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "home",
    "Home/Command Center",
    "Mission control for the Kingdom AI OS: aggregate status, live queues, idle capacity, and one-click dispatch.",
)

__all__ = ["router"]
