"""Verify zero private keys in .env.example and strict 10 req/sec financial Vault rate limiting."""

from pathlib import Path
from fastapi.testclient import TestClient

from backend.core import config
from backend.main import app


def test_zero_financial_private_keys_in_env_example() -> None:
    env_txt = Path(".env.example").read_text(encoding="utf-8")
    assert "BEGIN PRIVATE KEY" not in env_txt
    assert "ETH_PRIVATE_KEY=" not in env_txt
    assert "BTC_WIF=" not in env_txt


def test_financial_10_req_per_sec_rate_limit_and_owner_bypass() -> None:
    with TestClient(app) as client:
        statuses = [client.get("/api/tabs/finance/settings").status_code for _ in range(13)]
        assert 429 in statuses

        # Owner with X-Kingdom-Internal header is never locked out even during burst
        owner_res = client.get(
            "/api/tabs/finance/settings",
            headers={"X-Kingdom-Internal": config.SETTINGS.kingdom_internal_secret},
        )
        assert owner_res.status_code == 200
