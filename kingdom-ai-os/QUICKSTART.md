# Kingdom AI OS — Quick start (working chat build, FREE models only)

## What works in this build
- 24 named workspaces, each with its own AI assistant, which answers in that workspace's specialty
- **Free & open-source models only.** Paid models are hidden and blocked (`KAIOS_FREE_ONLY=true`)
- Open-source models run **on your own server** (Ollama: Qwen 2.5, Llama 3.2, …) — no keys, no accounts
- Optional: a free OpenRouter account key (no credit card) adds the free cloud models (`:free` + `openrouter/free`)
- Chats are saved per workspace (SQLite on the server) — History, New chat, Delete
- Model picker: every free model, local ones first
- Automatic fallback: if the chosen model fails, it tries the next free model
- Free web search with cited sources (DuckDuckGo, no key) — on by default in Research, Legal, Finance, News, etc.; toggle "Web"
- Attach PDF / Word / text / code files; their text is sent with your question
- Themes + personal background image (Appearance & settings)

## Run it on the Vultr server (one command, no keys)
```bash
cd kingdom-ai-os
docker compose -f docker-compose.simple.yml --profile local-models up -d --build
# first start downloads the models (~4 GB) — watch it with:
docker compose -f docker-compose.simple.yml logs -f ollama-pull
# open http://<server-ip>:8080
```
Server size: 8 GB RAM minimum for 3B models (16 GB+ recommended). Bigger models: `OLLAMA_PULL="qwen2.5:7b"` and `OLLAMA_DEFAULT_MODEL=qwen2.5:7b` (needs 16 GB+ or a GPU).
Add free cloud models too: put `OPENROUTER_API_KEY=sk-or-...` in front of the command.

## Check it is healthy
- `http://<server-ip>:8080/api/v1/status` → `"chat_ready": true` and `"free_only": true`
- `http://<server-ip>:8080/healthz` → `ok`

## Develop
- Backend: `cd backend && pip install -r requirements.txt && pytest -q` (32 tests, providers mocked)
- Frontend: `cd frontend && npm install && npm run build`
