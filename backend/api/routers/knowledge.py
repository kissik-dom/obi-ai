"""Knowledge graph and entity management router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.get("")
async def knowledge_index() -> dict[str, str]:
    """Return service metadata for the knowledge router."""
    return {
        "service": "knowledge",
        "prefix": "/api/knowledge",
        "status": "ok",
        "description": "Knowledge graph and entity management",
    }


@router.get("/health")
async def knowledge_health() -> dict[str, str]:
    """Return a targeted health status for the knowledge service."""
    return {"service": "knowledge", "status": "ok"}
