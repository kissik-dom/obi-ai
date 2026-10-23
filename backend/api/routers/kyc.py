"""Legal BIPA/GDPR VideoKYC & Sovereign Seal OMNIVIDENS Passport Router."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Header
from pydantic import BaseModel, ConfigDict

from backend.agents.passport_agent import issue_omnividens_passport
from backend.agents.security_honeypot_agent import (
    VERIFIED_KYC_SESSIONS,
    enroll_biometric_opt_in,
    is_owner_request,
)
from backend.core.schemas import BiometricOptInRequest, BiometricOptInResponse

router = APIRouter(prefix="/api/kyc", tags=["domain:kyc"])
passport_domain_router = APIRouter(prefix="/api/passport", tags=["domain:passport"])


class KycStatusResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enrolled_subjects: int
    owner_allowlisted: bool
    retention_days: int = 30
    compliance: str = "BIPA + GDPR Explicit Opt-In + Vault HSM"


class PassportIssueRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    holder: str = "Sovereign Operator"
    scope: str = "global-tabs-1-28"


class PassportIssueResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    passport_id: str
    holder: str
    scope: str
    qr_payload: str
    vault_hsm_ref: str
    opentimestamps_proof: str
    ipfs_cid: str
    issued_at: str


@router.get("/status", response_model=KycStatusResponse)
async def get_kyc_status(x_kingdom_internal: Optional[str] = Header(default=None)) -> KycStatusResponse:
    return KycStatusResponse(
        enrolled_subjects=len(VERIFIED_KYC_SESSIONS),
        owner_allowlisted=is_owner_request(x_kingdom_internal),
    )


@router.post("/verify", response_model=BiometricOptInResponse)
async def post_kyc_verify(
    payload: BiometricOptInRequest,
    x_kingdom_internal: Optional[str] = Header(default=None),
) -> BiometricOptInResponse:
    return enroll_biometric_opt_in(payload, internal_header=x_kingdom_internal)


@passport_domain_router.post("/issue", response_model=PassportIssueResponse)
async def post_issue_passport(payload: PassportIssueRequest) -> PassportIssueResponse:
    res = issue_omnividens_passport(holder=payload.holder, scope=payload.scope)
    return PassportIssueResponse(**res)
