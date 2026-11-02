"""Router for Real Estate (real_estate)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "real_estate",
    "Real Estate",
    "Property underwriting, title/parcel research, zoning, comps, cashflow models, and document packages.",
)

__all__ = ["router"]
