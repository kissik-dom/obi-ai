# Kingdom AI OS — Independent Code, Integration, UI, Security, and Release Audit Template

**Reusable for:** Kingdom AI OS, Neo-generated changes, contractor submissions, future branches, and other software projects.  
**Version:** 1.0 | **Prepared:** 2026-10-28  
**Audit outcome options:** `PASS`, `PASS WITH ACCEPTED RISKS`, `FAIL`, `BLOCKED`, `NOT TESTED`.

> **Rule:** reviewers must report observed evidence, not promises. “The code appears to support X” is not the same as “X passed an end-to-end test.” Never claim the application is production-ready if critical controls or tests are absent.

## A. Audit cover sheet

- Project/repository URL:
- Branch and commit SHA:
- Pull request/change set:
- Release/build identifier:
- Audit date and timezone:
- Reviewer(s), roles, and independence:
- Environment: local / CI / staging / production-like:
- Operating system and runtime versions:
- Dependency lockfile hash:
- Database/service versions:
- Test data source and privacy classification:
- Secrets source (describe location only; never copy values):
- Budget/time limit approved:
- Scope exclusions and reason:

## B. Executive decision

| Gate | Status | Evidence link/path | Blocking defects |
|---|---|---|---|
| Repository integrity and provenance | NOT TESTED | | |
| Build reproducibility | NOT TESTED | | |
| Unit/integration/e2e tests | NOT TESTED | | |
| Frontend UX/accessibility | NOT TESTED | | |
| API and provider integrations | NOT TESTED | | |
| Model catalog and capability QA | NOT TESTED | | |
| Upload/OCR/document pipeline | NOT TESTED | | |
| Memory and retrieval isolation | NOT TESTED | | |
| Agents/tool execution safety | NOT TESTED | | |
| Scraping/ingestion safety | NOT TESTED | | |
| Security/privacy | NOT TESTED | | |
| Performance/load/reliability | NOT TESTED | | |
| Backup/restore/operations | NOT TESTED | | |
| Deployment and rollback | NOT TESTED | | |

**Decision:** `FAIL / BLOCKED / PASS WITH ACCEPTED RISKS / PASS`  
**Conditions to proceed:**  
**Known risks accepted by:**  
**Must-fix issues:**  
**Evidence location:**

## C. Severity rubric

- **P0 Critical:** remote compromise, credential exposure, unauthorized privileged action, cross-user data leak, destructive action without authorization, unrecoverable data loss. Stop release immediately.
- **P1 High:** core product unusable, authentication/authorization bypass, persistent data corruption, major model-routing/security failure, backup cannot restore. Block release.
- **P2 Medium:** important workflow broken with workaround, substantial reliability/performance defect, accessibility blocker for a key workflow. Usually block broad release; document owner and deadline.
- **P3 Low:** cosmetic issue, minor copy/layout defect, noncritical edge case. May be accepted with owner and target date.

Each issue must include: ID, severity, affected component, reproduction steps, expected/actual behavior, logs with secrets removed, screenshots or test output, suspected root cause, fix commit, regression test, and retest result.

## D. Repository and architecture audit

### D1. Provenance and completeness

- [ ] Obtain source from the intended repository/branch; verify commit and release tag.
- [ ] Compare archive file list and checksums against the reviewed source tree.
- [ ] Check for missing, duplicated, stale, or unexpectedly generated files.
- [ ] Confirm the app's actual entry points and deployment manifests.
- [ ] Identify all packages, services, databases, queues, storage, inference providers, and external APIs.
- [ ] Map UI action → frontend handler → API endpoint → service → persistence/provider → response rendering.
- [ ] For every advertised button/feature, identify the implementation and its test. Disabled or placeholder controls must be clearly disclosed.
- [ ] Verify registries use canonical IDs and provenance; separate candidates from verified integrations.
- [ ] Identify dead code, duplicate adapters, unreferenced routes, placeholder data, mock implementations, and TODOs.
- [ ] Confirm generated documentation accurately reflects the actual source.

**Reviewer notes:**

### D2. Architecture map

Create a diagram or table showing each component, owner, input/output, trust boundary, persistence, authentication method, failure mode, and monitoring. If no architecture map exists, add one before expanding features.

| Component | Entry point | Dependencies | Data handled | Auth boundary | Persistence | Tests |
|---|---|---|---|---|---|---|
| Frontend/UI | | | | | | |
| Backend/API | | | | | | |
| Model router | | | | | | |
| Agent/tool runner | | | | | | |
| Document/OCR pipeline | | | | | | |
| Memory/RAG | | | | | | |
| Scraper/ingestion | | | | | | |
| Database/object store | | | | | | |
| Jobs/queue/scheduler | | | | | | |
| Audit/metrics/logging | | | | | | |

## E. Reproducible build and dependency integrity

- [ ] Build from a clean checkout in a disposable environment.
- [ ] Install only from committed lockfiles; fail on unpinned or drifting production dependencies unless explicitly justified.
- [ ] Run formatting, linting, static type checks, unit tests, and production build.
- [ ] Build every Docker image and run Compose config validation.
- [ ] Check base image provenance, pinned tags/digests, non-root execution, read-only filesystems where feasible, and minimal packages.
- [ ] Scan direct and transitive dependencies for known vulnerabilities and abandoned packages.
- [ ] Generate an SBOM and archive it with the build.
- [ ] Verify no developer-local paths, machine-specific config, or secret values are required.
- [ ] Repeat build and compare artifacts or document expected nondeterminism.
- [ ] Ensure failure exit codes propagate; no `|| true` or ignored test errors in release gates.

**Required commands (adapt to actual project; never assume a command exists without checking):**

```bash
# inspect project scripts and documented commands first
python --version
python -m compileall backend/app backend/tests
pip check
pytest -q
./scripts_validate.sh

# if frontend/package.json defines these commands
cd frontend
npm ci
npm run build

# if Docker is installed and Compose exists
cd ..
docker compose config --quiet
docker compose build --pull
```

Record every command, exit code, duration, environment, and log path. If the tool is unavailable, mark `BLOCKED`; do not count it as passed.

## F. Unit, integration, contract, and end-to-end tests

### F1. Unit tests

- [ ] Input validation and boundary values.
- [ ] Empty/null/malformed data.
- [ ] Exceptions, timeouts, retries, and cancellation.
- [ ] Serialization/deserialization and schema versions.
- [ ] Provider adapter response variants.
- [ ] Idempotency and duplicate submissions.
- [ ] Permission checks and tenant/user scoping.
- [ ] Deterministic tests use controlled clocks/randomness/network mocks.

### F2. Integration tests

- [ ] Backend to each configured database/object store/queue.
- [ ] Migration from empty database and upgrade from previous release.
- [ ] Provider authentication, model catalog, inference call, response parsing, usage tracking.
- [ ] File upload to storage, metadata record, processing job, extracted result, retrieval and deletion.
- [ ] Audit log written for privileged/mutating actions.
- [ ] Dependency down / slow / rate-limited / malformed response scenarios.

### F3. End-to-end tests

- [ ] A new user can reach the supported landing state and understand what is functional.
- [ ] A normal request can be submitted, routed, streamed or completed, cancelled, and retried safely.
- [ ] A model error appears as an actionable error, not a fake success.
- [ ] A document is uploaded, processed, cited, downloaded/exported, and deleted according to permissions.
- [ ] A template can be selected, edited, previewed, exported, reopened, and compared to the source.
- [ ] Theme and wallpaper controls update all relevant surfaces and survive refresh according to the documented persistence promise.
- [ ] Keyboard-only use and screen reader labels work for critical flows.
- [ ] All empty, loading, success, partial, error, and disabled states are visible and consistent.

## G. User interface and usability acceptance

The desired visual direction is a high-contrast, polished interface with color accents, but visual polish does not excuse broken functionality. Compare against the approved reference screenshots/assets; record viewport sizes and theme state.

### G1. Navigation and interaction inventory

For **every** visible control, create a row. Do not sample only the homepage.

| Screen/tab | Control | Intended behavior | Click/keyboard test | API/state effect | Result | Evidence |
|---|---|---|---|---|---|---|
| | | | | | NOT TESTED | |

- [ ] Every visible button performs its advertised action or is visibly disabled with an explanation.
- [ ] No dead links, empty panels, placeholder buttons, duplicate IDs, or console errors.
- [ ] Back/forward navigation and deep links behave correctly.
- [ ] Loading states cannot be submitted repeatedly to duplicate an action.
- [ ] Focus order is logical; focus is visible; dialogs trap/restore focus correctly.
- [ ] Color contrast, zoom/reflow, labels, alt text, reduced motion, and touch targets are checked.
- [ ] Responsive behavior is tested at narrow mobile, tablet, laptop, and wide desktop sizes.
- [ ] Theme switching covers modals, menus, tables, code blocks, empty/error states, and settings—not just the page background.
- [ ] Wallpaper upload validates type/size, handles decode failure, provides crop/position/scale/blur/dimming controls, and never executes uploaded content.
- [ ] Settings persistence is described honestly: browser-only, account sync, or server persistence.
- [ ] UI never claims “saved,” “uploaded,” “running,” or “deployed” before the underlying operation succeeds.

### G2. Accessibility and clarity

- [ ] Critical tasks can be completed without a mouse.
- [ ] Labels describe the task, not just “click here.”
- [ ] Errors say what happened, whether data was saved, and what the user can do next.
- [ ] Long workflows have progress, cancellation, resume/retry, and clear completion states.
- [ ] No important status relies on color alone.
- [ ] Plain-language explanations are available for complex model, privacy, and deployment settings.

## H. Provider and model integration tests

Use `docs/MASTER_MODEL_AND_FEATURE_QA_PROTOCOL.md`. In addition:

- [ ] `FIREWORKS_API_KEY`, `OPENROUTER_API_KEY`, and `HF_TOKEN` are read only on server-side code/workflows that need them.
- [ ] The secret names match exactly and secrets are not in frontend bundles, source maps, logs, error traces, test snapshots, or artifacts.
- [ ] A missing key yields `BLOCKED`/configuration error without crashing the application.
- [ ] Invalid/expired key yields a clear auth failure without leaking provider response bodies.
- [ ] Provider catalog discovery is distinct from inference test and capability test.
- [ ] Exact provider model IDs are verified against current catalogs or official docs.
- [ ] Unknown/unverified IDs cannot be invoked by a normal user unless explicitly placed in a controlled testing workflow.
- [ ] Model output is treated as untrusted input; sanitize Markdown/HTML and validate JSON before using it.
- [ ] Model cannot change its own permissions, invoke hidden tools, or bypass server-side authorization.
- [ ] Provider rate limit, timeout, 5xx, malformed JSON, empty response, and partial stream paths are tested.
- [ ] Retry logic is bounded; non-idempotent tools are not blindly repeated.
- [ ] Fallback provider/model is visible in telemetry and does not silently violate data/privacy policy.
- [ ] Costs, token counts, latency, model ID, and request correlation ID are tracked without recording secrets or unnecessary prompt content.
- [ ] Long-context and multimodal claims have corresponding tests, not just a successful chat completion.
- [ ] Every model has test status, date, revision, evidence, license, access mode, and a responsible owner.

### H1. Five-to-ten-repeat policy

- [ ] Each priority model completed at least five runs per critical test.
- [ ] High-priority, JSON, tool-call, safety-boundary, image, and video cases completed ten runs where feasible.
- [ ] Failures and retries are preserved in results; they are not overwritten by a later pass.
- [ ] Reports include denominator, pass rate, cost, p50/p95 latency, and error category.
- [ ] Test suite distinguishes unavailable model, unsupported modality, access denied, provider error, quality failure, and application integration failure.

## I. Upload, OCR, document, template, and export tests

### I1. Upload and file security

- [ ] Allowed file types and size limits are explicit and enforced server-side.
- [ ] Extension, MIME type, file signature, and actual parser agree; do not trust filename alone.
- [ ] Reject path traversal, archive bombs, decompression bombs, malformed PDFs, oversized images, malicious macro-enabled files, and unsupported formats.
- [ ] Uploaded content is stored outside executable/static web roots and never executed.
- [ ] Malware scanning/quarantine policy is implemented or the feature is explicitly not production-ready.
- [ ] File ownership and access checks apply to list, download, process, preview, and delete routes.
- [ ] Temporary files are cleaned on success, error, and cancellation.
- [ ] User receives truthful progress and failure states.

### I2. OCR and ingestion correctness

- [ ] Compare text extraction against human-reviewed ground truth across clean scans, low DPI, skew, rotation, mixed columns, tables, handwriting (if claimed), and multiple languages.
- [ ] Verify page order, heading hierarchy, table cells, footnotes, captions, references, and page numbers.
- [ ] Store source page/region metadata so answers can be cited.
- [ ] Deduplicate by content hash where appropriate and avoid silently overwriting newer revisions.
- [ ] Batch ingestion resumes after interruption and reports per-file success/failure.
- [ ] One corrupt file does not silently corrupt or halt the whole batch.
- [ ] Verify source encoding and preserve original file bytes.

### I3. Templates and long-form book generation

- [ ] Template selection, variable substitution, styles, headers/footers, page numbering, tables of contents, references, and export are covered by golden tests.
- [ ] DOCX remains editable; PDF text is searchable where expected; fonts embed/render correctly.
- [ ] Test short, 50-page, 100-page, and 500-page stress documents separately. Rendering a long document is not proof that the content is coherent or factually correct.
- [ ] Long jobs are queued, resumable, cancellable, and idempotent; progress reflects actual work.
- [ ] Check section continuity, duplicated/missing sections, citation validity, glossary consistency, page breaks, orphan/widow handling, table overflow, and image resolution.
- [ ] Re-open exported files with independent readers and compare against expected content.
- [ ] Visual regression snapshots are reviewed at multiple zoom levels.

## J. Memory, RAG, and recursive-learning tests

Define the exact product behavior before testing; “memory” and “recursive learning” are ambiguous labels.

### J1. Memory

- [ ] Explicitly identify what is stored: conversation history, user preferences, embeddings, summaries, or learned model weights.
- [ ] User can inspect, correct, export, and delete the supported memory types.
- [ ] Memory is scoped by authenticated user/tenant and access control is tested with two separate users.
- [ ] One user's private fact never appears in another user's retrieval or generated answer.
- [ ] Consent, retention period, deletion propagation, backups, and audit trail are defined.
- [ ] Memory update and deletion survive refresh/restart and are verified at storage and retrieval layers.
- [ ] Contradictory preferences are timestamped/resolved transparently; no silent overwrites.
- [ ] Untrusted prompt injection in retrieved memory cannot override system policy.

### J2. Retrieval augmented generation (RAG)

- [ ] Ingestion pipeline and embeddings are versioned.
- [ ] Retrieval Recall@k and nDCG are measured against a labeled query set.
- [ ] Answers cite the correct source/page and refuse to invent sources.
- [ ] Conflicting documents and stale versions are detected.
- [ ] Chunking, overlap, metadata filters, reranker, and top-k are tuned one at a time.
- [ ] Retrieval cannot cross tenant or permission boundaries.
- [ ] Re-indexing, deletion, and failed jobs have verifiable outcomes.

### J3. “Recursive learning” / self-improvement

- [ ] State whether this means iterative prompting, memory summarization, retrieval updates, preference tuning, LoRA training, or actual model-weight updates.
- [ ] No model silently retrains itself on private/user content without explicit consent, governance, and documented data controls.
- [ ] All generated training examples are traceable to permitted sources and reviewed for leakage, duplication, and quality.
- [ ] A holdout set measures improvement and regression; training data does not leak into the holdout.
- [ ] Every update is versioned, evaluated, approved, and reversible.
- [ ] Automated feedback cannot poison the training set or grant new privileges.
- [ ] Rollback restores the previous model/prompt/index and records which version served each request.

If these controls are absent, mark recursive learning `NOT IMPLEMENTED` or `BLOCKED`, not “working.”

## K. Agent and tool execution security

- [ ] Agent tool permissions are allowlisted by task and user authorization.
- [ ] File, shell, browser, network, database, and deployment tools run in isolated environments with least privilege.
- [ ] Arbitrary shell execution is disabled unless explicitly required and sandboxed.
- [ ] Network egress restrictions prevent SSRF and access to cloud metadata endpoints.
- [ ] Tool arguments are schema-validated and bounded; output is treated as untrusted.
- [ ] Mutating or financial actions require explicit confirmation and audit logging.
- [ ] Idempotency keys prevent duplicate actions.
- [ ] Timeouts, CPU/memory limits, task quotas, cancellation, and cleanup are enforced.
- [ ] Secrets are never placed in model prompts or tool outputs unless narrowly required and redacted.
- [ ] Prompt-injection tests cover webpages, PDFs, emails, code comments, OCR text, and tool output.
- [ ] Agents cannot modify production secrets, CI permissions, or deployment credentials by default.
- [ ] Every agent run records tool calls, outcomes, duration, cost, and error state with privacy-appropriate redaction.

## L. Web scraping and source ingestion

- [ ] Respect applicable terms, robots directives, access controls, rate limits, copyright, and privacy requirements.
- [ ] Restrict URL schemes and destinations; block loopback, private network, link-local, and cloud metadata IPs to prevent SSRF.
- [ ] Revalidate DNS/IP after redirects and block unsafe redirect chains.
- [ ] Set page-size, depth, concurrency, timeout, and total-job limits.
- [ ] Parse HTML in a sandbox; never execute page JavaScript or downloaded files by default.
- [ ] Preserve source URL, retrieval timestamp, title, hash, license/rights notes, and extracted-content provenance.
- [ ] Handle duplicates, robots denial, login pages, CAPTCHA, paywalls, and HTTP errors transparently; do not claim content was collected if it was not.
- [ ] Untrusted page text cannot control system prompts or invoke tools.
- [ ] Deletion and source removal are propagated where policy requires.

## M. Security and privacy checklist

### M1. Identity, authorization, and session management

- [ ] Production authentication exists; no privileged routes are public by accident.
- [ ] Authorization is checked server-side on every protected object/action.
- [ ] Tenant isolation is tested with positive and negative cases.
- [ ] Session/token expiry, refresh, logout, CSRF where applicable, CORS, and cookie flags are correct.
- [ ] Rate limits and abuse controls cover login, upload, inference, scraping, and expensive jobs.
- [ ] Administrative actions require stronger authorization and are audited.

### M2. Secrets and supply chain

- [ ] Secret scanning runs on commits and repository history where appropriate.
- [ ] No keys in `.env.example`, fixtures, docs, screenshots, source maps, container layers, or build artifacts.
- [ ] `.gitignore` covers `.env`, private keys, local databases, caches, and generated reports containing private data.
- [ ] Keys are least-privilege, rotated, separated by environment, and revocable.
- [ ] CI uses minimal `GITHUB_TOKEN` permissions and pins third-party actions to reviewed versions/SHAs where feasible.
- [ ] Forked PRs cannot access deployment secrets.
- [ ] SSH host identity is verified; no blind host-key bypass.
- [ ] Dependency vulnerabilities and license obligations are reviewed.

### M3. API, data, and output handling

- [ ] Validate input length, type, encoding, schema, and allowed fields.
- [ ] Avoid SQL/command/template injection and unsafe deserialization.
- [ ] Rate limit and bound expensive operations.
- [ ] Escape/sanitize model-generated HTML/Markdown and uploaded filenames.
- [ ] Logs exclude passwords, tokens, private keys, full sensitive documents, and unnecessary personal data.
- [ ] Retention, deletion, export, and backup policy are documented and tested.
- [ ] Encryption in transit and at rest are configured for production services where appropriate.
- [ ] Error messages do not reveal internal stack traces, secrets, or cross-tenant data.

### M4. Threat-model exercise

Create a short threat model for: malicious user, compromised provider key, prompt injection in an uploaded document, compromised dependency, malicious repository contributor, SSRF via scraping, runaway agent, model hallucination, database leak, and stolen deployment credential. For each, document attack path, impact, control, test, owner, and residual risk.

## N. Database, object storage, queues, and observability

- [ ] Production persistence is real, not browser localStorage or in-memory placeholders unless explicitly intended.
- [ ] Migrations are versioned and reversible where feasible.
- [ ] Connection pooling, least-privilege database users, TLS, and backup policy are configured.
- [ ] Qdrant/vector index permissions and metadata filters enforce tenant boundaries.
- [ ] Object storage buckets are private by default; signed URLs expire and are scoped.
- [ ] Queue jobs are idempotent, retry-bounded, dead-lettered, and observable.
- [ ] Health endpoints distinguish liveness from readiness and report dependencies honestly.
- [ ] Metrics include latency, error rates, saturation, queue depth, provider status, spend, and task outcomes.
- [ ] Logs have correlation IDs and redaction; alerts are actionable.
- [ ] Alert routing and incident response are tested.

## O. Performance, load, resilience, and recovery

Run controlled load tests in a non-production environment using synthetic data. Define target load and SLOs before execution.

- [ ] Baseline: p50/p95/p99 latency, throughput, error rate, CPU, RAM, GPU/VRAM, DB connections, queue depth.
- [ ] Steady-state test at expected load.
- [ ] Burst test and concurrency limit test.
- [ ] Long-context, large upload, OCR batch, and large export stress tests.
- [ ] Provider timeout/rate-limit/outage and database/storage outage tests.
- [ ] Backpressure prevents unbounded queue/memory growth.
- [ ] Graceful degradation and fallback are truthful to the user.
- [ ] No retry storm, duplicate side effects, or uncontrolled spend.
- [ ] Backup integrity verified; perform a restore drill to a clean environment.
- [ ] Recovery time objective (RTO) and recovery point objective (RPO) are measured.
- [ ] Disaster recovery procedure and owner are documented.

## P. Deployment to Vultr/Voltaire via Neo

The deployment operator should use the repository's deployment guide and should not infer missing server details. Keep SSH private keys and root credentials out of the project ZIP and GitHub.

### P1. Before deployment

- [ ] Confirm target repo, branch, commit SHA, and archive checksum.
- [ ] Confirm Vultr instance identity and expected OS; do not expose server number, password, or private key in logs.
- [ ] Confirm secrets are configured in the server environment independently of GitHub Actions.
- [ ] Confirm firewall ports, TLS/domain, DNS, backup, disk capacity, and monitoring.
- [ ] Confirm container images build and Compose config validates.
- [ ] Confirm health/readiness checks and rollback version exist.
- [ ] Confirm DB migration backup and restore path.

### P2. Deployment execution

- [ ] Deploy to staging first where possible.
- [ ] Verify host key and SSH destination.
- [ ] Pull the reviewed commit by SHA; do not deploy an unreviewed default branch head.
- [ ] Build or pull pinned images and record digests.
- [ ] Apply migrations with backup and rollback plan.
- [ ] Inject runtime secrets through protected environment, never command-line echo/history.
- [ ] Start services and check health/readiness, logs, metrics, and TLS.
- [ ] Run smoke tests through the public/internal endpoint and verify provider connectivity only for approved test IDs.
- [ ] Confirm user-facing status reflects reality.

### P3. After deployment

- [ ] Verify deployed commit SHA matches approved SHA.
- [ ] Verify secrets are not visible in process listings, logs, image layers, or frontend bundles.
- [ ] Verify HTTPS, headers, firewall, rate limits, and access controls.
- [ ] Run core end-to-end flows and check logs/alerts.
- [ ] Verify backup job and perform a restore test on a separate target.
- [ ] Record deployment duration, incidents, and final status.
- [ ] Exercise rollback or prove rollback instructions with a staging simulation.

## Q. Defect log template

| ID | Severity | Component | Reproduction steps | Expected | Actual | Evidence | Fix commit | Regression test | Retest |
|---|---|---|---|---|---|---|---|---|---|
| BUG-001 | P1 | | | | | | | | NOT TESTED |

## R. Feature-by-feature acceptance register

Fill in one row per feature and every sub-feature. The status must reflect evidence in this commit/environment.

| Feature | Required observable behavior | Unit | Integration | E2E | Security | Status | Evidence / blocker |
|---|---|---|---|---|---|---|---|
| Model catalog | Search/filter with provenance and accurate status | | | | | NOT TESTED | |
| Add model | Validate ID/access/license; no guessed IDs | | | | | NOT TESTED | |
| Model routing | Correct provider/model, visible fallback | | | | | NOT TESTED | |
| Model evaluation | Repeatable prompt suites, scoring and report | | | | | NOT TESTED | |
| Agent builder | Create/configure, validate tools, run in sandbox | | | | | NOT TESTED | |
| Tool permissions | Allowlist, confirmation, audit trail | | | | | NOT TESTED | |
| File upload | Validate, store privately, process, delete | | | | | NOT TESTED | |
| OCR/ingestion | Ground-truth accuracy and page citations | | | | | NOT TESTED | |
| Document studio | Editable DOCX/searchable PDF and visual QA | | | | | NOT TESTED | |
| Templates | Select, edit, preview, export, reopen | | | | | NOT TESTED | |
| Memory | Inspect, correct, delete, isolate per user | | | | | NOT TESTED | |
| RAG/search | Accurate retrieval with source citations | | | | | NOT TESTED | |
| Recursive learning | Explicitly defined, versioned, evaluated, reversible | | | | | NOT TESTED | |
| Web scraping | SSRF protections, rate limits, provenance | | | | | NOT TESTED | |
| Theme/skin | Color themes across all states and components | | | | | NOT TESTED | |
| Wallpaper/backdrop | Upload safely, crop/scale/blur/dim, persistence promise | | | | | NOT TESTED | |
| Export/report | Correct format, no secrets, repeatable output | | | | | NOT TESTED | |
| Authentication | Secure login/session and server-side authz | | | | | NOT TESTED | |
| Audit logs | Required actions traced and redacted | | | | | NOT TESTED | |
| Backup/restore | Restore verified data in clean environment | | | | | NOT TESTED | |
| Deployment | Correct commit, health, TLS, rollback | | | | | NOT TESTED | |

## S. Reviewer report template

### S1. What was actually tested

List commands, tests, browsers, viewports, provider/model IDs, run counts, and environment. Mark unavailable tools and unrun tests as blocked/not tested.

### S2. What passed

For every pass, include the evidence location and the assertion that passed.

### S3. What failed

Include severity, reproduction, logs/screenshots, and issue IDs.

### S4. What remains unverified

Explicitly list all areas not tested, including features that are only mocked, local-only, disabled, or missing server-side persistence.

### S5. Security and deployment statement

- Secrets scanned? yes/no, tool/version:
- Dependencies scanned? yes/no, tool/version:
- Auth/authz tested? yes/no:
- Tenant isolation tested? yes/no:
- Restore drill performed? yes/no:
- Staging deployment tested? yes/no:
- Production deployment performed? yes/no:
- Residual risks accepted by:

### S6. Final decision

Choose one and explain:

- `PASS`: all release gates passed with evidence.
- `PASS WITH ACCEPTED RISKS`: no critical blocker; each accepted risk has named owner and mitigation.
- `FAIL`: a test failed or a release gate is unmet.
- `BLOCKED`: required credentials, services, hardware, or environment were unavailable.
- `NOT TESTED`: no evidence was collected.

## T. Audit ethics and operating rules

1. Do not test on production data unless explicitly approved and protected.
2. Do not paste credentials into chat, issue trackers, or test prompts.
3. Do not use real people's private data, voice, face, or likeness without permission.
4. Do not test security by attacking third-party systems; use authorized sandboxes.
5. Do not treat an AI-generated code review as independent verification of itself. Require actual test runs and human review for security-sensitive changes.
6. Do not mark an entire feature as passed because its happy path works once.
7. Do not hide failures in averages, replace prior reports, or discard failed runs.
8. Keep a clear boundary between a designed test, a test attempted, a test passed, and a feature verified.
