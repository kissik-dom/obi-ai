# Vultr deployment runbook (staging first)

This is a runbook, not evidence that deployment occurred. No Vultr deployment has been performed by this package.

1. Provision a Vultr VM sized for the selected workload; model inference/GPU workloads need separate capacity planning. Do not assume the listed models can run on a small CPU VM.
2. Configure SSH with the existing authorized key; disable password SSH where possible; patch OS; create a non-root deploy user. Do not put SSH private keys in this repository.
3. Install Docker Engine and Compose plugin from official sources.
4. Upload repository using reviewed GitHub commit; create `.env` on the server from a secret manager or secure shell session. For a local/staging bootstrap only, `./scripts/generate-secrets.sh` creates random service secrets and leaves the two provider keys blank. Never copy `.env` into Git.
5. Set unique secrets and the two provider keys only. Replace default root credentials with least-privilege MinIO credentials before production.
6. Validate `docker compose config`; inspect resolved config to ensure no secret leakage; run dependency/security scans.
7. Start staging with `docker compose up --build -d`; inspect logs for errors without printing secrets. Check `/health/live`, `/health/ready`, `/api/v1/system/dependencies`, and `/api/v1/system/providers`. The dependency report checks network reachability only; it does not prove data persistence or a working model call. Chat rejects all current unverified candidates; a model can only be called after an exact ID and supported provider mapping are reviewed and its registry status is explicitly set to VERIFIED. The chat adapter exists, but no live provider call has been tested here.
8. **Do not expose this prototype publicly.** It has no production authentication or per-user authorization. Before public access, implement and test identity, access control, tenant isolation, CSRF/session policy as applicable, TLS reverse proxy, upload security, and rate limits. Public firewall should expose only SSH from trusted IPs and HTTPS. Keep 5173/8000/4000/5432/6333/9000/9001 private behind the gateway.
9. Run smoke, auth, model access, upload, tenant isolation, persistence and restore tests. Record exact commit, VM image, versions, results.
10. Back up PostgreSQL, Qdrant, and MinIO data with encryption and test restoration to a separate environment.
11. Rollback: stop deployment, restore previous image/commit and database-compatible backup if migration requires it. Do not delete volumes during rollback.
12. Production only after human sign-off and all release gates.
