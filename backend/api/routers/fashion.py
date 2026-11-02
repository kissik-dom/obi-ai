"""Router for Fashion (fashion)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "fashion",
    "Fashion",
    "Fashion trend research, lookbooks, product data, image consistency, and collection briefs.",
)

__all__ = ["router"]
