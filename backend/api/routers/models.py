"""Model catalog, tiers, and routing configuration router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("")
async def models_index() -> dict[str, str]:
    """Return service metadata for the models router."""
    return {
        "service": "models",
        "prefix": "/api/models",
        "status": "ok",
        "description": "Model catalog, tiers, and routing configuration",
    }


@router.get("/health")
async def models_health() -> dict[str, str]:
    """Return a targeted health status for the models service."""
    return {"service": "models", "status": "ok"}
