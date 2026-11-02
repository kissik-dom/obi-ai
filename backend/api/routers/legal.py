"""Router for Legal (legal)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "legal",
    "Legal",
    "Legal research, contract review, compliance checklists, jurisdiction packs, and privilege-aware document handling.",
)

__all__ = ["router"]
