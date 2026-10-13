# Kingdom AI OS

A screenshot-led, privacy-conscious multi-agent workspace. One OS, many domain workspaces, behind a typed task service and an accountable model router.

> This repository is built in phases from the **Master Plan v1**. Each piece is shipped, tested, and verified before the next. "Unbreakable code that works first try" is not a promise anyone can keep; tested code, shipped in runnable pieces, is.

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
- **Local inference**: Ollama (Qwen2.5, Llama 3.3, Qwen2.5-Coder, a reviewed low-refusal variant)
- **Edge/TLS**: Caddy
- **Workers**: rootless containers, one per constrained resource
- **GPU**: Kaggle as an ephemeral, non-authoritative worker only

## Roadmap

0. **Security first** — rotate every exposed credential (the album screenshots leak API keys and a GitHub PAT; treat all as compromised), protect `main`, stand up TLS.
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

Built: the modular local-first OS, lawful research/OSINT, consent-aware likeness workflows, quarantined offensive models.

Not built: non-consensual face/body swap, scrapers designed to evade blocking, tooling to beat AI-detectors, covert surveillance of private individuals. The Master Plan draws these lines; this repo holds them.
