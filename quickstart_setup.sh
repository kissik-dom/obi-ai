#!/usr/bin/env bash
set -euo pipefail

# Kingdom AI OS - Zero-Vultr-Key Universal Setup & Secret Generator
# Works on: Mac, Linux, Windows WSL2, Vultr Web-UI VPS/GPU, RunPod, Hetzner, DigitalOcean, AWS
# Requires NO VULTR_API_KEY!

echo "[Kingdom AI OS] Initializing .env and generating cryptographic internal secrets..."

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

rand_hex() {
  python3 -c "import secrets; print(secrets.token_hex($1))"
}

INTERNAL_SEC="$(rand_hex 16)"
LITELLM_SEC="sk-kingdom-$(rand_hex 12)"
PG_PASS="$(rand_hex 12)"
MINIO_PASS="$(rand_hex 12)"
VAULT_TOK="hvs.$(rand_hex 16)"
LISTMONK_PASS="$(rand_hex 10)"

python3 - <<PY
from pathlib import Path

env_path = Path(".env")
text = env_path.read_text(encoding="utf-8")

replacements = {
    "KINGDOM_INTERNAL_SECRET=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4": f"KINGDOM_INTERNAL_SECRET=${INTERNAL_SEC}",
    "LITELLM_MASTER_KEY=sk-kingdom-litellm-master": f"LITELLM_MASTER_KEY=${LITELLM_SEC}",
    "POSTGRES_PASSWORD=kingdom123": f"POSTGRES_PASSWORD=${PG_PASS}",
    "DATABASE_URL=postgresql+psycopg://kingdom:kingdom123@postgres:5432/kingdom": f"DATABASE_URL=postgresql+psycopg://kingdom:${PG_PASS}@postgres:5432/kingdom",
    "MINIO_ROOT_PASSWORD=minioadmin123": f"MINIO_ROOT_PASSWORD=${MINIO_PASS}",
    "VAULT_TOKEN=root": f"VAULT_TOKEN=${VAULT_TOK}",
    "LISTMONK_ADMIN_PASS=kingdom123": f"LISTMONK_ADMIN_PASS=${LISTMONK_PASS}",
}
for old, new in replacements.items():
    text = text.replace(old, new)

env_path.write_text(text, encoding="utf-8")
PY

echo "[Kingdom AI OS] Internal secrets generated in .env (gitignored)."
echo "  -> Optional: edit .env and set OPENROUTER_API_KEY_1 (and OPENROUTER_API_KEY) for live cloud LLMs."

if [[ "${1:-}" == "--env-only" ]]; then
  echo "[Kingdom AI OS] --env-only complete."
  exit 0
fi

COMPOSE=()
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1 && docker-compose version >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
fi

if ((${#COMPOSE[@]})); then
  if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1; then
    echo "[Kingdom AI OS] NVIDIA GPU detected -> launching Full Base + Security + GPU Stack..."
    "${COMPOSE[@]}" \
      -f docker-compose.yml \
      -f vultr_security_docker-compose.yml \
      -f vultr_gpu_docker-compose.override.yml \
      up -d --build --remove-orphans
  else
    echo "[Kingdom AI OS] CPU/Standard host detected (no GPU required) -> launching Base Sovereign Stack..."
    "${COMPOSE[@]}" -f docker-compose.yml up -d --build --remove-orphans
  fi
  echo "[Kingdom AI OS] API Live at http://localhost:8000 and Swagger Docs at http://localhost:8000/docs"
else
  echo "[Kingdom AI OS] Docker not detected -> launching Local Python API-Only Mode..."
  python3 -m venv backend/.venv
  backend/.venv/bin/pip install -r backend/requirements.txt
  backend/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
fi
