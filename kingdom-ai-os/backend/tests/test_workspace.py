"""Tests for the working chat API. The provider is mocked; no network or key needed."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import assistant


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("KAIOS_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    assistant._catalog_cache.update(at=9e18, source="test", models=[
        {"id": "google/gemini-2.5-flash", "name": "Gemini 2.5 Flash", "context": 1000000, "input_modalities": ["text", "image"], "price_in": 0.3, "price_out": 2.5, "free": False, "vision": True},
        {"id": "meta/llama:free", "name": "Llama free", "context": 8000, "input_modalities": ["text"], "price_in": 0, "price_out": 0, "free": True, "vision": False},
    ])
    return TestClient(app)


def test_status_reports_missing_key(client, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    body = client.get("/api/v1/status").json()
    assert body["chat_ready"] is False and body["database"] == "ok"


def test_catalog_filters(client):
    assert client.get("/api/v1/catalog/models").json()["total"] == 2
    assert [m["id"] for m in client.get("/api/v1/catalog/models?free=true").json()["items"]] == ["meta/llama:free"]
    assert client.get("/api/v1/catalog/models?q=gemini").json()["items"][0]["check"] == "not_run"


def test_conversation_lifecycle_and_chat(client, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    seen = {}

    async def fake_call(model_id, messages, web, max_tokens):
        seen.update(model=model_id, messages=messages, web=web)
        return {"content": "Answer [1]", "model_id": model_id, "citations": [], "usage": {"total_tokens": 5}}

    async def fake_search(q, limit=5):
        return [{"url": "https://example.org", "title": "Ex", "snippet": "facts"}]

    monkeypatch.setattr(assistant, "_call", fake_call)
    monkeypatch.setattr(assistant, "web_search", fake_search)
    conv = client.post("/api/v1/conversations", json={"tab_id": "research"}).json()
    r = client.post(f"/api/v1/conversations/{conv['id']}/messages", json={"content": "What is X?", "model_id": "meta/llama:free", "attachments": [{"name": "a.txt", "text": "file body"}]})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["assistant"]["content"] == "Answer [1]" and body["web_search"] is True
    assert body["assistant"]["citations"][0]["url"] == "https://example.org"
    assert seen["messages"][0]["role"] == "system" and "Research" in seen["messages"][0]["content"]
    assert "file body" in seen["messages"][-1]["content"]
    assert any("Web results" in m["content"] and "https://example.org" in m["content"] for m in seen["messages"])
    full = client.get(f"/api/v1/conversations/{conv['id']}").json()
    assert [m["role"] for m in full["messages"]] == ["user", "assistant"] and full["title"] == "What is X?"
    assert client.get("/api/v1/conversations?tab_id=research").json()[0]["id"] == conv["id"]
    assert client.get("/api/v1/catalog/models?q=llama").json()["items"][0]["check"] == "passed"
    assert client.delete(f"/api/v1/conversations/{conv['id']}").json() == {"deleted": True}


def test_fallback_when_first_model_fails(client, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    async def flaky(model_id, messages, web, max_tokens):
        if model_id == "bad/model":
            raise assistant.ProviderError("bad/model: HTTP 404")
        return {"content": "ok", "model_id": model_id, "citations": [], "usage": {}}

    monkeypatch.setattr(assistant, "_call", flaky)
    conv = client.post("/api/v1/conversations", json={"tab_id": "coding-dev"}).json()
    body = client.post(f"/api/v1/conversations/{conv['id']}/messages", json={"content": "hi", "model_id": "bad/model"}).json()
    assert body["fell_back"] is True and body["assistant"]["model_id"] == assistant.default_model() and body["web_search"] is False


def test_chat_without_key_is_clear(client, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    conv = client.post("/api/v1/conversations", json={"tab_id": "home"}).json()
    r = client.post(f"/api/v1/conversations/{conv['id']}/messages", json={"content": "hi"})
    assert r.status_code == 503 and "OLLAMA_BASE_URL" in r.json()["detail"]


def test_unknown_tab_rejected(client):
    assert client.post("/api/v1/conversations", json={"tab_id": "nope"}).status_code == 404


def test_extract_text_file(client):
    import base64
    r = client.post("/api/v1/files/extract", json={"name": "n.txt", "data_b64": base64.b64encode(b"hello world").decode()})
    assert r.json()["text"] == "hello world"
    assert client.post("/api/v1/files/extract", json={"name": "x.exe", "data_b64": "AA=="}).status_code == 415


def test_self_hosted_models_need_no_key(client, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://ollama:11434")
    assert client.get("/api/v1/status").json()["chat_ready"] is True
    assert assistant.default_model() == "ollama/" + assistant.OLLAMA_DEFAULT

    async def local(model_id, messages, web, max_tokens):
        assert model_id.startswith("ollama/")
        return {"content": "local answer", "model_id": model_id, "citations": [], "usage": {}}

    monkeypatch.setattr(assistant, "_call", local)
    conv = client.post("/api/v1/conversations", json={"tab_id": "tasks"}).json()
    body = client.post(f"/api/v1/conversations/{conv['id']}/messages", json={"content": "plan my day"}).json()
    assert body["assistant"]["content"] == "local answer" and body["fell_back"] is False


def test_paid_models_are_blocked_in_free_only_mode(client, monkeypatch):
    import asyncio
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    assert assistant.FREE_ONLY is True
    assert assistant.is_free("meta/llama:free") and assistant.is_free("ollama/qwen2.5:3b")
    assert not assistant.is_free("google/gemini-2.5-flash")
    with pytest.raises(assistant.ProviderError, match="paid model blocked"):
        asyncio.run(assistant._call("google/gemini-2.5-flash", [{"role": "user", "content": "hi"}], False, 10))
