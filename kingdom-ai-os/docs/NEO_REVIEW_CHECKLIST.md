# Neo review checklist — do not treat as approved until evidence is attached

## Source of truth and scope
- [ ] Compare this handoff to the complete Library mapping and original downloaded chatbot UI source/asset. The original UI source was not identified in the materials inspected; the v4 scaffold has an empty apps/web directory, so the current UI is a prototype rather than a visual match.
- [ ] Confirm canonical names and scope for tabs 25–28; the source mapping explicitly names only 24 tabs.
- [ ] Confirm exact current model IDs and access for every provider model; all seed entries are UNVERIFIED.
- [ ] Normalize the full 600+ project inventory. Current JSON has 546 unique unverified candidates, not proof of 600 complete records; source categories include non-OSS services and APIs that must be classified.

## Code review
- [ ] Review all source, dependency versions, licenses, and transitive dependencies.
- [ ] Run backend tests, frontend production build, lint/type checks, and compose config.
- [ ] Replace all `latest` frontend dependency versions with lockfile-pinned versions after build verification.
- [ ] Add authentication and authorization before remote exposure.
- [ ] Implement DB migrations and persist task/model/project/audit state in PostgreSQL.
- [ ] Implement Qdrant collections, tenant/workspace filters, embedding pipeline, and retrieval tests.
- [ ] Implement MinIO bucket policies, per-user access, malware scanning, quotas, and object retention.
- [ ] Implement the verified provider adapter; prove keys remain server-side and test rate limits/fallbacks.
- [ ] Implement actual chat/task lifecycle, file attachments, character library, agent selection, and task cancellation/resume.
- [ ] Add keyboard navigation, contrast checks, screen-reader review, mobile browser tests, and wallpaper image safety.

## Release evidence
- [ ] Attach CI run URL and exact commit SHA.
- [ ] Attach model-by-model test report and open-source project-by-project verification report.
- [ ] Attach all 28 tab-specific tests; blocked tabs are not passed.
- [ ] Attach security review/SBOM/dependency scan and remediation status.
- [ ] Attach backup and restore proof.
- [ ] Attach Vultr staging deployment smoke test, TLS check, firewall review, and rollback proof.
- [ ] Obtain explicit human approval before production deployment.
