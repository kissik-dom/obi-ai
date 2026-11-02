# Kingdom AI OS

A screenshot-led, privacy-conscious multi-agent workspace. One OS, many domain workspaces, behind a typed task service and an accountable model router.

> This repository is built in phases from the [Master Plan v1](docs/MASTER_PLAN_v1.md). Each piece is shipped, tested, and verified before the next. "Unbreakable code that works first try" is not a promise anyone can keep; tested code, shipped in runnable pieces, is.
>
> **Naming:** the checked-in package and app UI still use the pre-rename **Obi AI** name. The product is being renamed to **Kingdom AI OS**, so both names appear until the `obi-ai` package name and UI strings are updated.

## Current state

**Shipped now:** the Next.js workspace app in `app/` and `lib/` — black/teal chat UI, browser-supported voice input, drag-and-drop attachments, deep research, document/PDF export, and an OpenAI-compatible gateway. The main app entry points are:

- `app/api/chat`: general chat through the agent swarm.
- `app/api/agent/*`: research, web search, analysis, prediction, document creation, and template creation.
- `app/api/gateway/chat/completions`: OpenAI-compatible chat completions.
- `app/api/upload/*`: Vercel Blob uploads and R2 presigned uploads.

**Foundation in progress:** the typed FastAPI task service in `services/api` with file-backed task storage and workspace-scoped bearer tokens for task reads (`GET /tasks`), plus the PostgreSQL/Valkey/Qdrant control-plane stores described below.

## Control plane

```
Identity -> Workspace -> Intent -> Model/Agent Stack -> Tools -> Isolated Sandbox
-> Memory/RAG -> Worker -> Validation/QC -> Artifact Store -> Audit -> User
```

The user asks for an outcome, not a model name. The router picks a stack and shows a "Why these tools?" explanation.

## Starting stack (Phase 1)

Verified, open components only. Exotic / unconfirmed model names stay quarantined until an exact repo + revision + license is confirmed.

- **UI**: Next.js (black/teal reference design)
- **API**: FastAPI task service
- **State**: PostgreSQL (durable truth), Valkey/Redis (queue, cache, locks)
- **RAG**: Qdrant (retrieval, not sole truth)
- **Model gateway**: LiteLLM, fallback chain local -> local backup -> approved cloud
- **Local inference**: Ollama (Qwen2.5, Llama 3.3, Qwen2.5-Coder, Hermes 3:8b)
- **Edge/TLS**: Caddy
- **Workers**: rootless containers, one per constrained resource
- **GPU**: Kaggle as an ephemeral, non-authoritative worker only

## Roadmap

0. **Security first:** Protect `main` with required reviews, stand up TLS, and rotate any credentials exposed during intake.
1. Control-plane skeleton: task API, model registry ingestion, secrets broker, auth.
2. Model layer: Ollama + LiteLLM gateway + fallback chain.
3. RAG & research: bge-m3 embeddings, reranker, SearXNG.
4. Two pilot workspaces end-to-end (Research + Images).
5. Media: ComfyUI image pipeline, then video/music workers on Kaggle one at a time.
6. Agents & automation (propose-only discovery; human approves promotion).
7. Hardening: Wazuh/CrowdSec, audit logging, backups + restore drills, auto-rollback.

## Verification labels

| Label | Meaning |
|---|---|
| CAPTURED | Named in intake; not validated |
| VERIFIED | Exact repo/revision/license + health check confirmed; eligible for staging |
| UNVERIFIED | Ambiguous/misspelled/no source; disabled |
| MEMBERSHIP_REQUIRED | Account/API key/quota needed |
| RESTRICTED | License/safety/rights review needed; quarantined |

## Scope boundaries

Built: the modular local-first OS, lawful research/OSINT, and consent-aware likeness workflows.

Catalogued, not deployed: offensive and otherwise restricted model candidates are quarantined in `config/models.yaml` and `config/tools.yaml` (`excluded_by_policy`). This branch keeps them visible for review, but does not activate or deploy them.

Not built: non-consensual face/body swap, scrapers designed to evade blocking, tooling to beat AI-detectors, covert surveillance of private individuals. The [Master Plan v1](docs/MASTER_PLAN_v1.md) draws these lines; this repo holds them.