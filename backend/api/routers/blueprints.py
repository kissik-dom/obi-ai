"""Reusable ecosystem and automation blueprints router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/blueprints", tags=["blueprints"])


@router.get("")
async def blueprints_index() -> dict[str, str]:
    """Return service metadata for the blueprints router."""
    return {
        "service": "blueprints",
        "prefix": "/api/blueprints",
        "status": "ok",
        "description": "Reusable ecosystem and automation blueprints",
    }


@router.get("/health")
async def blueprints_health() -> dict[str, str]:
    """Return a targeted health status for the blueprints service."""
    return {"service": "blueprints", "status": "ok"}
