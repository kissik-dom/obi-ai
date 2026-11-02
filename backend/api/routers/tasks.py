"""Router for Tasks (tasks)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "tasks",
    "Tasks",
    "Task intake, sandbox orchestration, idempotency, requests/finished folders, and completion receipts.",
)

__all__ = ["router"]
