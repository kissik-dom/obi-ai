"""Internal event stream and audit log router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("")
async def events_index() -> dict[str, str]:
    """Return service metadata for the events router."""
    return {
        "service": "events",
        "prefix": "/api/events",
        "status": "ok",
        "description": "Internal event stream and audit log",
    }


@router.get("/health")
async def events_health() -> dict[str, str]:
    """Return a targeted health status for the events service."""
    return {"service": "events", "status": "ok"}
