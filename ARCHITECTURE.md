# DOC 1: ARCHITECTURE.md - Kingdom AI OS Control Plane

## 1. System Overview

Kingdom AI OS is a self-sovereign, multi-modal AI Operating System designed with **24 core control-plane tabs extensible to 28+ tabs** using a single unified grammar across every tab:

`Chat | Agents | Open Tasks | Completed Tasks | Training | Knowledge | Files | Tools | Outputs | Settings`

Every user action or quick request provisions an isolated, fully equipped execution sandbox (`ENABLE_SANDBOX_EQUIP_ALL=true` by default, toggleable via environment flags) backed by vector memory (`Qdrant`), immutable object storage (`MinIO` buckets `s3://kingdom-requests/` and `s3://kingdom-finished/`), hardware-backed secret management (`HashiCorp Vault HSM`), relational task registry (`PostgreSQL 16`), low-latency event queues (`Redis 7` + `Celery Beat`), a `2000 x 5 = 10,000` isolated `trycua/cua` Boat computer-use fleet, and `200 x 5 = 1,000` parallel GPU worker pipelines.

## 2. Control Plane Diagram and Data Flow

```text
+---------------------------------------------------------------------------------------------------+
|                             WHITE UI CONTROL PLANE (Port 5173)                                    |
|  React 18 + Vite 6 + TypeScript Strict + Tailwind 3.4 + Zustand + TanStack Query                  |
|  White BG (#FFFFFF) | Black Text (#0A0A0A) | Magenta / Turquoise / Orange Headers | Gold COPY     |
|  24 Core Tabs -> Extensible to 28 Tabs (+ ADD TAB Skill) | Identical 10-Section Tab Grammar       |
+-------------------------------------------------+-------------------------------------------------+
                                                  | HTTP / JSON / SSE (Relative /api/* Proxy)
                                                  v
+---------------------------------------------------------------------------------------------------+
|                           SECURITY & ZERO-TRUST GATEWAY MIDDLEWARE                                |
|  CrowdSec 100k Behavioral WAF -> ModSecurity CRS 4.2 -> Suricata IDS -> Wazuh SIEM FIM            |
|  Falco eBPF Syscall Monitor -> Tetragon Cilium Enforcement -> Cowrie Honeypot (/admin,/financial) |
|  CompreFace facial_enrolled + FIDO2 WebAuthn + Opt-In VideoKYC (BIPA/GDPR) + Self Allowlist       |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                             FASTAPI BACKEND CORE (Port 8000 /docs)                                |
|  Python 3.11 + Pydantic v2 Validation + SQLAlchemy 2.0 + Lazy Tool Imports + /healthz + /metrics  |
|  24 Tab Routers + Extended 25-28 Routers + Security / KYC / BugFix / Sandbox / Agent Routers      |
+------+---------------+---------------+---------------+---------------+---------------+------------+
       |               |               |               |               |               |
       v               v               v               v               v               v
+-------------+ +-------------+ +-------------+ +-------------+ +-------------+ +-------------------+
| LiteLLM     | | Qdrant      | | MinIO S3    | | Vault HSM   | | PostgreSQL  | | Redis + Celery    |
| Port 4000   | | Port 6333   | | 9000 / 9001 | | Port 8200   | | Port 5432   | | Port 6379 / 5555  |
| 200+ Models | | 768d Cosine | | Atomic Put  | | Transit Key | | kingdom DB  | | Task & Beat Cron  |
| 10 OR Keys  | | 1M Context  | | finished/   | | Zero .env   | | 10 Task     | | Scout 6h / Opt 1d |
| 3 Retries   | | Ingestion   | | requests/   | | Fin Secrets | | States      | | Test 1200s / 10s  |
+------+------+ +-------------+ +-------------+ +-------------+ +-------------+ +---------+---------+
       |                                                                                  |
       +----------------------------------------+-----------------------------------------+
                                                | WireGuard Zero Trust mTLS (No Lateral Movement)
                                                v
+---------------------------------------------------------------------------------------------------+
|                         ISOLATED EXECUTION & SELF-HEALING WORKER PLANE                            |
|  - CUA Fleet (trycua/cua Boat): 2,000 Isolated Ephemeral VMs x 5 Profiles = 10,000 Accounts      |
|  - GPU Worker Fleet (Vultr A100): 200 Workers x 5 Parallel = 1,000 Photoreal Images One Batch     |
|  - Video Pipeline: 600 Clips @ 30s (18,000s) -> 10x Parallel -> FFmpeg + MoviePy + WhisperX MP4   |
|  - 12 Sovereign Agents + Hermes Swarm (ENABLE_HERMES) + OpenTimestamps / IPFS Kubo Audit Trail    |
|  - Observability & Self-Healing: Prometheus (9090) + Grafana (3001) + Loki (3100) + Watchtower    |
+---------------------------------------------------------------------------------------------------+
```

## 3. 24 Core Tabs + 4 Extensible Tabs (28 Total)

| # | Slug | Tab Name | Primary Domain |
|---|---|---|---|
| 1 | `home` | Home / Command Center | Global orchestration, health telemetry, sandbox overview |
| 2 | `llm` | LLM / Models | 200+ model registry, 10-key OpenRouter proxy, Scout A & Optimizer B |
| 3 | `research` | Research | 1M-context whole-website synthesis, academic & patent intelligence |
| 4 | `legal` | Legal | Contract chain-of-thought, DocAssemble LaTeX, Kissi Gazette IPFS liens |
| 5 | `osint` | OSINT | Entity mapping, SpiderFoot, Amass, Sherlock, Recon-ng |
| 6 | `finance` | Finance | Sovereign banking WBRG compliance, Vault HSM, Aave V3 / CCXT |
| 7 | `investments` | Investments | Quantitative portfolio analysis, bilateral treaties, OpenTimestamps |
| 8 | `real_estate` | Real Estate | Property scraping, ARV valuation, OSM+QGIS, DocAssemble escrow |
| 9 | `business` | Business / CRM | Composio 250+ enterprise connectors, pipeline automation |
| 10 | `leads` | Leads | Multi-source lead discovery, Playwright stealth, enrichment |
| 11 | `city` | City / Urban Planning | OSMnx, GeoPandas, QGIS, CityGML, IfcOpenShell BIM, OpenFOAM |
| 12 | `engineering` | Engineering GHIDRA Anti-Gravity | GHIDRA SRE, FreeCAD FEM, OpenSCAD, KiCad, OpenBOM, BPP research |
| 13 | `coding` | Coding / Dev | Qwen3-Coder-Next-80B, OpenHands, SWE-agent, Aider, CI/CD |
| 14 | `web` | Web / Scraping | Scrapy, Playwright, Crawlee, 2,000 CUA Boat browser spaces |
| 15 | `news` | News / Magazines | Multilingual RSS synthesis, blockchain-backed Kissi Gazette |
| 16 | `social` | Social / Marketing | Multimodal UGC campaigns, 2,000x5 Graph API & WAHA omnichannel |
| 17 | `fashion` | Fashion | Garment/jewelry isolation, ethnic skin-tone photoreal lookbooks |
| 18 | `images` | Images / Visual AI | 7-Subagent Director's Cut, Hair/Jewelry/Clothes/BG/Face isolation |
| 19 | `video` | Video / UGC / TV / Movies | MiniMax Hailuo-02, Wan 2.1, LTX 600-clip stitched single MP4 |
| 20 | `music` | Music / Audio Vocal Tuning | GSnap, MAutoPitch, Graillon 2, Spleeter, Demucs v4, RVC, 808 Kit |
| 21 | `agents` | Agents / Communications | 12 Sovereign Agents + Hermes Swarm, Llama 4 Scout 10M comms |
| 22 | `tasks` | Tasks | Unified 10-state task registry, Celery Beat schedules, Flower |
| 23 | `opensource` | Open Source / Apps | 900+ tool catalog (Categories A-K + Composio 250+ connectors) |
| 24 | `security` | Security / Admin | CrowdSec, Wazuh, Suricata, Falco eBPF, Cowrie PDF police export, KYC |
| 25 | `templates` | Templates *(Extensible)* | DocAssemble, LaTeX, OpenBOM, InvenTree, FreeCAD, OpenSCAD |
| 26 | `passport` | Passport / QR *(Extensible)* | CompreFace FIDO2, VideoKYC, OMNIVIDENS seal, WBRG verification |
| 27 | `training` | Training / Knowledge *(Extensible)* | Qdrant 768d ingestion, 1M-token Ling-3.1-Flash corpus builder |
| 28 | `marketplace` | Marketplace / Discovery *(Extensible)* | External Scout A quarantine gate & Internal Optimizer B rankings |

## 4. Docker Compose Topology

### 4.1 Base Stack (`docker-compose.yml`)
- `frontend` (`:5173`): React 18 + Vite 6 white UI control plane
- `backend` (`:8000`): FastAPI application server (`/docs`, `/healthz`, `/metrics`)
- `litellm` (`:4000`): LiteLLM Router proxy with 10 OpenRouter keys (`OPENROUTER_API_KEY_1..10`), `num_retries: 3`, `timeout: 60`
- `qdrant` (`:6333`, `:6334`): Vector store (`768d`, Cosine distance)
- `minio` (`:9000`, `:9001`): S3-compatible object store (`minioadmin` / `minioadmin123`, buckets `kingdom-finished`, `kingdom-requests`)
- `vault` (`:8200`): HashiCorp Vault HSM Transit secret engine
- `postgres` (`:5432`): PostgreSQL 16 (`POSTGRES_DB=kingdom`, `POSTGRES_USER=kingdom`, `POSTGRES_PASSWORD=kingdom123`)
- `redis` (`:6379`): Queue broker & ephemeral cache
- `celery-worker` & `celery-beat` & `flower` (`:5555`): Scheduled self-update, testing, and async batch workers
- `prometheus` (`:9090`), `grafana` (`:3001`), `loki` (`:3100`): Metrics, dashboards, and centralized audit logs
- `watchtower` & `keel`: Zero-downtime container self-healing
- `bugfix-agent` & `testing-agent`: Continuous 10s / `TEST_INTERVAL` self-verification loop

### 4.2 Security Override (`vultr_security_docker-compose.yml`)
- `crowdsec` (`:8080`): 100k collaborative behavioral WAF LAPI
- `wazuh` (`:55000`): SIEM + File Integrity Monitoring (FIM) + XDR
- `suricata`: Host-network IDS/IPS with ET Open ruleset
- `falco`: Privileged eBPF syscall anomaly sensor (`/proc:/host/proc:ro`)
- `tetragon`: Cilium eBPF policy enforcement sensor
- `kubearmor`: LSM + eBPF container confinement
- `wireguard` (`:51820/udp`): Zero Trust mTLS mesh isolating all 2,000 CUA Spaces
- `cowrie` (`:2222`, `:2223`): SSH/HTTP honeypot feeding `/api/security/attempts`
- `compreface` (`:8001`): Self-hosted facial recognition for `facial_enrolled` & VideoKYC

### 4.3 GPU & CUA Fleet Override (`vultr_gpu_docker-compose.override.yml`)
- `backend` & `litellm`: NVIDIA CUDA GPU reservation (`vcg-a100-1c-8g-40vram`, Ubuntu 24.04 `os_id: 1743`, Vultr `ewr`)
- `gpu-image-worker`: 5 replicas x 200 concurrent slots = 1,000 photoreal images per batch
- `gpu-video-worker`: 5 replicas x 10x parallel chunkers for 600-clip 2hr/5hr video stitching
- `cua-driver` & `boat-fleet`: `BOAT_FLEET_SIZE=2000` isolated computer-use sandboxes

### 4.4 Multi-Stage Dockerfile Layering
To prevent dependency bloat and OOM crashes, Docker builds follow strict multi-stage isolation and Python modules use lazy function-scoped imports:
`base -> security -> engineering -> images -> video -> messaging`

## 5. Runtime Turn-Off Flags

Every subsystem defaults to `true` and can be cleanly disabled via `.env` or live Settings API without breaking any tab:
- `ENABLE_SANDBOX_EQUIP_ALL=true`
- `ENABLE_DISCOVERY=true`
- `ENABLE_SANDBOX=true`
- `ENABLE_SECURITY=true`
- `ENABLE_HERMES=true`
- `ENABLE_LLM_ROUTER=true`
- `ENABLE_IMAGE_CONSISTENCY=true`
- `ENABLE_VIDEO_AGENT=true`
- `ENABLE_ENGINEERING=true`
- `ENABLE_VOCAL_TUNING=true`
- `ENABLE_TESTING=true`
- `ENABLE_SELF_UPDATE=true`
- `ENABLE_TAB_BUILDER=true`
- `ENABLE_NEVER_GIVE_UP=true`
