# Kingdom AI OS — engineering handoff for Neo (Vultr, two provider keys)

This package is a **reviewable implementation foundation**, not a finished or deployed product. It includes a React/Vite UI prototype with six themes and custom wallpaper controls, a FastAPI API, two-key provider configuration, registries seeded from the supplied Voltaire mapping and older Library model catalog, tests, CI, and a release checklist. It does not claim all models/projects/tabs work.

## Scope confirmed from the source mapping
- Hosting target: **Vultr**.
- Provider credentials: **one Fireworks API key and one OpenRouter API key**. No ten-key slots. Never place either key in the frontend.
- 24 tab names are listed in the source mapping; four more tabs are required by the latest request but not named in that mapping. They are explicitly marked `UNMAPPED TAB 25–28` until the canonical names are supplied/located.
- Candidate model/project names are preserved as unverified intake records. The mapping includes names whose provider IDs, availability, licenses, and open-source status have not been established.
- Appearance themes: white colorful, white orange, pink colorful, magenta colorful, lavender colorful, dark. Wallpaper upload supports JPG/PNG/WebP up to 5 MB, with position, scale, blur, dimming, chat opacity, and reset controls. It is stored in browser localStorage for this demo and is **not** account-synced or suitable for sensitive/private images in a shared browser profile. Production should store per-user wallpapers in private object storage with authorization and retention controls.

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

## Run backend tests locally
```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --port 8000
```

## Docker validation
Copy `.env.example` to `.env`, replace every placeholder with real unique secrets, then run `docker compose config`. Do not use the example values in a real deployment. Start with `docker compose up --build -d` only after the config check. Production deploy must use reviewed/pinned images, TLS, authentication, least-privilege storage credentials, backups, and firewall restrictions.

## Provider setup
The app's provider keys are read only by the backend. Model IDs must be confirmed against each provider's current catalog and account permissions before chat routing is enabled. The initial catalog intentionally shows candidate names as UNVERIFIED. Do not infer provider availability from a model name. The chat route now invokes only records explicitly marked `VERIFIED` with an exact provider model ID and a supported provider mapping. All current seed records remain unverified, so no candidate is assumed callable. Live provider catalog discovery and an explicitly authorized one-request probe are available through the API and UI.

## Document Studio and extensibility
- PDF and editable DOCX render endpoints support title pages, section headings, a contents list, page-number fields, a gold-line/diamond footer motif, footer quote on every page, glossary section by default, optional references, page size, margins, and reusable document presets. PDF rendering supports the built-in Times/Helvetica/Courier families; exact custom-font embedding is not yet implemented.
- DOCX/PDF/image template profiling extracts basic styles, page geometry, text samples, font samples, or image dimensions/palette without storing the source. This is not a promise of pixel-perfect reproduction.
- Registry-change validation produces a proposal and duplicate check but does not apply it. Authenticated approval, audit log, versioned mutation, and rollback remain production requirements.
- `scripts/probe_models.py` produces a dry-run report by default. `--execute` makes provider requests and may incur charges; only exact IDs already recorded and confirmed in the live provider catalog are probed.

## Test status
- Automated local tests in `backend/tests` are intended to verify API liveness, registry status behavior, and secret non-disclosure. Run them and retain the actual output.
- CI validates backend tests and frontend build. CI passing is not evidence that provider credentials, Vultr deployment, every tab, every model, or all 600+ projects have been tested.
- The accessible Library source packages include architecture and tab guides but no original chatbot UI source; the v4 scaffold has an empty `apps/web` directory. This UI is a fresh prototype, not a verified visual match to the original interface. Source documents are included under `docs/source-references/`. Neo should compare it with the original asset before accepting the frontend.

## Neo review gates
See `docs/NEO_REVIEW_CHECKLIST.md`, `docs/SECURITY.md`, `docs/TEST_PLAN.md`, `docs/VULTR_DEPLOYMENT.md`, and `docs/AGENT_TASKS.md` for the parallel research/interface workstreams. Do not merge/deploy with unresolved critical/high findings, secret placeholders, unverified production model IDs, or missing backup/restore evidence.

## Reproducible validation

From the repository root, install the backend requirements and run:

```sh
pip install -r backend/requirements.txt
./scripts_validate.sh
```

The script validates registry JSON structure, duplicate identifiers, tab count, YAML syntax, Python compilation, and backend API tests. It does **not** prove external provider access, Docker image health, full database persistence, security certification, or production readiness.

## Generate local environment secrets

```sh
./scripts/generate-secrets.sh
```

This refuses to overwrite an existing `.env`, creates random service secrets with file permissions `0600`, and leaves the two provider keys blank. Add `FIREWORKS_API_KEY` and `OPENROUTER_API_KEY` only in the server-side `.env` or an approved secret manager. Never commit `.env` or place provider keys in frontend variables.

## Independent QA and model verification

- [Master model and modality test protocol](docs/MASTER_MODEL_AND_FEATURE_QA_PROTOCOL.md)
- [Reusable code, feature, security, and deployment audit template](docs/FEATURE_AND_CODE_AUDIT_TEMPLATE.md)
- [Model verification workflow and status definitions](docs/MODEL_VERIFICATION.md)
- [Current QA work log and known limitations](docs/QA_WORK_LOG_2026-10-28.md)

For Hugging Face Inference Providers, configure `HF_TOKEN` server-side or as a GitHub Actions secret. `python scripts/discover_hf_models.py` discovers the live chat catalog (catalog only). `python scripts/probe_one_model.py --provider huggingface --model-id 'EXACT_ID_FROM_CATALOG' --execute` sends one explicitly authorized request that may incur charges. A manual GitHub workflow is also available at **Actions → Manual live model smoke test**. Use **Actions → Manual provider catalog discovery** to produce a downloadable catalog artifact without running inference. Catalog discovery and a smoke test do not constitute quality verification.
