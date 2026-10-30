"""Router for Open Source/Apps (open_source)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "open_source",
    "Open Source/Apps",
    "Open source app catalog, app runtime sandboxes, dependency scanning, and one-click deployments.",
)

__all__ = ["router"]
