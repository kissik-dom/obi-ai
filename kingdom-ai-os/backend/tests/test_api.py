import asyncio
from fastapi.testclient import TestClient
import app.main as main
from app.main import app

client = TestClient(app)


def test_liveness():
    r = client.get("/health/live")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_security_headers_present():
    r = client.get("/health/live")
    assert r.headers["x-content-type-options"] == "nosniff"
    assert r.headers["x-frame-options"] == "DENY"
    assert r.headers["referrer-policy"] == "no-referrer"


def test_tabs_have_28_entries_and_unmapped_are_explicit():
    r = client.get("/api/v1/tabs")
    assert r.status_code == 200 and len(r.json()) == 28
    assert sum(1 for tab in r.json() if tab["id"].startswith("unmapped-")) == 4


def test_models_are_unverified_until_reviewed():
    r = client.get("/api/v1/models")
    body = r.json()
    assert r.status_code == 200 and body["total"] >= 30
    assert all(m["status"] == "UNVERIFIED" for m in body["items"])
    assert all(m.get("exact_provider_model_id") is None for m in body["items"])


def test_model_registry_search_and_pagination():
    all_models = client.get("/api/v1/models?limit=500").json()
    assert all_models["total"] >= len(all_models["items"])
    if all_models["items"]:
        name = all_models["items"][0]["name"]
        found = client.get("/api/v1/models", params={"q": name, "limit": 1}).json()
        assert found["total"] >= 1
        assert found["items"][0]["name"] == name


def test_project_registry_search_and_pagination():
    body = client.get("/api/v1/projects?limit=5&offset=0").json()
    assert body["total"] >= len(body["items"])
    assert len(body["items"]) <= 5


def test_unverified_model_cannot_be_invoked():
    r = client.post("/api/v1/chat", json={"model_name": "Qwen3.8-27B", "message": "Hello"})
    assert r.status_code == 409
    assert "not sent to a provider" in r.json()["detail"]


def test_unknown_model_returns_404():
    r = client.post("/api/v1/chat", json={"model_name": "Definitely-Not-A-Model", "message": "Hello"})
    assert r.status_code == 404


def test_provider_status_never_returns_secrets(monkeypatch):
    monkeypatch.setenv("FIREWORKS_API_KEY", "synthetic-fireworks-secret")
    monkeypatch.setenv("OPENROUTER_API_KEY", "synthetic-openrouter-secret")
    monkeypatch.setenv("HF_TOKEN", "synthetic-hf-secret")
    response = client.get("/api/v1/system/providers")
    body = response.text
    assert response.status_code == 200
    assert "synthetic-fireworks-secret" not in body
    assert "synthetic-openrouter-secret" not in body
    assert "synthetic-hf-secret" not in body
    assert body.count('"configured":true') == 3


def test_dependency_status_never_exposes_secrets(monkeypatch):
    async def fake_report():
        return {"api": "ok", "database": "unavailable", "qdrant": "unavailable", "minio": "unavailable", "litellm": "unavailable"}
    monkeypatch.setattr(main, "dependency_report", fake_report)
    body = client.get("/api/v1/system/dependencies").text
    for key in ("FIREWORKS_API_KEY", "OPENROUTER_API_KEY", "KINGDOM_INTERNAL_SECRET"):
        assert key not in body


def test_pdf_renderer_outputs_real_pdf_with_signature_footer():
    from pypdf import PdfReader
    import io
    response = client.post('/api/v1/documents/render-pdf', json={
        'title': 'Test Book', 'subtitle': 'A test subtitle', 'author': 'QA',
        'font': 'Times-Roman', 'page_size': 'A4', 'footer_quote': 'Evidence matters.',
        'include_contents': True,
        'sections': [{'title': 'Chapter One', 'body': 'A paragraph of sample text.\n\nA second paragraph.'}],
        'glossary': [{'term': 'Evidence', 'definition': 'Information used to support a claim.'}]
    })
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/pdf'
    reader = PdfReader(io.BytesIO(response.content))
    assert len(reader.pages) >= 3
    text = '\n'.join(page.extract_text() or '' for page in reader.pages)
    assert 'Test Book' in text and 'Glossary' in text and 'Evidence' in text
    assert all('Evidence matters.' in (page.extract_text() or '') for page in reader.pages)


def test_pdf_renderer_rejects_missing_sections():
    response = client.post('/api/v1/documents/render-pdf', json={'title': 'Empty Book', 'sections': []})
    assert response.status_code == 422


def test_template_profile_rejects_unsupported_format():
    import base64
    response = client.post('/api/v1/documents/template-profile', json={
        'filename': 'bad.exe', 'content_base64': base64.b64encode(b'not an exe').decode()
    })
    assert response.status_code == 415


def test_registry_change_is_validated_but_never_applied():
    response = client.post('/api/v1/registry/changes/validate', json={
        'registry': 'open_source_projects', 'operation': 'propose_add',
        'record': {'name_as_written': 'Test-only crawler'}, 'reason': 'QA validation of a candidate tool.'
    })
    assert response.status_code == 200
    body = response.json()
    assert body['valid'] is True and body['applied'] is False and body['requires_approval'] is True
    assert body['proposed_record']['open_source_status'] == 'UNVERIFIED'


def test_registry_duplicate_add_rejected():
    rows = client.get('/api/v1/projects?limit=1').json()['items']
    record = rows[0]
    response = client.post('/api/v1/registry/changes/validate', json={
        'registry': 'open_source_projects', 'operation': 'propose_add',
        'record': record, 'reason': 'Testing duplicate prevention in registry intake.'
    })
    assert response.status_code == 409


def test_live_model_probe_requires_explicit_cost_confirmation():
    response = client.post('/api/v1/system/model-probe', json={
        'provider': 'openrouter', 'model_id': 'some/model', 'confirm_provider_cost': False
    })
    assert response.status_code == 400


def test_document_template_catalog_has_reusable_presets():
    response = client.get('/api/v1/documents/templates')
    assert response.status_code == 200
    ids = {row['id'] for row in response.json()}
    assert {'royal-gold-book', 'academic-research-paper', 'legal-memorandum', 'reference-recreation'} <= ids


def test_template_profile_extracts_docx_style_profile():
    import base64, io
    from docx import Document
    doc = Document()
    doc.add_heading('Reference Heading', level=1)
    doc.add_paragraph('Sample body text for template profiling.')
    output = io.BytesIO(); doc.save(output)
    response = client.post('/api/v1/documents/template-profile', json={
        'filename': 'reference.docx', 'content_base64': base64.b64encode(output.getvalue()).decode()
    })
    assert response.status_code == 200
    body = response.json()
    assert 'Heading 1' in body['paragraph_styles']
    assert body['stored'] is False


def test_verified_model_chat_calls_adapter(monkeypatch):
    async def fake_chat(provider, model_id, messages, max_tokens):
        assert provider == 'fireworks'
        assert model_id == 'accounts/demo/models/verified-model'
        assert messages[0]['content'] == 'Hello'
        return {'content': 'KAIOS_OK', 'usage': {'total_tokens': 3}}
    monkeypatch.setattr(main, 'read_json', lambda name: [{
        'name': 'Verified Test Model', 'status': 'VERIFIED',
        'exact_provider_model_id': 'accounts/demo/models/verified-model', 'provider_family': 'Fireworks'
    }] if name == 'models.json' else [])
    monkeypatch.setattr(main, 'chat_completion', fake_chat)
    response = client.post('/api/v1/chat', json={'model_name': 'Verified Test Model', 'message': 'Hello'})
    assert response.status_code == 200
    assert response.json()['content'] == 'KAIOS_OK'


def test_docx_renderer_outputs_editable_word_document():
    import io
    from docx import Document
    response = client.post('/api/v1/documents/render-docx', json={
        'title': 'Editable Book', 'sections': [{'title': 'Chapter A', 'body': 'Body text.'}],
        'glossary': [{'term': 'Word', 'definition': 'A term.'}], 'footer_quote': 'A quote.'
    })
    assert response.status_code == 200
    doc = Document(io.BytesIO(response.content))
    text = '\n'.join(p.text for p in doc.paragraphs)
    assert 'Editable Book' in text and 'Chapter A' in text and 'Glossary' in text
    assert 'A quote.' in doc.sections[0].footer.paragraphs[0].text


def test_pdf_renderer_handles_500_page_manuscript_stress_case():
    import io
    from pypdf import PdfReader
    from app.services.documents import render_pdf
    paragraph = ('This is a controlled renderer stress test. It verifies pagination and layout only, not factual content. ' * 7)[:690]
    sections = [{'title': f'Chapter {i+1}', 'body': '\n\n'.join([paragraph] * 11)} for i in range(250)]
    payload = render_pdf({'title': 'Long Document Stress Test', 'sections': sections,
                          'include_contents': True, 'include_glossary': True,
                          'footer_quote': 'Evidence matters.', 'glossary': []})
    reader = PdfReader(io.BytesIO(payload))
    assert len(reader.pages) >= 500
    assert 'Evidence matters.' in (reader.pages[0].extract_text() or '')
    assert 'Evidence matters.' in (reader.pages[-1].extract_text() or '')
    all_text = '\n'.join((page.extract_text() or '') for page in reader.pages[-3:])
    assert 'Glossary' in all_text and 'Glossary terms have not yet been supplied' in all_text


def test_huggingface_provider_catalog_route_is_allowlisted(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    response = client.get("/api/v1/system/provider-models?provider=huggingface")
    assert response.status_code == 200
    assert response.json()["status"] == "blocked"
    assert response.json()["reason"] == "HF_TOKEN is not configured"


def test_unknown_provider_catalog_is_rejected():
    response = client.get("/api/v1/system/provider-models?provider=unknown")
    assert response.status_code == 422
