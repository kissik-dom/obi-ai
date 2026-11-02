"""Capability, tool, and service discovery router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/discovery", tags=["discovery"])


@router.get("")
async def discovery_index() -> dict[str, str]:
    """Return service metadata for the discovery router."""
    return {
        "service": "discovery",
        "prefix": "/api/discovery",
        "status": "ok",
        "description": "Capability, tool, and service discovery",
    }


@router.get("/health")
async def discovery_health() -> dict[str, str]:
    """Return a targeted health status for the discovery service."""
    return {"service": "discovery", "status": "ok"}
