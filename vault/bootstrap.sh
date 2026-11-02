#!/bin/sh
# One-shot Vault bootstrap: initialize on first boot, persist credentials in
# the shared persistent volume, and unseal so the main service is healthy.
set -eu

export VAULT_ADDR="${VAULT_ADDR:-http://vault:8200}"

# Wait until the Vault HTTP API responds (it may still be sealed or
# uninitialized, so `vault status` alone is not a usable readiness check).
i=0
until vault status -format=json 2>/dev/null | grep -q '"initialized"'; do
  i=$((i + 1))
  if [ "$i" -ge 60 ]; then
    echo "vault-init: Vault did not become reachable" >&2
    exit 1
  fi
  sleep 2
done

# Initialize on first boot and keep the unseal key/root token for restarts.
if [ ! -s /vault/file/init.json ]; then
  vault operator init -key-shares=1 -key-threshold=1 -format=json > /vault/file/init.json
fi

UNSEAL_KEY="$(sed -n 's/.*"unseal_keys_b64"[[:space:]]*:[[:space:]]*\["\([^"]*\)".*/\1/p' /vault/file/init.json)"
ROOT_TOKEN="$(sed -n 's/.*"root_token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' /vault/file/init.json)"

# Unseal when needed (fresh boot or restart while sealed).
if vault status -format=json | grep -q '"sealed"[[:space:]]*:[[:space:]]*true'; then
  vault operator unseal "$UNSEAL_KEY" >/dev/null
fi

# Persist the generated root token so downstream services can read it from
# the volume instead of relying on a hardcoded dev token.
printf '%s' "$ROOT_TOKEN" > /vault/file/root_token
echo "vault-init: Vault initialized and unsealed."