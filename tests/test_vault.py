"""Verify HashiCorp Vault HSM transit seal encryption, decryption, and HMAC tamper rejection."""

import json
import pytest

from backend.core.stores import VAULT_STORE


def test_vault_hsm_encrypt_decrypt_and_tamper_detection() -> None:
    ref = VAULT_STORE.put_secret("test/api_secret", {"token": "sovereign-999", "tier": "hsm"})
    assert ref.startswith("vault:v1:")
    recovered = VAULT_STORE.get_secret("test/api_secret")
    assert recovered == {"token": "sovereign-999", "tier": "hsm"}

    # Tamper with stored MAC and verify integrity rejection
    raw = json.loads(VAULT_STORE.seal_file.read_text(encoding="utf-8"))
    orig_mac = raw["test/api_secret"]["mac"]
    raw["test/api_secret"]["mac"] = "0" * len(orig_mac)
    VAULT_STORE.seal_file.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError):
        VAULT_STORE.get_secret("test/api_secret")
    raw["test/api_secret"]["mac"] = orig_mac
    VAULT_STORE.seal_file.write_text(json.dumps(raw), encoding="utf-8")
