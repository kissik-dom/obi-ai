"""Hermes agent swarm orchestration router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/hermes", tags=["hermes"])


@router.get("")
async def hermes_index() -> dict[str, str]:
    """Return service metadata for the hermes router."""
    return {
        "service": "hermes",
        "prefix": "/api/hermes",
        "status": "ok",
        "description": "Hermes agent swarm orchestration",
    }


@router.get("/health")
async def hermes_health() -> dict[str, str]:
    """Return a targeted health status for the hermes service."""
    return {"service": "hermes", "status": "ok"}
