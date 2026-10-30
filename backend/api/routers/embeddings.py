"""Embedding generation and vector indexing router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/embeddings", tags=["embeddings"])


@router.get("")
async def embeddings_index() -> dict[str, str]:
    """Return service metadata for the embeddings router."""
    return {
        "service": "embeddings",
        "prefix": "/api/embeddings",
        "status": "ok",
        "description": "Embedding generation and vector indexing",
    }


@router.get("/health")
async def embeddings_health() -> dict[str, str]:
    """Return a targeted health status for the embeddings service."""
    return {"service": "embeddings", "status": "ok"}
