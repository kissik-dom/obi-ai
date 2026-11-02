"""Workflow execution and scheduling router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


@router.get("")
async def workflows_index() -> dict[str, str]:
    """Return service metadata for the workflows router."""
    return {
        "service": "workflows",
        "prefix": "/api/workflows",
        "status": "ok",
        "description": "Workflow execution and scheduling",
    }


@router.get("/health")
async def workflows_health() -> dict[str, str]:
    """Return a targeted health status for the workflows service."""
    return {"service": "workflows", "status": "ok"}
