# Known gaps — must be resolved or explicitly accepted before release

- Original chatbot UI source/asset has not been identified or visually compared; inspected source packages include architecture and tab guides, but the v4 scaffold has an empty apps/web directory. This frontend is a new prototype.
- Only 24 tab names are found in the supplied mapping. Four entries are blocked placeholders pending the canonical tab names.
- The current model seed has 101 candidates but all are UNVERIFIED. The source mapping includes model names and claims not independently verified for existence, provider ID, context, modality, availability, license or quality.
- The project/tool intake contains 546 unique candidate names normalized from the mapping and older registry sources, not a complete verified inventory of 600+. Candidates may include commercial services, APIs, wrappers, and tools; their project status remains unverified. Eight entries have license-source spot checks recorded; install, security, maintenance, and integration checks remain outstanding.
- Chat invocation is enabled only for registry records marked VERIFIED with exact IDs and supported provider mappings; the current seed has no verified models, so candidate invocation is still blocked. Live model-catalog discovery and explicit one-call probes are implemented for Fireworks, OpenRouter, and Hugging Face Inference Providers, but no real provider calls were made in this environment.
- PostgreSQL, Qdrant and MinIO are declared in Compose but not yet connected to API persistence or retrieval. Health readiness is honest/degraded rather than a false green.
- No production authentication/authorization, account system, migrations, task queue, agent sandbox, file upload backend, malware scanner, audit database, or private per-user wallpaper storage is implemented.
- The prototype's composer records drafts locally; it does not run a task. File attach and agent selection are clearly disabled.
- Theme and wallpaper settings persist in browser localStorage only; not synced across devices.
- Frontend dependency versions are not yet locked/pinned. Neo must run `npm install`, commit `package-lock.json`, review and pin dependency versions.
- No Docker build, compose validation, provider credential check, Vultr deploy, GitHub push, restore drill, security scan, or original UI match has been performed in this environment.
- The API now reports network reachability for dependencies and reports only whether the three provider keys are present; this does not prove authenticated database operations, persistence, or successful model invocation.
- A Dockerized static frontend and Nginx API proxy have been added, but the frontend image has not been built or tested because Docker is unavailable and frontend dependencies could not be installed in this environment.
- Wallpaper controls now include position, scale, blur, dimming, chat panel opacity, and reset-to-defaults in browser-local settings. Account sync and private server-side storage remain unimplemented.
- Three asynchronous Manus workstreams were started for the interface prototype, model research, and open-source inventory. Their results are pending and must be reviewed before integration.

- Document Studio now renders PDF and editable DOCX outputs and can profile DOCX/PDF/image references. It does not yet orchestrate a source-verified 500-page manuscript job or guarantee pixel-perfect recreation; custom font embedding, durable job queue, resumability, visual comparison, and citation QA remain open.
- The model verification dry-run report lists all 101 candidates as blocked from live testing because exact IDs/provider mappings are missing and provider credentials are not configured in this environment.
- Scraper and inference acceleration projects were added as unverified candidates; none has been installed, benchmarked, or security-reviewed as part of this build.

- Added `docs/MASTER_MODEL_AND_FEATURE_QA_PROTOCOL.md` and `docs/FEATURE_AND_CODE_AUDIT_TEMPLATE.md`. These are test specifications/templates, not completed execution evidence. They include modality-specific plans, 5–10 repeat guidance, low-over-refusal evaluation, security, UI, memory/RAG, scraping, agent execution, and deployment audits.
- Added Hugging Face Inference Providers support to the server-side model probe and catalog route plus `scripts/discover_hf_models.py`. It remains untested against a live credential in this environment.
