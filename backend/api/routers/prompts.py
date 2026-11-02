"""Prompt templates and versioning router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/prompts", tags=["prompts"])


@router.get("")
async def prompts_index() -> dict[str, str]:
    """Return service metadata for the prompts router."""
    return {
        "service": "prompts",
        "prefix": "/api/prompts",
        "status": "ok",
        "description": "Prompt templates and versioning",
    }


@router.get("/health")
async def prompts_health() -> dict[str, str]:
    """Return a targeted health status for the prompts service."""
    return {"service": "prompts", "status": "ok"}
