# Kingdom AI OS — Sandbox Specification

## Default creation policy

Every task creates a new isolated sandbox unless the per-tab or global sandbox
turn-off flag is set. Sandboxes exist under `/var/lib/kingdom/requests/<tab>/<idempotency-key>`
and must finish with an atomic manifest in `/var/lib/kingdom/finished/<tab>/<key>.manifest.json`.

## Layout

```
/var/lib/kingdom/
  requests/
    <tab>/
      <idempotency-key>/
        manifest.json
        input/
        work/
  finished/
    <tab>/
      <key>.artifact.json
      <key>.manifest.json
```

## Request Folder

- Created with a temp name then `os.replace`/rename; scanners never see a partial sandbox.
- `manifest.json` records tab, idempotency key, sandbox flags, CUA space, GPU worker,
  and MinIO bucket.
- Duplicate idempotency key returns the existing folder and never creates a second.

## Finished Folder

- Artifact is written to `.tmp-<uuid>`, flushed, `fsync`, then atomically renamed.
- Manifest includes `schema: kingdom.finished.v1`, tab, task id, content file, and payload.

## MinIO buckets

- `kingdom-sandboxes` — immutable initial inputs for each task.
- `kingdom-sandboxes-<tab>` — per-tab working objects.
- `kingdom-finished` — encrypted, versioned finished artifacts.
- `kingdom-knowledge` — training and knowledge imports.

## CUA isolation

- CUA Fleet exposes 5 spaces, internal ports 2000-2004, each with its own
  browser profile, clipboard, filesystem, and network egress policy.
- No CUA space can write to another space's path or call backend infrastructure directly.
- Every action is audited with sidecar screenshots; screenshots are stored only in MinIO.

## Turn-off flags

| Flag | Default | Effect |
| --- | --- | --- |
| `FLAG_SANDBOX` | 1 | master sandbox toggle |
| `FLAG_SANDBOX_<TAB>` | 1 | per-tab override |
| `FLAG_AGENT_SWARM` | 1 | disable multi-agent fanout |
| `FLAG_GPU_WORKERS` | 1 | disable GPU dispatch |
| `FLAG_VIDEO_GENERATION` | 1 | disable generated video |
| `FLAG_IMAGE_GENERATION` | 1 | disable generated images |
