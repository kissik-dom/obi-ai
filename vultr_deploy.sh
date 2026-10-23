#!/usr/bin/env bash
set -euo pipefail

# Kingdom AI OS - Vultr GPU A100 Provisioner & Zero-Downtime Stack Deployer
VULTR_REGION="${VULTR_REGION:-ewr}"
VULTR_PLAN="${VULTR_PLAN:-vcg-a100-1c-8g-40vram}"
VULTR_OS_ID="${VULTR_OS_ID:-1743}"
GITHUB_REPO="${GITHUB_REPO:-YOURNAME/kingdom-ai-os}"
GITHUB_BRANCH="${GITHUB_BRANCH:-main}"

if [[ "${1:-}" == "--provision" ]]; then
  if [[ -z "${VULTR_API_KEY:-}" ]]; then
    echo "ERROR: VULTR_API_KEY is required for --provision" >&2
    exit 1
  fi
  USER_DATA_FILE="$(mktemp)"
  PAYLOAD_FILE="$(mktemp)"
  trap 'rm -f "$USER_DATA_FILE" "$PAYLOAD_FILE"' EXIT
  sed "s|__GITHUB_BRANCH__|${GITHUB_BRANCH}|g" vultr_cloud_init.yaml > "$USER_DATA_FILE"
  USER_DATA_B64="$(base64 -w0 "$USER_DATA_FILE")"
  cat > "$PAYLOAD_FILE" <<EOF
{
  "region": "${VULTR_REGION}",
  "plan": "${VULTR_PLAN}",
  "os_id": ${VULTR_OS_ID},
  "label": "kingdom-ai-os-sovereign",
  "hostname": "kingdom-ai-os",
  "backups": "enabled",
  "user_data": "${USER_DATA_B64}"
}
EOF
  echo "[Vultr] Provisioning ${VULTR_PLAN} in region ${VULTR_REGION} (Ubuntu 24.04 OS ${VULTR_OS_ID})..."
  curl --fail-with-body --silent --show-error --retry 3 --retry-all-errors \
    --connect-timeout 20 --max-time 180 -X POST "https://api.vultr.com/v2/instances" \
    -H "Authorization: Bearer ${VULTR_API_KEY}" \
    -H "Content-Type: application/json" \
    --data-binary "@${PAYLOAD_FILE}"
  echo ""
  exit 0
fi

echo "[Kingdom AI OS] Updating repository (${GITHUB_REPO}) and launching Docker Compose stack on Vultr..."
if [[ ! -f .env ]]; then
  cp .env.example .env
fi

docker compose \
  -f docker-compose.yml \
  -f vultr_security_docker-compose.yml \
  -f vultr_gpu_docker-compose.override.yml \
  up -d --build --remove-orphans

echo "[Kingdom AI OS] Waiting for /healthz..."
for i in {1..30}; do
  if curl -fsS http://127.0.0.1:8000/healthz >/dev/null 2>&1; then
    echo "[Kingdom AI OS] Backend healthy on :8000 and Frontend live on :5173"
    exit 0
  fi
  sleep 2
done

echo "WARNING: /healthz did not respond within 60s; check docker compose logs." >&2
exit 1
