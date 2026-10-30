"""Vault-backed secrets and security policy router."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/security", tags=["security"])


@router.get("")
async def security_index() -> dict[str, str]:
    """Return service metadata for the security router."""
    return {
        "service": "security",
        "prefix": "/api/security",
        "status": "ok",
        "description": "Vault-backed secrets and security policy",
    }


@router.get("/health")
async def security_health() -> dict[str, str]:
    """Return a targeted health status for the security service."""
    return {"service": "security", "status": "ok"}
