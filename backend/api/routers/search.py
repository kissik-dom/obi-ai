"""Web, vector, and enterprise search router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("")
async def search_index() -> dict[str, str]:
    """Return service metadata for the search router."""
    return {
        "service": "search",
        "prefix": "/api/search",
        "status": "ok",
        "description": "Web, vector, and enterprise search",
    }


@router.get("/health")
async def search_health() -> dict[str, str]:
    """Return a targeted health status for the search service."""
    return {"service": "search", "status": "ok"}
