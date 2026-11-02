"""Router for Leads (leads)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "leads",
    "Leads",
    "Lead enrichment, scoring, routing, cadence orchestration, and reply generation from CRM sources.",
)

__all__ = ["router"]
