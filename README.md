# Kingdom AI OS (v2.4.0)

Sovereign Multi-Agent AI Operating System featuring **24 Core Tabs extensible to 28+ Tabs**, **205+ Registered LLMs & Multimodal Models** (prioritizing Tier S Huihui `OBLITERATED` models with 10-key OpenRouter + LiteLLM failover), **920 Lazy-Loaded Tools** (620 Open-Source across Categories A-L + 300 Composio Connectors), **12 Sovereign Agents + 14 Hermes Swarm Specialists**, **Equipped Per-Task Sandboxes**, and an **8-Layer Zero-Trust Security Perimeter** ready for **Vultr GPU Cloud**.

## Architecture Highlights

- **Uniform 10-Section Tab Grammar (Tabs 1 -> 28+)**: Every tab exposes the exact same 10 sections (`Chat`, `Agents`, `Open Tasks`, `Completed Tasks`, `Training`, `Knowledge`, `Files`, `Tools`, `Outputs`, `Settings`).
- **205+ Sovereign Model Vault & Deterministic Router**: Scores every eligible model via `score = task_fit + benchmark_quality + tool_use_quality + context_fit + modality_fit + reliability + privacy_fit + local_preference + latency_fit - cost - risk - resource` after applying 7 hard filters.
- **920 Lazy-Loaded Tools**: Categories `A` through `K` (`50+` open-source tools per category) + `L` (`56` sovereign infra tools) + `M` (`300` Composio actions), imported lazily inside function scope to guarantee zero startup bloat or OOM.
- **Equipped Isolated Sandboxes**: Every task provisions an isolated sandbox (`ENABLE_SANDBOX_EQUIP_ALL=true` by default) wired to Qdrant `768d` Cosine memory, MinIO atomic S3 buckets (`s3://kingdom-requests/` and `s3://kingdom-finished/`), HashiCorp Vault HSM transit policies, PostgreSQL 16 (SQLAlchemy 2.0 + Alembic), Redis 7 queues, CUA Boat cloud spaces (`2,000 x 5 = 10,000` official Business Graph accounts), and GPU worker pools (`200 x 5 = 1,000` parallel renders).
- **8-Layer Zero-Trust Security & Legal BIPA/GDPR VideoKYC**: CrowdSec WAF, Wazuh SIEM FIM, Suricata IDS, Falco + Tetragon eBPF, Vault HSM (`10 req/sec` financial rate limit, zero private keys in `.env`), WireGuard Zero Trust, Cowrie decoy honeypot (`/admin`, `/financial`, `/photos` -> ReportLab police PDF export), and explicit-consent CompreFace FIDO2 VideoKYC with `X-Kingdom-Internal` owner allowlist.

## Mandatory Planning Specifications

1. `ARCHITECTURE.md`
2. `LLM_REGISTRY.md`
3. `TOOL_REGISTRY.md`
4. `TAB_SPEC.md` (+ `ADD_TAB.md`)
5. `SANDBOX_SPEC.md`
6. `SECURITY_SPEC.md`
7. `AGENT_SWARM_SPEC.md`
8. `STACK_DECISION.md` (+ `ENGINEERING_SPEC.md`)
9. `TESTING_SPEC.md`
10. `GITHUB_SPEC.md` (+ `CONNECT_GITHUB_TO_VULTR.md`)

## Quick Start (Local Development)

### 1. Backend (`:8000` & Swagger `/docs`)
```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
backend/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend (`:5173` Sovereign White Theme)
```bash
cd frontend
npm install
npm run dev
```

### 3. Run Verification Suite (`pytest`)
```bash
backend/.venv/bin/pytest tests/ -v
```

### 4. Deploy to Vultr GPU Cloud
See `CONNECT_GITHUB_TO_VULTR.md`, `vultr_cloud_init.yaml`, and `./vultr_deploy.sh`.
