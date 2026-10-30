"""Router for Investments (investments)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "investments",
    "Investments",
    "Investment pipeline, deal scoring, cap tables, due diligence, and scenario simulations.",
)

__all__ = ["router"]
