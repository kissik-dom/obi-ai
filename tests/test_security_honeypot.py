"""Verify Cowrie Honeypot decoys, Police PDF export, BIPA/GDPR explicit VideoKYC opt-in, and Owner Allowlist."""

from fastapi.testclient import TestClient

from backend.core import config
from backend.main import app


def test_cowrie_honeypot_and_police_pdf_export() -> None:
    with TestClient(app) as client:
        for decoy in ["/admin", "/financial", "/photos"]:
            r = client.get(decoy)
            assert r.status_code == 200
            assert r.json()["honeypot"] is True

        attempts = client.get("/api/security/attempts")
        assert attempts.status_code == 200
        assert len(attempts.json()["attempts"]) >= 3

        pdf = client.get("/api/security/audit/export")
        assert pdf.status_code == 200
        assert pdf.headers["content-type"] == "application/pdf"
        assert pdf.content.startswith(b"%PDF")


def test_biometric_explicit_opt_in_and_owner_allowlist() -> None:
    with TestClient(app) as client:
        declined = client.post(
            "/api/security/biometric/opt-in",
            json={"consent": False, "bipa_gdpr_acknowledged": False, "subject_id": "guest-1"},
        )
        assert declined.status_code == 200
        assert declined.json()["verified"] is False
        assert declined.json()["vault_hsm_key_id"] == "none"

        accepted = client.post(
            "/api/security/biometric/opt-in",
            json={"consent": True, "bipa_gdpr_acknowledged": True, "subject_id": "operator-1"},
        )
        assert accepted.status_code == 200
        assert accepted.json()["verified"] is True
        assert accepted.json()["retention_days"] == 30

        bot_owner = client.post(
            "/api/security/bot/check",
            json={"mouse_moves": 0, "request_interval_ms": 1},
            headers={"X-Kingdom-Internal": config.SETTINGS.kingdom_internal_secret},
        )
        assert bot_owner.status_code == 200
        assert bot_owner.json()["owner_allowlisted"] is True
        assert bot_owner.json()["is_bot"] is False
