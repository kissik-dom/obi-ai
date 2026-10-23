# Kingdom AI OS — Pure API-Only Deployment & Secrets Guide (Zero SSH / Zero Vultr Key)

This repository is now **100% Pure Headless API-Only** (no React/Node frontend build, zero SSH, zero Vultr GPU required).

---

## 1. Key API Endpoints Once Deployed

| Endpoint | Purpose |
| :--- | :--- |
| `GET /` | JSON API Root Manifest & live registry counts |
| `GET /docs` | Interactive OpenAPI / Swagger UI (test any endpoint or seal keys right in browser) |
| `GET /healthz` | Healthcheck (`healthy` \| `degraded` \| `offline`) |
| `GET /v1/models` | **OpenAI-compatible** list of all 205 Sovereign LLMs |
| `POST /v1/chat/completions` | **OpenAI-compatible** Chat Completions gateway (also aliased at `/api/gateway/chat/completions`) |
| `POST /api/vault/llm-keys` | Seal OpenRouter / Obliteratus / Composio keys into Vault HSM via HTTP API or `/docs` |
| `GET/POST /api/tabs/{tab}/*` | Full 10-endpoint Sovereign Grammar across all 24 -> 28+ tabs |
| `POST /api/requests` | Quick Request sandbox (`s3://kingdom-requests/{sandbox_id}/`) |
| `GET /api/finished` | Finished Folder archive (`s3://kingdom-finished/{sandbox_id}/`) |

---

## 2. Which Secrets to Insert (Only 1 Required, 2 Optional)

In your API host's **Environment Variables** web screen (Vercel / Railway / Render) — **never in chat**:

| Variable Name | Required? | Purpose |
| :--- | :--- | :--- |
| `OPENROUTER_API_KEY_1` | **Required for live cloud LLMs** | Your OpenRouter API key (`sk-or-v1-...` from [openrouter.ai/keys](https://openrouter.ai/keys)). Add `_2`..`_10` only if you want multi-key rotation. |
| `KINGDOM_API_KEY` | Optional | If set (e.g. `sk-my-secret-api-key`), `/v1/chat/completions` requires `Authorization: Bearer <KINGDOM_API_KEY>` so nobody else can use your API. |
| `OBLITERATUS_API_KEY` | Optional | Only if routing through your own Obliteratus Hermes gateway (`OBLITERATUS_GATEWAY_URL`). |

*(You can also seal `OPENROUTER_API_KEY_1` live via `POST /api/vault/llm-keys` right inside Swagger `/docs` -> **`POST /api/vault/llm-keys` -> Try it out -> Execute**!)*

---

## 3. Deploy API-Only in 60 Seconds From Browser (No SSH, No Vultr)

Pick **any** of these 3 browser platforms connected to GitHub repo **`kissik-dom/obi-ai`** (branch `arena/41e9ebf0-obi-ai`, or merge the PR into `main` on GitHub):

1. **Vercel (Zero-Config Python Serverless API — `vercel.json` + `api/index.py` included)**:
   - Open **[vercel.com/new](https://vercel.com/new)** -> Import **`kissik-dom/obi-ai`**.
   - Expand **Environment Variables** -> add `OPENROUTER_API_KEY_1` (and optional `KINGDOM_API_KEY`).
   - Tap **Deploy** -> Instant `https://your-project.vercel.app/v1/chat/completions` & `/docs`!

2. **Railway.app (Persistent Container API — `Dockerfile` + `railway.json` included)**:
   - Open **[railway.app](https://railway.app)** -> **New Project -> Deploy from GitHub repo** -> **`kissik-dom/obi-ai`**.
   - Add `OPENROUTER_API_KEY_1` under **Variables** and tap **Settings -> Networking -> Generate Domain**.

3. **Render.com (1-Click API Blueprint — `render.yaml` included)**:
   - Open **[dashboard.render.com](https://dashboard.render.com)** -> **New + -> Blueprint** -> **`kissik-dom/obi-ai`**.
   - Paste `OPENROUTER_API_KEY_1` when prompted (`KINGDOM_API_KEY`, `KINGDOM_INTERNAL_SECRET`, `LITELLM_MASTER_KEY`, and `VAULT_TOKEN` auto-generate automatically).
