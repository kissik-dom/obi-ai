# Kingdom AI OS — Quick start (working chat build)

## What works in this build
- 24 named workspaces, each with its own AI assistant, which answers in that workspace's specialty
- Chats are saved per workspace (SQLite on the server) — History, New chat, Delete
- Live model picker: every OpenRouter model (search, free-only filter, prices, context, vision)
- Automatic fallback: if the chosen model fails, it tries google/gemini-2.5-flash → openai/gpt-4o-mini → deepseek/deepseek-v4.1-flash
- Web search with cited sources (on by default in Research, Legal, Finance, News, etc.; toggle "Web")
- Attach PDF / Word / text / code files; their text is sent with your question
- Themes + personal background image (Appearance & settings)
- Document Studio (PDF/DOCX), model test, and registry tools from the previous build

## Run it on the Vultr server (one command)
```bash
cd kingdom-ai-os
OPENROUTER_API_KEY=sk-or-... docker compose -f docker-compose.simple.yml up -d --build
# open http://<server-ip>:8080
```
Optional: `KAIOS_DEFAULT_MODEL=<openrouter model id>` and `FRONTEND_PORT=<port>`.

## Check it is healthy
- `http://<server-ip>:8080/api/v1/status` → `"chat_ready": true` means the key is loaded
- `http://<server-ip>:8080/healthz` → `ok`

## Develop
- Backend: `cd backend && pip install -r requirements.txt && pytest -q` (30 tests, provider mocked)
- Frontend: `cd frontend && npm install && npm run build`
