#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
if [ -e "$ENV_FILE" ]; then
  echo "Refusing to overwrite existing .env. Back it up and remove it intentionally before regenerating." >&2
  exit 2
fi
if ! command -v openssl >/dev/null 2>&1; then
  echo "OpenSSL is required to generate secrets." >&2
  exit 2
fi
secret() { openssl rand -hex 32; }
{
  printf 'APP_ENV=development\n'
  printf 'APP_NAME=Kingdom AI OS API\n'
  printf 'API_PREFIX=/api/v1\n'
  printf 'CORS_ORIGINS=http://localhost:5173\n'
  printf 'BACKEND_PORT=8000\nFRONTEND_PORT=5173\n'
  printf 'POSTGRES_DB=kingdom_ai\nPOSTGRES_USER=kingdom_app\nPOSTGRES_PASSWORD=%s\n' "$(secret)"
  printf 'QDRANT_API_KEY=%s\n' "$(secret)"
  printf 'MINIO_ROOT_USER=kingdom%s\n' "$(openssl rand -hex 8)"
  printf 'MINIO_ROOT_PASSWORD=%s\n' "$(secret)"
  printf 'LITELLM_MASTER_KEY=sk-%s\n' "$(secret)"
  printf 'KINGDOM_INTERNAL_SECRET=%s\n' "$(secret)"
  printf 'FIREWORKS_API_KEY=\nOPENROUTER_API_KEY=\n'
} > "$ENV_FILE"
chmod 600 "$ENV_FILE"
echo "Created $ENV_FILE with restrictive permissions. Provider keys are blank and must be added locally; do not commit this file."
