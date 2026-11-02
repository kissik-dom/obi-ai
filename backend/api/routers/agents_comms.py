"""Router for Agents/Communications (agents_comms)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "agents_comms",
    "Agents/Communications",
    "Agent fleet and messaging with WAHA, Baileys, Evolution API, CUA spaces, and Hermes routing.",
)

__all__ = ["router"]
