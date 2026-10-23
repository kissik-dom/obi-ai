# DOC 7: AGENT_SWARM_SPEC.md - 12 Sovereign Agents + Hermes Extensions Swarm

## 1. The 12 Sovereign Agents (`backend/agents/`)

Every agent is modular, typed with Pydantic v2 outputs, equipped with lazy tool loading, and individually toggleable via environment flags.

| # | Module | Agent Name | Primary LLMs | Core Tools & Responsibility | Turn-Off Flag |
|---:|---|---|---|---|---|
| 1 | `bugfix_agent.py` | **BugFix Agent** | `qwen3-coder-next-80b`, `deepseek-v4-flash` | OpenHands, SWE-agent, Aider, Watchtower, Keel, Prometheus. Checks health every **10s**; auto-diagnoses, patches, and restarts unhealthy services (`POST /api/bugfix/trigger`, `GET /api/bugfix/status`). | `ENABLE_SELF_UPDATE` |
| 2 | `testing_agent.py` | **Testing Agent** | `agents-a1-35b`, `huihui-qwen3.6-35b-a3b` | Pytest, Playwright, HTTPX, Loki. Continuously verifies all 24->28 tabs, stores, Vault, CUA isolation, and honeypot every `TEST_INTERVAL` (`1200s` default or `1s` high-frequency bank mode). | `ENABLE_TESTING` |
| 3 | `external_scout_agent.py` | **External Scout Agent A** | `ling-3.1-flash-1m`, `huihui-qwen3.6-35b-a3b` | Runs every **6 hours** via Celery Beat. Scans HuggingFace Hub (`abliterated`/`uncensored`), OpenRouter `/api/v1/models`, GitHub Trending (`huihui-ai`), and Arxiv; benchmarks in `quarantine -> staging -> production` and dispatches breakdown digest. | `ENABLE_DISCOVERY` |
| 4 | `internal_optimizer_agent.py` | **Internal Optimizer Agent B** | `deepseek-v4-flash`, `qwen3.8-27b-2.19m` | Runs **daily** via Celery Beat. Analyzes Postgres task registry success rate, p95 latency, token cost, and quality score per tab; recommends priority routing promotions. | `ENABLE_SELF_UPDATE` |
| 5 | `cua_fleet_agent.py` | **CUA Fleet Agent** | `moe-0.8b-2e`, `ornith-1.0-2b`, `granite-4.1-3b` | Orchestrates **2,000 isolated `trycua/cua` Boat VMs x 5 profiles = 10,000 accounts** using official Business Graph APIs, staggered rate budgets, and WireGuard Zero Trust isolation. | `ENABLE_SANDBOX` |
| 6 | `gpu_worker_agent.py` | **GPU Worker Agent** | `gemma-4-it-qat-12b`, `flux-1-dev-12b` | Coordinates **200 GPU worker slots x 5 replicas = 1,000 parallel photoreal images** delivered as one unified ZIP + PDF contact sheet batch. | `ENABLE_IMAGE_CONSISTENCY` |
| 7 | `video_stitching_agent.py` | **Video Stitching Agent** | `minimax-hailuo-02`, `wan-2.1-14b`, `ltx-video-13b`, `qwythos-9b-classic` | Splits long-form video requests into **600 clips @ 30s (`18,000s` / 5h -> `10x` parallel)** and stitches via `FFmpeg` + `MoviePy` + `WhisperX` word-level audio sync into a single `final_video.mp4`. | `ENABLE_VIDEO_AGENT` |
| 8 | `image_consistency_agent.py` | **Image Consistency Director** | `gemma-4-it-qat-12b`, `gemma-4-e2b-5b`, `qwen3.8-vision-28b` | **7 Parallel Subagents (Director's Cut)**: (1) 7-Angle Selection (`0,15,30,45,90,135,180`), (2) **Hair Only** (`SAM2`+`DINOv2`+`BiRefNet`, zero skin bleed), (3) **Jewelry Only** (`GroundingDINO`+`SAM2`, metal/carat/stone filter), (4) **Clothes Only**, (5) **Background Only** (`BiRefNet`+`LaMa`), (6) **Face Only Biometric Preservation** (`InstantID`+`CompreFace`), (7) Photoreal Rendering. | `ENABLE_IMAGE_CONSISTENCY` |
| 9 | `security_honeypot_agent.py` | **Security Honeypot Agent** | `cyberstrike-offsec-35b`, `glm-5.3-flash-fp8` | Manages CrowdSec WAF, Wazuh FIM, Falco/Tetragon eBPF telemetry, Cowrie decoy traps (`/admin`, `/financial`, `/photos`), JA3 bot detection, and Law-Enforcement PDF export. | `ENABLE_SECURITY` |
| 10 | `passport_agent.py` | **Passport OMNIVIDENS & Legal Agent** | `qwen3.8-27b-2.19m`, `gemini-4-plus-400b` | Issues OMNIVIDENS QR sovereign seals, FIDO2 + VideoKYC credentials, WBRG compliant dual-license verification notices, and Kissi Gazette OpenTimestamps/IPFS liens. | `ENABLE_SECURITY` |
| 11 | `engineering_agent.py` | **Engineering GHIDRA Anti-Gravity Agent** | `qwen3-coder-next-80b`, `gemini-4-argon-400b` | Runs headless GHIDRA 11.2 SRE P-code analysis, Binary Ninja/Radare2/angr triage, FreeCAD/OpenSCAD/CadQuery 3D models, KiCad HV PCBs, OpenFOAM/Elmer FEM, OpenBOM/InvenTree M3/M4 screw torque BOMs, and NASA BPP / Woodward Mach-Effect simulations. | `ENABLE_ENGINEERING` |
| 12 | `vocal_tuning_agent.py` | **Vocal Tuning Agent** | `gemma-4-e2b-5b`, `qwen3.8-27b-2.19m` | Executes `Demucs v4` / `Spleeter` 2-4-5 stem separation -> `GSnap` + `MAutoPitch` + `Graillon 2` + `PitchProof` pitch chain -> `RVC v2` / `F5-TTS` timbre synthesis + **Free 808 Kit (94 808s)** & `MusicGen` mastering. | `ENABLE_VOCAL_TUNING` |

## 2. Hermes Agents & Extensions Swarm (`backend/agents/skills/hermes/`)

Kingdom AI OS embeds the full **Hermes Agents & Extensions** stack alongside the Obliteratus multi-provider cascade:
- `hermes_agent.py`: 14-specialist Hermes swarm router (`general`, `researcher`, `coder`, `code_fixer`, `repo_scout`, `ecosystem_architect`, `integrator`, `analyst`, `document`, `predictor`, `editor`, `ui_designer`, `marketer`, plus `director`) backed by `Obliteratus-Hermes-3-70B` and `Llama-4-Scout-10M`.
- `hermes_library.py`: Persistent Hermes skill & episodic memory adapter synced to Qdrant (`768d`) and MinIO.
- `hermes_tool_use.py`: Deterministic `<tool_call>` XML/JSON function-calling parser & sandbox dispatcher across all 920 registered tools.
- **Complete Turn-Off**: Setting `ENABLE_HERMES=false` cleanly disables all Hermes swarm routing and extensions without affecting the 12 core Sovereign Agents.

## 3. Code-Generating Meta-Skills (`backend/agents/skills/`)

- `new_tab_skill.py`: Programmatically scaffolds a new tab (`frontend/src/pages/<Tab>.tsx` + `backend/api/routers/<tab>.py` + registry metadata) with identical 10-section grammar.
- `new_llm_skill.py`: Validates and registers a new `ModelRecord` into the live router and `litellm_proxy_config.yaml`.
- `new_tool_skill.py`: Validates and registers a new lazy-imported `ToolRecord` in Categories A-M.
- `new_agent_skill.py`: Scaffolds and registers a new domain agent with turn-off flag support.
