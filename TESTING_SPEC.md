# DOC 9: TESTING_SPEC.md - Bank-Grade Continuous Verification & Self-Update Gate

## 1. Continuous Runtime Verification (`backend/agents/testing_agent.py`)

`testing_agent.py` runs in a dedicated self-healing daemon container controlled by `TEST_INTERVAL` (`1200` seconds = 3x/hour default, or `1` second for continuous high-frequency verification):
1. Probes `/healthz` (`healthy` | `degraded` | `offline`), `/metrics`, `/docs`, `/api/security/attempts`, `/api/kyc/status`, `/api/bugfix/status`, and all 24->28 tab grammar endpoints.
2. Persists verification evidence into `s3://kingdom-finished/system-tests/evidence/`.
3. On any 5xx or degraded subsystem, immediately POSTs failure diagnostics to `POST /api/bugfix/trigger`, invoking `bugfix_agent.py` (OpenHands / SWE-agent / Aider + Watchtower/Keel auto-recovery).

## 2. Comprehensive Automated Pytest Suite (`tests/`)

All tests live in a dedicated `tests/` layer separated from application runtime code and execute with safe synthetic prompts:

| Test File | Verification Scope |
|---|---|
| `tests/test_all.py` | End-to-end verification of `/healthz`, `/metrics`, all **24 core tabs + 4 extensible tabs**, all 10 grammar routes (`/chat`, `/agents`, `/open-tasks`, `/completed-tasks`, `/training`, `/knowledge`, `/files`, `/tools`, `/outputs`, `/settings`), Quick Request, Finished Folder, and `+ ADD TAB` skill. |
| `tests/test_llm_registry.py` | Verifies **205+ `ModelRecord`s**, Tier S `OBLITERATED` priority ordering, hard filters, ranking formula, domain overrides (Image, Video, Research, OSINT, Legal, Engineering), and 10-key OpenRouter LiteLLM config (`num_retries=3`, `timeout=60`). |
| `tests/test_tool_registry.py` | Verifies **620+ open-source tools** (`>=50` in each of Categories A-K) + **300 Composio actions = 920 total tools**, and lazy-import execution safety. |
| `tests/test_qdrant.py` | Verifies `768d` Cosine upsert, similarity search, and 1M-token Training Tab document ingestion. |
| `tests/test_minio.py` | Verifies `s3://kingdom-requests/` and `s3://kingdom-finished/` atomic temp-then-rename writes, `summary.md`, `request.json`, `response.json`, `artifacts/`, `evidence/`, and `audit.json`. |
| `tests/test_vault.py` & `tests/test_financial_vault.py` | Verifies Vault HSM secret sealing (zero `.env` private key leakage), mTLS metadata, `10 req/sec` rate-limit enforcement, and mandatory opt-in VideoKYC BIPA/GDPR gate. |
| `tests/test_postgres.py` | Verifies transactional CRUD across all 10 task states (`queued`, `running`, `waiting`, `approval_required`, `blocked`, `completed`, `failed`, `cancelled`, `scheduled`, `recurring`) and idempotency keys. |
| `tests/test_redis.py` | Verifies task queue publish/consume and Celery Beat schedule registration. |
| `tests/test_gpu_workers.py` & `tests/test_1000_pics.py` | Verifies `200 x 5 = 1,000` safe photoreal batch planner (`gemma-4-it-qat-12b`) + 7-Subagent Director's Cut isolation (`Hair Only`, `Jewelry Only`, `Clothes Only`, `Background Only`, `Face Only Biometric`) producing one unified batch manifest. |
| `tests/test_2hr_video.py` | Verifies `600 clips @ 30s = 18,000s` (`10x` parallel) chunk planner + `FFmpeg`/`MoviePy`/`WhisperX` word-level stitcher outputting one unified `final_video.mp4` manifest. |
| `tests/test_cua_isolation.py` | Verifies `2,000` CUA Boat Spaces have isolated WireGuard `/32` network policies (zero lateral movement between Space A and Space B) and Falco eBPF syscall confinement. |
| `tests/test_security_honeypot.py` | Verifies Cowrie decoy logging (`IP`, `ASN`, `GeoIP`, `JA3`, `WiFi SSID`, `Vultr EWR`, server-side session recording), `X-Kingdom-Internal` owner allowlist, and Law-Enforcement PDF export (`/api/security/audit/export`). |
| `tests/test_ghidra.py` & `tests/test_freecad.py` | Verifies headless GHIDRA P-code analyzer adapter + FreeCAD/OpenSCAD parametric M3/M4 fastener CAD + OpenBOM/InvenTree torque & Octopart BOM output. |
| `tests/test_vocal_tuning.py` | Verifies `Demucs`/`Spleeter` stem separation + `GSnap`/`MAutoPitch`/`Graillon 2`/`PitchProof`/`RVC` vocal tuning chain + Free 808 Kit (94 808s). |

## 3. Self-Update Quarantine Gate

When **External Scout Agent A** (every 6h) discovers a candidate model on HuggingFace, OpenRouter, GitHub Trending, or Arxiv:
1. Candidate enters `maturity="quarantine"`.
2. Automated benchmark runs `pytest tests/test_llm_registry.py`.
3. Passing models promote `quarantine -> staging -> production` and emit a structured breakdown report; failing candidates remain isolated in `quarantine`.
