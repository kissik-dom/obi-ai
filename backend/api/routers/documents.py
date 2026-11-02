"""Document creation, parsing, and templates router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("")
async def documents_index() -> dict[str, str]:
    """Return service metadata for the documents router."""
    return {
        "service": "documents",
        "prefix": "/api/documents",
        "status": "ok",
        "description": "Document creation, parsing, and templates",
    }


@router.get("/health")
async def documents_health() -> dict[str, str]:
    """Return a targeted health status for the documents service."""
    return {"service": "documents", "status": "ok"}
