# Obi AI — Centillion OS-AI

Private. Hermes agent swarm chatbot on the Obliteratus multi-provider cascade.

- Obliteratus Hermes Gateway: never-fail LLM cascade (SambaNova → OpenRouter → HuggingFace → Gemini), OpenAI-compatible at /api/gateway/chat/completions
- 14-agent Hermes swarm (router + specialists), web search, deep-research ensemble
- Voice-to-text, image/video/file uploads (optional Vercel Blob)
- Next.js 14, deployed as a Docker service on Vultr

## Deployment
See [`VULTR_DEPLOY.md`](./VULTR_DEPLOY.md) for the Docker Compose deployment.

## Env
See `.env.example`. Provider keys belong in the Vultr server's untracked `.env` file and are never committed.
