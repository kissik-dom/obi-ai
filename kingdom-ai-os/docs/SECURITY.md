# Security baseline

- Never expose Fireworks/OpenRouter keys to Vite variables, browser code, URLs, client logs, or checked-in files.
- Current handoff has no production authentication; keep API bound to loopback and do not expose publicly until authN/authZ, TLS, rate limits, and audit are implemented.
- Use a secrets manager for production. Rotate any credential that was ever committed or placed in a shared document.
- Use least-privilege non-root service accounts and MinIO application credentials instead of root credentials for application access.
- Require workspace-aware authorization on every record, file, Qdrant query, task and output.
- Treat model output and uploaded files as untrusted. Validate tool calls and enforce permissions server-side.
- Experimental/low-guardrail models must run in isolated workers with no unrestricted shell, secrets, financial signing keys, or production ledger write access.
- Separate financial services and signing authority from AI execution; use human approval for consequential actions.
- Add malware scanning, file size/type limits, quotas, encrypted backups, off-site/offline copies, restore drills, immutable audit trails and security alerting before production.
- Custom wallpaper in this prototype is stored in browser localStorage. Do not use shared devices for private images; production implementation must use per-user private object storage.
