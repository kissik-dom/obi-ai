"""Verify 2,000 CUA Spaces x 5 Official Business Graph Accounts = 10,000 Isolated Accounts."""

from fastapi.testclient import TestClient

from backend.main import app


def test_cua_2000_spaces_x_5_accounts_strict_isolation() -> None:
    with TestClient(app) as client:
        res = client.get("/api/agents/cua/isolation")
        assert res.status_code == 200
        body = res.json()
        assert body["cua_spaces_total"] == 2000
        assert body["accounts_per_space"] == 5
        assert body["total_official_accounts"] == 10000
        assert body["zero_shared_subnets_in_sample"] is True
        assert body["zero_shared_cookie_jars_in_sample"] is True
        assert body["wireguard_zero_trust"] is True
        assert body["falco_ebpf_enforced"] is True
