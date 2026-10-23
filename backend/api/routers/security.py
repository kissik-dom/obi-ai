"""Tab 24: Security / Admin Router (10-Section Grammar + Cowrie Honeypot Logs, Police PDF Export, Bot Check & Opt-In Biometric)."""

from __future__ import annotations

import asyncio
from typing import Optional

from fastapi import APIRouter, Header, Response

from backend.agents.security_honeypot_agent import (
    enroll_biometric_opt_in,
    evaluate_bot_check,
    export_police_audit_pdf,
    list_security_attempts,
)
from backend.api.routers._tab_factory import build_tab_router
from backend.core.schemas import (
    BiometricOptInRequest,
    BiometricOptInResponse,
    BotCheckRequest,
    BotCheckResponse,
    SecurityAttemptsResponse,
)

router = build_tab_router("security")
domain_router = APIRouter(prefix="/api/security", tags=["domain:security"])


@domain_router.get("/attempts", response_model=SecurityAttemptsResponse)
async def get_security_attempts() -> SecurityAttemptsResponse:
    return SecurityAttemptsResponse(
        status="active",
        layers=[
            "CrowdSec 100k WAF",
            "Wazuh 4.8 SIEM FIM",
            "Suricata 7 IDS",
            "Falco eBPF + Tetragon",
            "Vault 1.15 HSM",
            "WireGuard Zero Trust",
            "Cowrie SSH/HTTP Honeypot",
            "CompreFace FIDO2 VideoKYC",
        ],
        attempts=list_security_attempts(),
    )


@domain_router.get("/audit/export")
async def get_security_audit_pdf() -> Response:
    loop = asyncio.get_running_loop()
    pdf_bytes = await loop.run_in_executor(None, export_police_audit_pdf)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="kingdom_police_audit_report.pdf"'},
    )


@domain_router.post("/biometric/opt-in", response_model=BiometricOptInResponse)
async def post_biometric_opt_in(
    payload: BiometricOptInRequest,
    x_kingdom_internal: Optional[str] = Header(default=None),
) -> BiometricOptInResponse:
    return enroll_biometric_opt_in(payload, internal_header=x_kingdom_internal)


@domain_router.post("/bot/check", response_model=BotCheckResponse)
async def post_bot_check(
    payload: BotCheckRequest,
    x_kingdom_internal: Optional[str] = Header(default=None),
) -> BotCheckResponse:
    return evaluate_bot_check(payload, internal_header=x_kingdom_internal)
