"""User and agent session management router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.get("")
async def sessions_index() -> dict[str, str]:
    """Return service metadata for the sessions router."""
    return {
        "service": "sessions",
        "prefix": "/api/sessions",
        "status": "ok",
        "description": "User and agent session management",
    }


@router.get("/health")
async def sessions_health() -> dict[str, str]:
    """Return a targeted health status for the sessions service."""
    return {"service": "sessions", "status": "ok"}
