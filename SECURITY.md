# Security

## Phase 0 — do this first
1. **Rotate every exposed credential.** The intake album screenshots leak API keys and a GitHub PAT. Treat them all as compromised and rotate now.
2. Enable 2FA on the GitHub account; protect `main` (require PR review).
3. Put TLS in front of everything (Caddy auto-provisions once DNS points at the host). The server currently serves plain HTTP.

## Secrets
- `.env` is gitignored and never committed. Use `.env.example` as the template.
- Production secrets belong in a broker (OpenBao/Vault), not in the repo. Agents receive references, never raw keys.

## Reporting
Open a private security advisory on this repo. Do not file secrets or exploit details in public issues.
