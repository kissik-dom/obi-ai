# Kingdom AI OS

Private 24-tab sovereign AI operating system. This is the full system replacement
for the previous Next.js app.

- Backend: FastAPI + Pydantic v2 + SQLAlchemy + Alembic + Celery + Redis
- Frontend: React 18 + Vite + TypeScript strict + Tailwind + shadcn/ui + Zustand + TanStack Query
- LLM plane: LiteLLM Router proxy, 10 OpenRouter keys, fallback mapping, `num_retries=3`, `timeout=60`
- Infrastructure: Docker Compose with Qdrant 6333, MinIO 9000/9001, Vault 8200, Postgres 5432, Redis 6379, CUA Fleet 2000×5, GPU Workers 200×5, security plane

## Quickstart

```bash
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml -f vultr_security_docker-compose.yml up -d
# GPU instances only
docker compose -f docker-compose.yml -f vultr_gpu_docker-compose.override.yml --profile gpu up -d
python3 test_all.py
```

Frontend: http://localhost:5173  
Backend: http://localhost:8000/docs  
Health: http://localhost:8000/healthz

## Planning documents

All ten mandatory planning documents live in [`docs/`](./docs):

1. `ARCHITECTURE.md`
2. `LLM_REGISTRY.md`
3. `TOOL_REGISTRY.md`
4. `TAB_SPEC.md`
5. `SANDBOX_SPEC.md`
6. `SECURITY_SPEC.md`
7. `AGENT_SWARM_SPEC.md`
8. `STACK_DECISION.md`
9. `TESTING_SPEC.md`
10. `GITHUB_SPEC.md`