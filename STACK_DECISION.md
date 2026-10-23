# DOC 8: STACK_DECISION.md - Locked Sovereign Stack & Anti-Wonky Rules

## 1. Frontend Stack (`frontend/` - Port `5173`)

- **Runtime & Build**: Node `20+`, React `18.3`, Vite `6`, TypeScript `5.6` with:
  - `"strict": true`
  - `"noImplicitAny": true`
  - `"strictNullChecks": true`
  - **Zero `any` types anywhere in `frontend/src/`**
- **Styling & Design System**:
  - Tailwind CSS `3.4` + Radix/shadcn-pattern primitives + `lucide-react` icons
  - **White UI Mandate**: Crisp white background (`#FFFFFF`), deep black text (`#0A0A0A`), **Magenta (`#D90077`)**, **Turquoise (`#0097A7`)**, and **Orange (`#EA580C`)** section/chapter headers, **Gold (`#D4AF37` / `#F59E0B`) `COPY` buttons**, `11px` monospace code (`font-mono text-[11px]`), sans-serif body (`Inter`), chapter header bar, numbered page footer, and **zero em dashes** (commas and colons only).
- **State & Networking**:
  - `zustand` for UI/tab/flag state
  - `@tanstack/react-query` for server cache, mutations, and live polling
  - URL/Router synchronization across all 24->28 tabs
  - Relative `/api/*` requests proxied by Vite (`0.0.0.0:5173`, `allowedHosts: true`) to FastAPI (`:8000`)

### Why FastAPI + Postgres/Qdrant/MinIO Instead of Convex by Default?
Kingdom AI OS is self-sovereign on Vultr GPU infrastructure (`vcg-a100-1c-8g-40vram`, Ubuntu 24.04 `os_id: 1743`, `ewr`) requiring local Vault HSM secret custody, WireGuard Zero Trust isolation, and terabyte-scale MinIO/Qdrant storage. PostgreSQL + FastAPI is the single source of truth; an optional stateless **Convex webhook sync adapter** (`backend/core/convex_adapter.py`) is provided for teams who want external edge replication without splitting state authority.

## 2. Backend Stack (`backend/` - Port `8000`)

- **Framework**: Python `3.11`, FastAPI, Uvicorn, **Pydantic v2 (`BaseModel`, `ConfigDict`, `@field_validator`)** on every request and response (zero unvalidated raw dicts).
- **Persistence & Messaging**:
  - `sqlalchemy==2.0.27` + `alembic==1.13.1` (PostgreSQL `5432` `kingdom`/`kingdom123` with automatic local SQLite WAL fallback when running outside Docker)
  - `qdrant-client==1.7.3` (`6333`, `768d` Cosine embeddings, deterministic local vector store fallback)
  - `minio==7.2.0` (`9000`/`9001`, **`minio-py` exclusively, never `boto3`**, atomic temp-then-rename object writes)
  - `hvac==2.1.0` (HashiCorp Vault `8200` HSM Transit client with local AES/HMAC sealed vault fallback)
  - `redis==5.0.1` + `celery==5.3.6` (`6379` task broker & Celery Beat cron)
  - `litellm` + `httpx` + `openai` (10 OpenRouter keys `OPENROUTER_API_KEY_1..10`, `num_retries=3`, `timeout=60`)

## 3. Pitfalls Eliminated by Design

| Pitfall | Root Cause | Kingdom AI OS Fix |
|---|---|---|
| Event-loop stalls | Mixing sync CPU code inside `async def` | All LLM/HTTP calls are `async def`; CPU-bound CAD/GHIDRA/audio tasks run via `asyncio.to_thread` / `run_in_executor`. |
| Startup OOM / import crashes | Top-level imports of `torch`, `ghidra_bridge`, `cadquery`, `diffusers` | Strict **lazy imports inside worker functions** + multi-stage Docker targets. |
| Schema drift | Mixing Pydantic v1/v2 or untyped TS `any` | 100% Pydantic v2 `BaseModel` + TypeScript `strict: true` (`tsc --noEmit` verified). |
| Storage corruption | Partial S3 uploads or mixing `boto3` with `minio-py` | `minio==7.2.0` only; atomic write-to-`.tmp` then rename/copy. |
| UI visual drift | Different layouts per tab or inline style soup | Single `<UnifiedTabWorkspace />` grammar shared by all 24->28 tabs using Tailwind utility tokens. |
