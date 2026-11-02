"""Llm gateway and provider routing router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/gateway", tags=["gateway"])


@router.get("")
async def gateway_index() -> dict[str, str]:
    """Return service metadata for the gateway router."""
    return {
        "service": "gateway",
        "prefix": "/api/gateway",
        "status": "ok",
        "description": "LLM gateway and provider routing",
    }


@router.get("/health")
async def gateway_health() -> dict[str, str]:
    """Return a targeted health status for the gateway service."""
    return {"service": "gateway", "status": "ok"}
