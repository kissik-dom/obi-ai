"""BugFix + Testing Self-Healing Status & Trigger Router."""

from __future__ import annotations

from fastapi import APIRouter

from backend.agents.bugfix_agent import get_bugfix_status, run_bugfix_cycle
from backend.core.schemas import BugfixStatusResponse, BugfixTriggerRequest

router = APIRouter(prefix="/api/bugfix", tags=["domain:bugfix"])


@router.get("/status", response_model=BugfixStatusResponse)
async def bugfix_status() -> BugfixStatusResponse:
    return get_bugfix_status()


@router.post("/trigger", response_model=BugfixStatusResponse)
async def bugfix_trigger(payload: BugfixTriggerRequest) -> BugfixStatusResponse:
    return run_bugfix_cycle(payload)
