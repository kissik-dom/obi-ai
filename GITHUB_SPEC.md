# DOC 10: GITHUB_SPEC.md - Repository Hygiene, CI/CD & Vultr Deployment

## 1. Repository Structure & Branch Workflow

- **Canonical Target Repository**: `YOURNAME/kingdom-ai-os` (or active workspace repository `kissik-dom/obi-ai`)
- **Production & Integration Branches**: `main`, `dev` (and active Arena session branch when running inside Arena Agent Mode)
- **Ignored Runtime Artifacts (`.gitignore`)**:
  - `.env`, `.env.*` (except `.env.example`)
  - `__pycache__/`, `.pytest_cache/`, `.venv/`, `backend/.runtime/`
  - `node_modules/`, `frontend/dist/`
  - `.qdrant/`, `.minio/`, `.vault/`
  - `*.mp4`, `*.zip`, `finished/*`, `requests/*`

## 2. Conventional Commit Standard

- `docs:` Planning specifications (`DOC 1` through `DOC 10`, `ADD_TAB.md`, `ENGINEERING_SPEC.md`)
- `chore:` Infrastructure (`docker-compose.yml`, `vultr_security_docker-compose.yml`, `vultr_gpu_docker-compose.override.yml`, `.env.example`, Vultr scripts)
- `feat:` Backend routers, 12 Sovereign Agents, Hermes Swarm, Sandbox engine, and White UI 24->28 tabs
- `feat(llm):` New `ModelRecord` additions via External Scout A or `new_llm_skill.py`
- `feat(tool):` New `ToolRecord` additions via `new_tool_skill.py`
- `fix:` Automated patches from `bugfix_agent.py`
- `test:` Continuous verification suite (`tests/test_*.py`)

## 3. GitHub Actions Pipelines (`.github/workflows/`)

1. **`.github/workflows/test.yml`**:
   - Triggered on every `push` and `pull_request`.
   - Sets up Python `3.11` and Node `20`.
   - Runs full `pytest tests/` backend verification and `npm run build` (`tsc -b && vite build`) strict TypeScript frontend verification.

2. **`.github/workflows/deploy.yml`**:
   - Triggered on `push` to `main` or manual `workflow_dispatch`.
   - Provisions or updates the Vultr GPU instance (`region: ewr`, `plan: vcg-a100-1c-8g-40vram`, `os_id: 1743` Ubuntu 24.04) via `vultr_deploy.sh` (`VULTR_API_KEY`) and `vultr_cloud_init.yaml` (`GITHUB_REPO`), then runs `docker compose -f docker-compose.yml -f vultr_security_docker-compose.yml -f vultr_gpu_docker-compose.override.yml up -d --build`.
