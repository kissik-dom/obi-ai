# Connect GitHub (`YOURNAME/kingdom-ai-os`) to Vultr GPU Server

## 1. Repository & Branch Topology
- **Canonical GitHub Repository**: `https://github.com/YOURNAME/kingdom-ai-os`
- **Protected Production Branch**: `main` (auto-deploys to Vultr ONLY after `test.yml` passes 100%)
- **Active Development Branch**: `dev` (all feature PRs and autonomous agent patches target `dev` first)

## 2. Configure GitHub Actions Secrets
In your GitHub repository, navigate to **Settings -> Secrets and variables -> Actions** and add:

| Secret Name | Purpose |
| :--- | :--- |
| `VULTR_HOST` | Public IPv4 or WireGuard management IP of your Vultr GPU instance |
| `VULTR_USER` | SSH user (`root` or `kingdom`) |
| `VULTR_SSH_KEY` | Ed25519 private key (`ssh-keygen -t ed25519 -C "github-actions-vultr"`) |
| `VULTR_API_KEY` | Optional Vultr v2 API key for `vultr_deploy.sh --provision` |

## 3. Provision Your Vultr GPU Node (`ewr` / `vcg-a100-1c-8g-40vram`)
```bash
export VULTR_API_KEY="your-vultr-v2-api-key"
chmod +x vultr_deploy.sh
./vultr_deploy.sh --provision
```
`vultr_cloud_init.yaml` automatically installs Docker Engine, NVIDIA Container Toolkit, WireGuard (`51820/udp`), UFW rules, clones the repository into `/opt/kingdom-ai-os`, and launches the full Compose stack.

## 4. Populate `.env` & Vault HSM Secrets on Vultr
SSH into the Vultr server:
```bash
ssh root@YOUR_VULTR_IP
cd /opt/kingdom-ai-os
cp -n .env.example .env
nano .env   # Add OPENROUTER_API_KEY_1..10 and rotate KINGDOM_INTERNAL_SECRET
./vultr_deploy.sh
```
Never store financial private keys in `.env`; enroll them directly into HashiCorp Vault HSM (`http://127.0.0.1:8200`).

## 5. Continuous Verification & Zero-Downtime Rollout
1. Open a Pull Request into `dev` -> `.github/workflows/test.yml` runs `pytest tests/` + `npm run build`.
2. Merge `dev` into `main` -> `.github/workflows/deploy.yml` re-runs verification and SSH-deploys `/opt/kingdom-ai-os` on Vultr, rolling back automatically if `/healthz` fails.
