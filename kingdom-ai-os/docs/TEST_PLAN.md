# Test plan

## Required statuses
`not_implemented`, `implemented`, `tested`, `failed`, `blocked`, `unverified`. Never infer `tested` from UI presence or a container starting. Record commit SHA, test-suite version, timestamp, environment, model/project exact version, result, logs, and reviewer.

## Provider/model test matrix
For each model: (1) exact identity and provider access; (2) connectivity and quota; (3) known-answer instruction/coding/JSON/retrieval tasks; (4) tools and schema validity; (5) prompt injection, synthetic-secret leakage, tenant isolation and server-side permission enforcement; (6) latency, timeout, cost, retry and fallback. For multimodal models, test each modality separately. Test at least 3 repetitions for nondeterministic tasks.

## Two provider credentials only
- Fireworks: validate credential server-side, verify intended exact model IDs, rate limits, timeout, revocation.
- OpenRouter: same tests, with fallback only to explicitly approved model IDs.
- Ensure logs, traces, error responses, browser bundles, and CI artifacts never include credentials. Do not assume two keys increase throughput.

## Open-source project verification
Each project record requires official repo, owner, exact release/commit, license text, commercial-use terms, project type, dependencies/SBOM, advisories, install command, health check, integration test, resource/network requirements, cleanup test, and last verified timestamp. A commercial API or wrapper is not to be labeled open source without evidence.

## Tab matrix
Each of the 28 canonical tabs requires route/render, responsive layout, interaction, loading/empty/error states, API contract, permissions, input validation, persistence, keyboard/accessibility, smoke test, and regression test. The 4 unresolved tab placeholders must remain blocked until their official names and scope are confirmed.

## End-to-end path
UI -> authenticated API -> task state -> model/router adapter -> approved tools -> Qdrant retrieval with workspace filter -> PostgreSQL task/audit metadata -> MinIO object with private access -> result UI. Inject failures at each hop. Verify timeout and retry bounds, cancellation, recovery after restart, no cross-workspace data, no secrets in logs, and idempotency for retried writes.

## Release gates
Build; tests; security; registry completeness; backup/restore; UI/accessibility; staging deployment; rollback. Any item blocked by missing keys, hardware, permission, original UI asset, or canonical tab names must be marked `blocked`, not passed.
