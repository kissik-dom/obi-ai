# DOC 5: SANDBOX_SPEC.md - Every Task Creates a New Equipped Sandbox

## 1. Core Invariant

**Every Task Creates a New Sandbox Equipped With Everything Unless Turned Off (`ENABLE_SANDBOX_EQUIP_ALL=true`).**

Whenever a task is created from any of the 24->28 tabs or via the **Quick Request** button:
1. A unique `sandbox_id` (`sbx-<uuid>`) and idempotency key (`idem-<sha256>`) are allocated.
2. Unless disabled by feature flags, the sandbox is automatically equipped with:
   - **Vector Memory**: Dedicated Qdrant namespace (`768d` Cosine embeddings + `Ling-3.1-Flash` 1M-token ingestion).
   - **Object Buckets**: Atomic MinIO paths in `s3://kingdom-requests/{sandbox_id}/` and `s3://kingdom-finished/{sandbox_id}/`.
   - **Secret Transit**: Ephemeral scoped token in HashiCorp Vault HSM (`:8200`), zero plaintext keys in `.env`.
   - **Relational State**: PostgreSQL `kingdom` task row tracking all 10 lifecycle states (`queued`, `running`, `waiting`, `approval_required`, `blocked`, `completed`, `failed`, `cancelled`, `scheduled`, `recurring`).
   - **Queue & Workers**: Redis `:6379` dispatch channel + access to `2,000` isolated CUA Boat Spaces and `200 x 5` GPU workers.
   - **Tool & Agent Kit**: Full 920-tool lazy-import registry (Categories A-M), 205-model LiteLLM router, 12 Sovereign Agents, and Hermes Swarm.

## 2. Requests Folder (`s3://kingdom-requests/`)

Clicking **Quick Request** (or submitting any tab task) creates a `quick` or domain task in `s3://kingdom-requests/{sandbox_id}/` and transitions cleanly through `queued -> running -> completed`:

```text
s3://kingdom-requests/{sandbox_id}/
├── request.json       # Validated Pydantic payload, tab, model, refs, isolation rules, idempotency_key
├── response.json      # Unified single-batch structured output & router trace
├── artifacts/         # Intermediate masks, CAD scripts, scraped pages, stems
├── evidence/          # Verification hashes, citations, test logs
└── audit.json         # User/agent actor, timestamps, Vault policy, WireGuard Space ID
```

All MinIO writes use **atomic write-temp-then-copy/rename** semantics (`minio-py` `7.2.0` exclusively, never `boto3`) so readers never observe partial files.

## 3. Finished Folder (`s3://kingdom-finished/`)

Every completed sandbox publishes a complete, clickable archive in `s3://kingdom-finished/{sandbox_id}/`. Clicking any item in the **SandboxViewer -> Finished Folder** surfaces the entire dossier for review and iterative improvement:

```text
s3://kingdom-finished/{sandbox_id}/
├── summary.md         # Human-readable executive summary, models used, one-batch deliverable manifest
├── artifacts/         # Final single-batch outputs (.mp4, .zip, .pdf, .step, .stl, .csv, BOM.json)
├── evidence/          # Face Consistency cosine scores, GHIDRA P-code report, citations
├── audit.json         # Immutable event chain + OpenTimestamps proof + IPFS Kubo CID
├── logs/              # Execution & Loki promtail structured logs
└── metrics/           # Latency, token count, GPU worker utilization, cost breakdown
```

Domain-specific finished bundles automatically attach:
- **Legal / Sovereign**: OpenTimestamps proof + IPFS Kubo CID immutable lien + Kissi Gazette entry.
- **Engineering**: GHIDRA headless decompilation summary + FreeCAD/OpenSCAD parametric model + OpenBOM/InvenTree M3/M4 fastener & torque wrench specification + Octopart sourcing table.
- **Video / UGC**: 600-clip @ 30s (`18,000s` -> `10x` parallel) manifest stitched via FFmpeg + MoviePy + WhisperX word-level sync into a single `final_video.mp4`.
- **Music / Vocal Tuning**: Demucs/Spleeter stem report + GSnap/MAutoPitch/Graillon 2/RVC vocal chain manifest.

## 4. 2,000 CUA Spaces Network & Syscall Isolation

1. **Dedicated Ephemeral VM**: Each of the `2,000` CUA Spaces (`trycua/cua` + Boat) runs in its own isolated container/micro-VM with dedicated filesystem and saved session state.
2. **WireGuard Zero Trust mTLS**: Every Space receives a point-to-point WireGuard `/32` tunnel to the control plane only; **east-west peer-to-peer traffic between Spaces is dropped (`no lateral movement`)**.
3. **Falco eBPF + Tetragon Enforcement**: Host eBPF probes monitor `execve`, `openat`, `connect`, `ptrace`, `/var/run/docker.sock`, and `/proc` mounts across every Space. Any syscall-evasion or container-escape attempt triggers immediate quarantine and Wazuh SIEM alert.

## 5. Granular Turn-Off Flags

Operators can disable equipping globally or selectively via environment variables or the live Settings drawer:
- `ENABLE_SANDBOX_EQUIP_ALL=false` -> Provisions lightweight minimal sandbox (skips pre-warming GPU/CUA/Vault attachments).
- `ENABLE_SANDBOX=false` -> Executes statelessly inline without bucket persistence.
- `ENABLE_DISCOVERY=false` -> Disables External Scout A and OSINT background scanning.
- `ENABLE_SECURITY=false` -> Sets security middleware to passive header-only mode for local debugging.
- `ENABLE_HERMES=false` -> Disables Hermes agent extensions (`hermes-agent`, `hermes-library`, `hermes-tool-use`).
