#!/usr/bin/env bash
set -euo pipefail

# Kingdom AI OS Vultr deploy.
# Configures a fresh Vultr Ubuntu VM with cloud-init, uploads compose files,
# boots frontend/backend/data planes, then security and optional GPU profiles.

VULTR_IP="${VULTR_IP:?set VULTR_IP}"
SSH_KEY="${SSH_KEY:-~/.ssh/id_ed25519}"
DOMAIN="${DOMAIN:-kingdom.example.com}"

ssh -i "$SSH_KEY" "root@${VULTR_IP}" "mkdir -p /opt/kingdom/vultr/suricata"

scp -i "$SSH_KEY" docker-compose.yml vultr_gpu_docker-compose.override.yml vultr_cloud_init.yaml "root@${VULTR_IP}:/opt/kingdom/"

ssh -i "$SSH_KEY" "root@${VULTR_IP}" bash -s <<'REMOTE'
set -euo pipefail
cd /opt/kingdom
test -f .env || cp .env.example .env

# Data/application control plane first.
docker compose -f docker-compose.yml up -d --remove-orphans

# Security plane second; all services carry healthchecks and restart policies.
if [ "${ENABLE_SECURITY_PROFILE:-1}" = "1" ]; then
  docker compose -f docker-compose.yml --profile security up -d --remove-orphans
fi

# GPU fleet only on GPU-enabled Vultr instances.
if lspci 2>/dev/null | grep -qi nvidia && [ "${ENABLE_GPU_PROFILE:-0}" = "1" ]; then
  docker compose -f docker-compose.yml -f vultr_gpu_docker-compose.override.yml --profile gpu up -d
fi

echo "Waiting for healthchecks..."
sleep 40
docker compose -f docker-compose.yml ps

for url in "http://127.0.0.1:8000/healthz" "http://127.0.0.1:5173"; do
  curl -fsS --retry 5 --retry-delay 5 "$url" >/dev/null
done
echo "Kingdom AI OS is healthy on ${DOMAIN}"
REMOTE
