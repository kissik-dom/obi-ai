"""Verify Headless GHIDRA P-Code Reverse Engineering Endpoint."""

from fastapi.testclient import TestClient

from backend.main import app


def test_ghidra_binary_decompilation() -> None:
    with TestClient(app) as client:
        res = client.post(
            "/api/engineering/ghidra/analyze",
            json={"binary_name": "thruster_mcu.elf", "hex_sample": "7f454c4602010100"},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["llm_sre_model"] == "qwen3-coder-next-80b"
        assert len(body["functions_recovered"]) >= 3
        assert "hal_pwm_field_drive" in body["decompiled_c_preview"]
