# QA report — 2026-10-27

## Checks actually performed in this environment

| Check | Result | Evidence / limitation |
|---|---|---|
| Python syntax compilation | PASS | `python -m compileall -q backend/app backend/tests` |
| Backend API tests | PASS | `./scripts_validate.sh` → 21 passed |
| Registry JSON integrity | PASS | 28 tab records, 101 model candidates, 546 project/tool candidates, 4 document templates; duplicate checks pass |
| Registry status guardrails | PASS | All seed model and project/tool candidates remain `UNVERIFIED`; unverified model invocation is rejected |
| PDF generation and long-document stress | PASS | ReportLab PDF output tested; a controlled 1.9-million-character input rendered 509 pages in about 1.3 seconds; tests check title, glossary placeholder, and footer quote on first/last pages |
| Editable DOCX generation | PASS | `python-docx` output reopens in tests; title, chapter, glossary, and footer are present |
| Template profiling | PASS | DOCX style/geometry and font samples, PDF dimensions/fonts/text samples, and image dimensions/color samples are extracted without persisting the upload |
| Model verification runner | PASS (dry-run only) | 101 candidate rows; 0 live tests; 101 blocked because exact IDs/provider mappings and credentials are unavailable |
| Registry change validation | PASS | Duplicate prevention and proposal-only behavior tested; no live mutation is performed |
| YAML syntax parsing | PASS | Compose, LiteLLM config, and GitHub Actions YAML parse with PyYAML |
| Secret redaction | PASS | Synthetic test credentials do not appear in provider status or dependency responses |
| Frontend syntax inspection | PARTIAL | Global TypeScript compiler found no syntax diagnostics; dependency/typecheck fails because React, lucide-react, and react/jsx-runtime packages are not installed |
| Frontend production build | BLOCKED | `npm install --no-audit --no-fund` timed out; no successful production build claimed |
| Docker Compose schema / image build | BLOCKED | Docker CLI is not installed; YAML parsing is not equivalent to `docker compose config` or an image build |
| Live model/provider checks | NOT RUN | No provider credentials are available here and no candidate has an exact verified model ID. The dry-run is not a working-model test. |
| Database/Qdrant/MinIO persistence | NOT IMPLEMENTED | API has reachability checks but no production persistence, retrieval, or storage adapters |
| Auth, authorization, tenant isolation, task queue | NOT IMPLEMENTED | Prototype must not be exposed publicly until these controls exist |
| Durable long-book generation | PARTIAL | PDF/DOCX rendering supports large supplied content, but chapter-by-chapter generation, resumable jobs, source/citation verification, and visual QA orchestration are not implemented |
| Pixel-perfect template recreation | NOT VERIFIED | Basic profile extraction and native presets exist; arbitrary layout recreation and custom-font embedding require additional implementation and side-by-side review |
| Complete 600+ tool inventory | INCOMPLETE | 546 unique candidate records; eight license-source spot checks recorded, but all project/install/security/integration status remains unverified |
| Canonical tabs 25–28 | BLOCKED | Supplied source mapping names 24 workspaces only; four placeholders remain unresolved |
| GitHub push / Codex work | BLOCKED | No writable target repository was established through the connected GitHub access; no push is claimed |
| Vultr deployment | NOT RUN | No Vultr host/API credentials or deployment access established |

## Interpretation

This is an expanded, testable engineering handoff—not a production release. `scripts_validate.sh` is reproducible. Do not expose the prototype publicly until authentication/authorization, tenant isolation, persistence, upload security, model credentials and IDs, a real task queue, dependency builds, Docker validation, backup/restore, and deployment smoke tests are completed.
