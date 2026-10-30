"""Short-term and long-term agent memory router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/memory", tags=["memory"])


@router.get("")
async def memory_index() -> dict[str, str]:
    """Return service metadata for the memory router."""
    return {
        "service": "memory",
        "prefix": "/api/memory",
        "status": "ok",
        "description": "Short-term and long-term agent memory",
    }


@router.get("/health")
async def memory_health() -> dict[str, str]:
    """Return a targeted health status for the memory service."""
    return {"service": "memory", "status": "ok"}
