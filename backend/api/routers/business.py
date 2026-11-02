"""Router for Business/CRM (business)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "business",
    "Business/CRM",
    "Business automation, CRM entities, pipeline stages, deal rooms, and client lifecycle signals.",
)

__all__ = ["router"]
