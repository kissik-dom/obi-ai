# Security

## Phase 0 — do this first
1. **Rotate every credential that may have been exposed during intake.** Treat all previously used API keys and tokens as compromised and rotate now.
2. Enable 2FA on the GitHub account; protect `main` (require PR review).
3. Put TLS in front of everything (Caddy auto-provisions once DNS points at the host). The server currently serves plain HTTP.

## Secrets
- `.env` is gitignored and never committed. Use `.env.example` as the template.
- Production secrets belong in a broker (OpenBao/Vault), not in the repo. Agents receive references, never raw keys.
- `TASK_API_KEYS` is a workspace-to-bearer-token map. The task service uses it to scope `/tasks` reads to the authenticated workspace.

## Reporting
Open a private security advisory on this repo. Do not file secrets or exploit details in public issues.
