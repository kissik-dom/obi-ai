"""Operational metrics and telemetry router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("")
async def metrics_index() -> dict[str, str]:
    """Return service metadata for the metrics router."""
    return {
        "service": "metrics",
        "prefix": "/api/metrics",
        "status": "ok",
        "description": "Operational metrics and telemetry",
    }


@router.get("/health")
async def metrics_health() -> dict[str, str]:
    """Return a targeted health status for the metrics service."""
    return {"service": "metrics", "status": "ok"}
