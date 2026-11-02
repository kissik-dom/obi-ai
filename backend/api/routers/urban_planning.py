"""Router for City/Urban Planning (urban_planning)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "urban_planning",
    "City/Urban Planning",
    "Urban planning maps, zoning, census layers, infrastructure models, GHG and traffic impact analysis.",
)

__all__ = ["router"]
