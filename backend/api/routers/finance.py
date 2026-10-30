"""Router for Finance (finance)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "finance",
    "Finance",
    "Finance analytics, portfolio data, ledger ingestion, market signals, and guardrailed financial vault outputs.",
)

__all__ = ["router"]
