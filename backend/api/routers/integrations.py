"""Third-party integration configuration router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


@router.get("")
async def integrations_index() -> dict[str, str]:
    """Return service metadata for the integrations router."""
    return {
        "service": "integrations",
        "prefix": "/api/integrations",
        "status": "ok",
        "description": "Third-party integration configuration",
    }


@router.get("/health")
async def integrations_health() -> dict[str, str]:
    """Return a targeted health status for the integrations service."""
    return {"service": "integrations", "status": "ok"}
