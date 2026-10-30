# Kingdom AI OS — Stack Decision

## Frontend

| Concern | Decision |
| --- | --- |
| Framework | React 18 |
| Build | Vite |
| Language | TypeScript strict (`"strict": true`, no `any`) |
| Styling | Tailwind CSS (Vite plugin) + shadcn/ui primitives |
| Server state | TanStack Query |
| Client state | Zustand |
| Theme | White background, black text, magenta/turquoise/orange headers, gold copy buttons, mono 11px code, sans body |
| Port | 5173 |

## Backend

| Concern | Decision |
| --- | --- |
| Framework | FastAPI |
| Models | Pydantic v2 `BaseModel` |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Async workers | Celery |
| Broker/Result | Redis 6379 |
| LLM proxy | LiteLLM Router config with OpenRouter x10 keys, fallbacks, num_retries=3, timeout=60 |
| Port | 8000 |

## Infrastructure

| Concern | Decision |
| --- | --- |
| Vector DB | Qdrant 6333 |
| Object store | MinIO 9000/9001 |
| Secrets | Vault 8200 |
| System of record | Postgres 5432 |
| Queue/cache | Redis 6379 |
| Computer-use | CUA Fleet 2000×5 |
| GPU jobs | GPU Workers 200×5 |
| Deployment | Docker Compose on Vultr VM |
| Security | CrowdSec, Wazuh, Suricata, Falco, Tetragon, Vault HSM, WireGuard, Cowrie, CompreFace |

## Why

- React/Vite keeps frontend local-first and fast; Zustand/TanStack Query separate
  server cache from UI state.
- FastAPI/Pydantic v2 gives strict request contracts that map 1:1 to frontend types.
- LiteLLM Router gives one OpenAI-compatible surface with automatic multi-key
  failover, no code-level fallback logic in each tab.
- Docker Compose keeps every service explicit, healthchecked, and reproducible on Vultr.
