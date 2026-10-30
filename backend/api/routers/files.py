"""Object storage and upload management router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/files", tags=["files"])


@router.get("")
async def files_index() -> dict[str, str]:
    """Return service metadata for the files router."""
    return {
        "service": "files",
        "prefix": "/api/files",
        "status": "ok",
        "description": "Object storage and upload management",
    }


@router.get("/health")
async def files_health() -> dict[str, str]:
    """Return a targeted health status for the files service."""
    return {"service": "files", "status": "ok"}
