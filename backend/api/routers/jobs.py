"""Celery/redis job submission and status router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("")
async def jobs_index() -> dict[str, str]:
    """Return service metadata for the jobs router."""
    return {
        "service": "jobs",
        "prefix": "/api/jobs",
        "status": "ok",
        "description": "Celery/Redis job submission and status",
    }


@router.get("/health")
async def jobs_health() -> dict[str, str]:
    """Return a targeted health status for the jobs service."""
    return {"service": "jobs", "status": "ok"}
