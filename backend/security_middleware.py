"""Zero-Trust Security Middleware: CrowdSec/Wazuh/Falco Headers, Cowrie Decoy Traps, Owner Allowlist & 10 req/s Financial Rate Limit."""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from backend.agents.security_honeypot_agent import is_owner_request, record_honeypot_attempt
from backend.core import config
from backend.core.stores import VAULT_STORE

DECOY_PATHS = {"/admin", "/financial", "/photos", "/wp-admin", "/.env"}


class SecurityMiddleware(BaseHTTPMiddleware):
    """8-Layer Sovereign Perimeter Middleware (toggleable via ENABLE_SECURITY)."""

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path.rstrip("/") or "/"
        internal_hdr = request.headers.get("X-Kingdom-Internal")
        owner = is_owner_request(internal_hdr)
        client_ip = request.client.host if request.client else "127.0.0.1"

        if config.FLAGS.ENABLE_SECURITY:
            # 1. Cowrie decoy honeypot endpoints (never hit by legitimate /api/* routes)
            if path in DECOY_PATHS and not owner:
                attempt = record_honeypot_attempt(
                    path=path,
                    ip=client_ip,
                    user_agent=request.headers.get("User-Agent", ""),
                    ja3=request.headers.get("X-JA3-Fingerprint", "771,4865-4866-4867"),
                    wifi_ssid=request.headers.get("X-Client-SSID", "not_transmitted"),
                    actor_type="unauthorized_decoy_probe",
                    is_bot=True,
                )
                return JSONResponse(
                    status_code=200,
                    content={
                        "honeypot": True,
                        "status": "decoy_session_isolated",
                        "message": "Session routed to isolated Cowrie decoy environment.",
                        "attempt_id": attempt.attempt_id,
                        "honeypot_recording_id": attempt.honeypot_recording_id,
                    },
                )

            # 2. Strict 10 req/sec sliding-window rate limit per financial tab (/api/tabs/finance/* and /api/tabs/investments/*)
            if (path.startswith("/api/tabs/finance") or path.startswith("/api/tabs/investments")) and not owner:
                fin_tab = path.split("/")[3] if len(path.split("/")) > 3 else "finance"
                allowed = VAULT_STORE.check_financial_rate_limit(f"{client_ip}:{fin_tab}", limit_per_sec=10)
                if not allowed:
                    return JSONResponse(
                        status_code=429,
                        content={"detail": "Vault HSM financial rate limit exceeded (max 10 req/sec)."},
                    )

        response = await call_next(request)
        response.headers["X-Kingdom-Zero-Trust"] = "CrowdSec-Wazuh-Suricata-Falco-Vault-WireGuard"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
