"""Code execution sandbox and tool gating router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/sandbox", tags=["sandbox"])


@router.get("")
async def sandbox_index() -> dict[str, str]:
    """Return service metadata for the sandbox router."""
    return {
        "service": "sandbox",
        "prefix": "/api/sandbox",
        "status": "ok",
        "description": "Code execution sandbox and tool gating",
    }


@router.get("/health")
async def sandbox_health() -> dict[str, str]:
    """Return a targeted health status for the sandbox service."""
    return {"service": "sandbox", "status": "ok"}
