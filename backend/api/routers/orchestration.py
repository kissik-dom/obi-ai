"""Workflow orchestration and dependency control router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/orchestration", tags=["orchestration"])


@router.get("")
async def orchestration_index() -> dict[str, str]:
    """Return service metadata for the orchestration router."""
    return {
        "service": "orchestration",
        "prefix": "/api/orchestration",
        "status": "ok",
        "description": "Workflow orchestration and dependency control",
    }


@router.get("/health")
async def orchestration_health() -> dict[str, str]:
    """Return a targeted health status for the orchestration service."""
    return {"service": "orchestration", "status": "ok"}
