"""Router for Security/Admin (security_admin)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "security_admin",
    "Security/Admin",
    "CrowdSec, Wazuh, Suricata, Falco, Tetragon, Vault HSM, WireGuard, Cowrie, CompreFace, and admin controls.",
)

__all__ = ["router"]
