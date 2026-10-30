"""Authentication, api keys, and session issuance router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("")
async def auth_index() -> dict[str, str]:
    """Return service metadata for the auth router."""
    return {
        "service": "auth",
        "prefix": "/api/auth",
        "status": "ok",
        "description": "Authentication, API keys, and session issuance",
    }


@router.get("/health")
async def auth_health() -> dict[str, str]:
    """Return a targeted health status for the auth service."""
    return {"service": "auth", "status": "ok"}
