"""Agent lifecycle, registry, and runtime control router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("")
async def agents_index() -> dict[str, str]:
    """Return service metadata for the agents router."""
    return {
        "service": "agents",
        "prefix": "/api/agents",
        "status": "ok",
        "description": "Agent lifecycle, registry, and runtime control",
    }


@router.get("/health")
async def agents_health() -> dict[str, str]:
    """Return a targeted health status for the agents service."""
    return {"service": "agents", "status": "ok"}
