"""Conversation and completion endpoints router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.get("")
async def chat_index() -> dict[str, str]:
    """Return service metadata for the chat router."""
    return {
        "service": "chat",
        "prefix": "/api/chat",
        "status": "ok",
        "description": "Conversation and completion endpoints",
    }


@router.get("/health")
async def chat_health() -> dict[str, str]:
    """Return a targeted health status for the chat service."""
    return {"service": "chat", "status": "ok"}
