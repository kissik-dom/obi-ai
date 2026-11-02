# Master Plan v1

This file is the repository-local pointer for the plan referenced by the root
[`README.md`](../README.md). The executable version of the plan's safety and
verification boundaries lives in:

- [`config/models.yaml`](../config/models.yaml): model states and the verified / restricted / quarantined split.
- [`config/tools.yaml`](../config/tools.yaml): tool states and `excluded_by_policy` entries that are not built in this repo.
- [`README.md`](../README.md#roadmap): the current phase order and status against this plan.

## Control plane

```
Identity -> Workspace -> Intent -> Model/Agent Stack -> Tools -> Isolated Sandbox
-> Memory/RAG -> Worker -> Validation/QC -> Artifact Store -> Audit -> User
```

## Phase order

0. **Security first:** protect `main`, stand up TLS, and rotate any credentials exposed during intake.
1. Control-plane skeleton: task API, model registry ingestion, secrets broker, auth.
2. Model layer: Ollama + LiteLLM gateway + fallback chain.
3. RAG & research: bge-m3 embeddings, reranker, SearXNG.
4. Two pilot workspaces end-to-end (Research + Images).
5. Media: ComfyUI image pipeline, then video/music workers on Kaggle one at a time.
6. Agents & automation (propose-only discovery; human approves promotion).
7. Hardening: Wazuh/CrowdSec, audit logging, backups + restore drills, auto-rollback.