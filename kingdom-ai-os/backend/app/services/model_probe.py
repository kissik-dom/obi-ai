"""Explicit, cost-bearing provider smoke tests. Never called automatically."""
from __future__ import annotations
import os
import httpx

PROVIDERS = {
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
    },
    "fireworks": {
        "base_url": "https://api.fireworks.ai/inference/v1",
        "key_env": "FIREWORKS_API_KEY",
    },
    # Hugging Face's OpenAI-compatible Inference Providers router supports chat
    # completion only. Use huggingface_hub InferenceClient for image/audio tasks.
    "huggingface": {
        "base_url": "https://router.huggingface.co/v1",
        "key_env": "HF_TOKEN",
    },
}

async def probe_model(provider: str, model_id: str) -> dict:
    provider = provider.casefold().strip()
    model_id = model_id.strip()
    if provider not in PROVIDERS:
        return {"status": "blocked", "reason": "Provider is not on the allowlist"}
    if not model_id or len(model_id) > 300 or any(ord(c) < 32 for c in model_id):
        return {"status": "blocked", "reason": "Invalid model ID"}
    config = PROVIDERS[provider]
    key = os.getenv(config["key_env"], "").strip()
    if not key:
        return {"status": "blocked", "reason": f"{config['key_env']} is not configured"}
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if provider == "openrouter":
        headers["HTTP-Referer"] = "https://kingdom-ai-os.local"
        headers["X-Title"] = "Kingdom AI OS model verification"
    payload = {"model": model_id, "messages": [{"role": "user", "content": "Reply with exactly: KAIOS_OK"}], "max_tokens": 12, "temperature": 0}
    try:
        async with httpx.AsyncClient(timeout=25.0, follow_redirects=False) as client:
            response = await client.post(config["base_url"] + "/chat/completions", headers=headers, json=payload)
        if response.status_code < 200 or response.status_code >= 300:
            # Do not echo provider response bodies; they can contain sensitive diagnostics.
            return {"status": "failed", "http_status": response.status_code, "reason": "Provider rejected the request; inspect provider console for details"}
        data = response.json()
        choices = data.get("choices") or []
        content = (((choices[0] or {}).get("message") or {}).get("content")) if choices else None
        if not isinstance(content, str) or not content.strip():
            return {"status": "failed", "http_status": response.status_code, "reason": "Provider returned no text response"}
        return {"status": "passed", "provider": provider, "model_id": model_id, "http_status": response.status_code, "response_received": True, "response_text": content[:200]}
    except httpx.TimeoutException:
        return {"status": "failed", "reason": "Provider request timed out"}
    except (httpx.HTTPError, ValueError):
        return {"status": "failed", "reason": "Provider connection or response parsing failed"}


async def list_provider_models(provider: str) -> dict:
    provider = provider.casefold().strip()
    if provider not in PROVIDERS:
        return {"status": "blocked", "reason": "Provider is not on the allowlist", "models": []}
    config = PROVIDERS[provider]
    key = os.getenv(config["key_env"], "").strip()
    if not key:
        return {"status": "blocked", "reason": f"{config['key_env']} is not configured", "models": []}
    headers = {"Authorization": f"Bearer {key}"}
    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=False) as client:
            response = await client.get(config["base_url"] + "/models", headers=headers)
        if response.status_code < 200 or response.status_code >= 300:
            return {"status": "failed", "http_status": response.status_code, "reason": "Provider model catalog request failed", "models": []}
        body = response.json()
        items = body.get("data", []) if isinstance(body, dict) else []
        models = []
        for item in items[:1000]:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                models.append({"id": item["id"], "name": item.get("name"), "context_length": item.get("context_length")})
        return {"status": "passed", "provider": provider, "count_returned": len(models), "models": models}
    except (httpx.HTTPError, ValueError):
        return {"status": "failed", "reason": "Provider connection or response parsing failed", "models": []}


async def chat_completion(provider: str, model_id: str, messages: list[dict], max_tokens: int = 2048) -> dict:
    provider = provider.casefold().strip()
    if provider not in PROVIDERS:
        raise ValueError("Provider is not on the allowlist")
    config = PROVIDERS[provider]
    key = os.getenv(config["key_env"], "").strip()
    if not key:
        raise RuntimeError("Provider API key is not configured")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if provider == "openrouter":
        headers["HTTP-Referer"] = "https://kingdom-ai-os.local"
        headers["X-Title"] = "Kingdom AI OS"
    payload = {"model": model_id, "messages": messages, "max_tokens": max_tokens}
    try:
        async with httpx.AsyncClient(timeout=120.0, follow_redirects=False) as client:
            response = await client.post(config["base_url"] + "/chat/completions", headers=headers, json=payload)
        if response.status_code < 200 or response.status_code >= 300:
            raise RuntimeError(f"Provider returned HTTP {response.status_code}")
        body = response.json()
        choices = body.get("choices") or []
        content = (((choices[0] or {}).get("message") or {}).get("content")) if choices else None
        if not isinstance(content, str):
            raise RuntimeError("Provider returned no text response")
        return {"content": content, "provider": provider, "model_id": model_id, "usage": body.get("usage")}
    except httpx.TimeoutException as exc:
        raise RuntimeError("Provider request timed out") from exc
    except httpx.HTTPError as exc:
        raise RuntimeError("Provider connection failed") from exc
