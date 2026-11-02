"""Router for OSINT (osint)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "osint",
    "OSINT",
    "Open source intelligence collection with SpiderFoot, theHarvester, Maltego transforms, Sherlock, and evidence custody.",
)

__all__ = ["router"]
