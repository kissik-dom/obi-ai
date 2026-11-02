# Kingdom AI OS — Testing Specification

## Continuous test loop

- `testing_agent.py` runs with `TEST_INTERVAL = 1200` seconds.
- Celery beat schedules `kingdom.testing_agent.run` every 1200 seconds.
- Every tab has a grammar probe every 300 seconds.

## `test_all.py` covers

1. All 10 mandatory planning documents exist.
2. Backend mounts 24 routers with identical grammar endpoints.
3. LiteLLM config has 200+ models, 10 OpenRouter keys, fallback mapping,
   `num_retries=3`, `request_timeout=60`.
4. Docker Compose has healthchecks for Qdrant, MinIO, Vault, Postgres, Redis,
   frontend, backend, CUA, GPU, and the security plane.
5. Frontend exports 24 tab components with the same grammar order.
6. Optional live checks (only when `KINGDOM_TEST_LIVE=1`):
   - Qdrant 6333
   - MinIO 9000
   - Vault 8200
   - Postgres 5432
   - Redis 6379
   - GPU worker 200
   - CUA isolation ports 2000-2004
   - security honeypot 2222
   - financial vault role
   - GHIDRA/FreeCAD sandbox flags
   - vocal tuning tool flags

## Definition of done

- `python3 test_all.py` exits zero on a clean checkout.
- `python3 -m py_compile` passes for backend and agents.
- Live checks are not allowed to fail a deployment when their service flag is 0.
