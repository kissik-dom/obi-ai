# Deploy Kingdom AI OS (With or Without a Vultr API Key)

You **do NOT need `VULTR_API_KEY`** to run or deploy Kingdom AI OS. Choose whichever option fits what you have right now:

---

## Option A: Deploy on Vultr WITHOUT `VULTR_API_KEY` (Dashboard Click-Through)
`VULTR_API_KEY` was only for optional command-line server creation (`--provision`). You can skip it completely:

1. Log in to **https://my.vultr.com/** and click **Deploy + -> Deploy New Server**.
2. Choose **Cloud GPU** (NVIDIA A100) *or* **Cloud Compute / Optimized Cloud** (CPU works too via OpenRouter).
3. Select **Ubuntu 24.04 x64**, select your SSH key, and click **Deploy Now**.
4. Once it boots, SSH into the server IP and run:
   ```bash
   git clone https://github.com/kissik-dom/obi-ai.git /opt/kingdom-ai-os
   cd /opt/kingdom-ai-os
   chmod +x quickstart_setup.sh
   ./quickstart_setup.sh --env-only
   nano .env          # Only paste OPENROUTER_API_KEY_1 (and OPENROUTER_API_KEY); all internal passwords are already auto-generated!
   ./quickstart_setup.sh
   ```
   `quickstart_setup.sh` automatically detects whether an NVIDIA GPU is attached and starts the matching Docker stack.

*(Tip: If you ever want a `VULTR_API_KEY` later, it lives in `my.vultr.com` -> left sidebar **Account** -> **API** tab -> **Enable API** -> **Allow All IPv4**.)*

---

## Option B: No Vultr Account Needed — Run Locally or on Any VPS (Mac / Windows WSL2 / Linux / RunPod / Hetzner / DigitalOcean)
You can run the entire 28-tab OS right now on your own computer or any other host with **zero cloud keys** (or just 1 `OPENROUTER_API_KEY`):

```bash
git clone https://github.com/kissik-dom/obi-ai.git
cd obi-ai
chmod +x quickstart_setup.sh
./quickstart_setup.sh
```
- **What `quickstart_setup.sh` auto-generates for you** (so you don't have to invent them):
  - `KINGDOM_INTERNAL_SECRET`
  - `LITELLM_MASTER_KEY`
  - `POSTGRES_PASSWORD` & `DATABASE_URL`
  - `MINIO_ROOT_PASSWORD`
  - `VAULT_TOKEN`
  - `LISTMONK_ADMIN_PASS`
- **The ONLY key you optionally add in `.env`**:
  - `OPENROUTER_API_KEY_1=sk-or-v1-...` (and `OPENROUTER_API_KEY=sk-or-v1-...`) from [openrouter.ai/keys](https://openrouter.ai/keys) to unlock live cloud LLM completions across all 205 models (and up to `_2`..`_10` if you want 10-key rotation). Even without OpenRouter keys, the UI (`:5173`), Swagger API (`:8000/docs`), Qdrant 768d, MinIO buckets, Vault HSM, and Sovereign Local Engine run out-of-the-box.

---

## Option C: Connect GitHub Auto-Deploy Later (Still No `VULTR_API_KEY` Needed!)
`.github/workflows/deploy.yml` deploys over **SSH**, so it **never needs `VULTR_API_KEY`** — it only uses 3 GitHub Actions secrets (`Settings -> Secrets and variables -> Actions`) pointing to **any** Linux server IP (Vultr or otherwise):

| GitHub Secret | Purpose |
| :--- | :--- |
| `VULTR_HOST` | IP address of your server (Vultr, RunPod, Hetzner, DigitalOcean, etc.) |
| `VULTR_USER` | SSH username (e.g. `root` or `ubuntu`) |
| `VULTR_SSH_KEY` | Private SSH key matching `~/.ssh/authorized_keys` on that server |
