# Kingdom AI OS — Agent Swarm Specification

## 12 primary agents

| Agent | File | Responsibility |
| --- | --- | --- |
| BugFix | `backend/agents/bugfix.py` | reproduce, isolate, patch, regression proof |
| Testing | `backend/agents/testing.py` | contract/unit/integration/security tests |
| External Scout | `backend/agents/external_scout.py` | OSINT/news/scraping/public sources |
| Internal Optimizer | `backend/agents/internal_optimizer.py` | capacity, latency, cache, spend |
| CUA Fleet | `backend/agents/cua_fleet.py` | five isolated computer-use spaces |
| GPU Worker | `backend/agents/gpu_worker.py` | five VRAM inference/GPU spaces |
| Video Stitching | `backend/agents/video_stitching.py` | FFmpeg edit, stitch, delivery |
| Image Consistency | `backend/agents/image_consistency.py` | style/palette/character consistency |
| Security Honeypot | `backend/agents/security_honeypot.py` | Cowrie/Suricata/Falco/Tetragon triage |
| Passport/OMNIVIDENS | `backend/agents/passport_omnividens.py` | KYC, liveness, synthetic/OOD detection |
| Engineering GHIDRA | `backend/agents/engineering_ghidra.py` | GHIDRA/FreeCAD/OpenSCAD/Blender/KiCad |
| Vocal Tuning | `backend/agents/vocal_tuning.py` | GSnap/MAutoPitch/Spleeter/Demucs/RVC |

## Hermes gateway

`backend/agents/skills/hermes.py` exposes the Obliteratus Hermes gateway with
14 Hermes skills: router, research, scout, coder, legal, finance, OSINT, image,
video, audio, security, CUA, engineering, and comms.

Rules:

- Router selects a Hermes skill before fanout.
- LiteLLM Router applies `num_retries=3`, `request_timeout=60`, and fallback chains.
- If the primary agent returns an error, the failure is written to the finished
  folder as evidence; no silent retry beyond configured fallback.
- Agents are launched inside the task's sandbox; no agent shares an untrusted FS.
