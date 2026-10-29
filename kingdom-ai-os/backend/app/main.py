from __future__ import annotations

import asyncio
import json
import os
import socket
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi.responses import Response
from app.services.documents import render_pdf, render_docx
from app.services.model_probe import probe_model, list_provider_models, chat_completion
import base64
import io
import zipfile
from app.routes_workspace import router as workspace_router

HERE = Path(__file__).resolve()
ROOT = next((parent for parent in HERE.parents if (parent / "registries").is_dir()), HERE.parents[2])
REGISTRY = ROOT / "registries"
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
APP_ENV = os.getenv("APP_ENV", "development")


def read_json(name: str) -> list[dict[str, Any]]:
    path = REGISTRY / name
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Registry {name} must contain a JSON array")
    return payload


app = FastAPI(
    title=os.getenv("APP_NAME", "Kingdom AI OS API"),
    version="0.3.0",
    docs_url="/docs" if APP_ENV != "production" else None,
    redoc_url=None,
)
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-Request-ID"],
)
app.include_router(workspace_router)


@app.middleware("http")
async def secure_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Cache-Control"] = "no-store" if request.url.path.startswith(API_PREFIX) else "no-cache"
    return response


@app.exception_handler(Exception)
async def generic_error(request, exc):
    # Do not return exception details, credentials, or internal URLs to clients.
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health/live")
async def live():
    return {"status": "ok"}


async def tcp_check(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except (OSError, asyncio.TimeoutError):
        return False


async def http_check(url: str, headers: dict[str, str] | None = None) -> bool:
    try:
        async with httpx.AsyncClient(timeout=2.5, follow_redirects=False) as client:
            response = await client.get(url, headers=headers)
        return 200 <= response.status_code < 300
    except (httpx.HTTPError, ValueError):
        return False


async def dependency_report() -> dict[str, str]:
    database_url = os.getenv("DATABASE_URL", "")
    db = urlparse(database_url.replace("postgresql+psycopg://", "postgresql://", 1))
    if db.hostname and db.port:
        database_ok = await tcp_check(db.hostname, db.port)
    else:
        database_ok = False

    qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333").rstrip("/")
    qdrant_headers = {"api-key": os.getenv("QDRANT_API_KEY", "")} if os.getenv("QDRANT_API_KEY") else None
    qdrant_ok = await http_check(f"{qdrant_url}/healthz", qdrant_headers)

    minio_endpoint = os.getenv("MINIO_ENDPOINT", "minio:9000")
    minio_scheme = os.getenv("MINIO_SCHEME", "http")
    minio_ok = await http_check(f"{minio_scheme}://{minio_endpoint}/minio/health/ready")

    litellm_url = os.getenv("LITELLM_BASE_URL", "http://litellm:4000").rstrip("/")
    litellm_ok = await http_check(f"{litellm_url}/health/liveliness", {"Authorization": f"Bearer {os.getenv('LITELLM_MASTER_KEY', '')}"})
    return {
        "api": "ok",
        "database": "reachable" if database_ok else "unavailable",
        "qdrant": "reachable" if qdrant_ok else "unavailable",
        "minio": "reachable" if minio_ok else "unavailable",
        "litellm": "reachable" if litellm_ok else "unavailable",
    }


@app.get("/health/ready")
async def ready():
    checks = await dependency_report()
    ok = all(value in {"ok", "reachable"} for value in checks.values())
    return JSONResponse(status_code=200 if ok else 503, content={"status": "ready" if ok else "degraded", "checks": checks})


@app.get(f"{API_PREFIX}/system/version")
async def version():
    return {"name": app.title, "version": app.version, "environment": APP_ENV}


@app.get(f"{API_PREFIX}/system/dependencies")
async def dependencies():
    return await ready()


@app.get(f"{API_PREFIX}/system/providers")
async def providers():
    # Report presence only; never return provider secrets or their lengths.
    fireworks = bool(os.getenv("FIREWORKS_API_KEY", "").strip())
    openrouter = bool(os.getenv("OPENROUTER_API_KEY", "").strip())
    huggingface = bool(os.getenv("HF_TOKEN", "").strip())
    return {
        "policy": "provider_secrets_presence_only",
        "providers": [
            {"id": "fireworks", "configured": fireworks, "invocation": "disabled_until_model_id_verified"},
            {"id": "openrouter", "configured": openrouter, "invocation": "enabled_via_workspace_chat" if openrouter else "needs_api_key"},
            {"id": "huggingface", "configured": huggingface, "invocation": "disabled_until_model_id_verified"},
            {"id": "ollama_self_hosted", "configured": bool(os.getenv("OLLAMA_BASE_URL", "").strip()), "invocation": "enabled_via_workspace_chat"},
        ],
    }


@app.get(f"{API_PREFIX}/tabs")
async def tabs():
    return read_json("tabs.json")


@app.get(f"{API_PREFIX}/models")
async def models(
    status: str | None = None,
    q: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    rows = read_json("models.json")
    if status:
        rows = [r for r in rows if str(r.get("status", "")).casefold() == status.casefold()]
    if q:
        needle = q.casefold()
        rows = [r for r in rows if needle in json.dumps(r, ensure_ascii=False).casefold()]
    return {"total": len(rows), "items": rows[offset : offset + limit], "limit": limit, "offset": offset}


@app.get(f"{API_PREFIX}/projects")
async def projects(
    status: str | None = None,
    q: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    rows = read_json("open_source_projects.json")
    if status:
        rows = [r for r in rows if str(r.get("status", "")).casefold() == status.casefold()]
    if q:
        needle = q.casefold()
        rows = [r for r in rows if needle in json.dumps(r, ensure_ascii=False).casefold()]
    return {"total": len(rows), "items": rows[offset : offset + limit], "limit": limit, "offset": offset}


class ChatRequest(BaseModel):
    model_name: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=20000)
    max_output_tokens: int = Field(default=2048, ge=1, le=16000)


@app.post(f"{API_PREFIX}/chat")
async def chat(payload: ChatRequest):
    # Fail closed until a reviewed model record and adapter exist.
    records = read_json("models.json")
    record = next((m for m in records if m.get("name", "").casefold() == payload.model_name.casefold()), None)
    if record is None:
        raise HTTPException(status_code=404, detail="Model is not registered")
    if str(record.get("status", "")).casefold() != "verified" or not record.get("exact_provider_model_id"):
        raise HTTPException(status_code=409, detail="Model is not verified/configured; request not sent to a provider")
    provider_family = str(record.get("provider_family", "")).casefold()
    provider = "openrouter" if "openrouter" in provider_family else "fireworks" if "fireworks" in provider_family else "huggingface" if any(x in provider_family for x in ("huggingface", "hugging face", "hf inference")) else ""
    if not provider:
        raise HTTPException(status_code=409, detail="Verified model has no supported provider mapping")
    try:
        result = await chat_completion(provider, str(record["exact_provider_model_id"]), [{"role": "user", "content": payload.message}], payload.max_output_tokens)
    except RuntimeError as exc:
        # Provider detail is intentionally generic to avoid leaking request or account data.
        raise HTTPException(status_code=502, detail="Provider request failed or timed out; check provider status and server logs") from exc
    return {"model": record.get("name"), "provider": provider, "content": result["content"], "usage": result.get("usage")}


class ModelProbeRequest(BaseModel):
    provider: str = Field(min_length=1, max_length=40)
    model_id: str = Field(min_length=1, max_length=300)
    confirm_provider_cost: bool = False


@app.post(f"{API_PREFIX}/system/model-probe")
async def model_probe(payload: ModelProbeRequest):
    # This makes a live provider request and may incur charges; never run implicitly.
    if not payload.confirm_provider_cost:
        raise HTTPException(status_code=400, detail="Set confirm_provider_cost=true to authorize one live test request")
    return await probe_model(payload.provider, payload.model_id)


class DocumentSection(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    body: str = Field(default="", max_length=1_500_000)


class PDFRenderRequest(BaseModel):
    template_id: str = Field(default="royal-gold-book", max_length=100)
    title: str = Field(min_length=1, max_length=300)
    subtitle: str = Field(default="", max_length=500)
    author: str = Field(default="", max_length=200)
    font: str | None = Field(default=None, max_length=40)
    page_size: str | None = Field(default=None, max_length=20)
    margin_inches: float | None = Field(default=None, ge=0.45, le=1.5)
    footer_quote: str | None = Field(default=None, max_length=180)
    include_contents: bool | None = None
    include_glossary: bool = True
    references: list[str] = Field(default_factory=list, max_length=3000)
    sections: list[DocumentSection] = Field(min_length=1, max_length=250)
    glossary: list[dict[str, str]] = Field(default_factory=list, max_length=1000)


@app.post(f"{API_PREFIX}/documents/render-pdf")
async def render_document_pdf(payload: PDFRenderRequest):
    """Render supplied chapters into a styled PDF; content generation is a separate LLM task."""
    try:
        render_payload = payload.model_dump()
        templates = read_json("document_templates.json")
        template = next((t for t in templates if t.get("id") == payload.template_id), None)
        if not template:
            raise HTTPException(status_code=422, detail="Unknown document template")
        for key, value in template.get("defaults", {}).items():
            # Pydantic defaults should not override an explicitly customized non-default value.
            if render_payload.get(key) is None:
                render_payload[key] = value
        pdf = render_pdf(render_payload)
    except HTTPException:
        raise
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    safe_name = "kingdom-ai-document.pdf"
    return Response(content=pdf, media_type="application/pdf", headers={
        "Content-Disposition": f'attachment; filename="{safe_name}"',
        "X-Document-Renderer": "kingdom-ai-os-reportlab-v1",
    })


class TemplateProfileRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=240)
    content_base64: str = Field(min_length=1, max_length=28_000_000)


@app.post(f"{API_PREFIX}/documents/template-profile")
async def analyze_template(payload: TemplateProfileRequest):
    """Extract a bounded style profile from DOCX/PDF/image bytes; no file is persisted."""
    name = payload.filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext not in {"docx", "pdf", "png", "jpg", "jpeg", "webp"}:
        raise HTTPException(status_code=415, detail="Supported template references: DOCX, PDF, PNG, JPG, JPEG, WEBP")
    try:
        raw = base64.b64decode(payload.content_base64, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise HTTPException(status_code=400, detail="Invalid base64 file content") from exc
    if len(raw) > 20 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Template reference exceeds 20 MB")
    result: dict[str, Any] = {"filename": name, "format": ext, "bytes": len(raw), "fidelity": "style-profile-only", "stored": False}
    try:
        if ext == "docx":
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                members = archive.infolist()
                if len(members) > 2000 or sum(member.file_size for member in members) > 100 * 1024 * 1024:
                    raise ValueError("DOCX archive expansion limit exceeded")
                if "[Content_Types].xml" not in archive.namelist() or "word/document.xml" not in archive.namelist():
                    raise ValueError("Not a valid DOCX package")
            from docx import Document
            document = Document(io.BytesIO(raw))
            result["paragraph_styles"] = list(dict.fromkeys(p.style.name for p in document.paragraphs if p.text))[:80]
            font_samples = []
            seen_fonts = set()
            for paragraph in document.paragraphs:
                for run in paragraph.runs:
                    if not run.text:
                        continue
                    key = (run.font.name, run.font.size.pt if run.font.size else None, run.bold, run.italic)
                    if key not in seen_fonts:
                        seen_fonts.add(key)
                        font_samples.append({"name": key[0], "size_pt": key[1], "bold": key[2], "italic": key[3]})
            result["font_samples"] = font_samples[:40]
            result["sample_text"] = [p.text[:240] for p in document.paragraphs if p.text][:12]
            result["section_geometry"] = [{"page_width_emu": s.page_width, "page_height_emu": s.page_height, "margin_top_emu": s.top_margin, "margin_bottom_emu": s.bottom_margin, "margin_left_emu": s.left_margin, "margin_right_emu": s.right_margin} for s in document.sections[:10]]
            result["note"] = "DOCX style names and section geometry extracted; theme fonts, floating objects, and exact rendering still require visual review."
        elif ext == "pdf":
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(raw), strict=False)
            page_count = len(reader.pages)
            if page_count > 10000:
                raise ValueError("PDF page-count limit exceeded")
            result["page_count"] = page_count
            result["page_sizes"] = [{"width_pt": float(p.mediabox.width), "height_pt": float(p.mediabox.height)} for p in reader.pages[:10]]
            pdf_fonts = []
            for page in reader.pages[:5]:
                resources = page.get("/Resources") or {}
                fonts = resources.get("/Font") or {}
                for font_key, font_ref in fonts.items():
                    font_obj = font_ref.get_object()
                    pdf_fonts.append({"resource": str(font_key), "base_font": str(font_obj.get("/BaseFont", "unknown")), "subtype": str(font_obj.get("/Subtype", "unknown"))})
            result["font_samples"] = pdf_fonts[:40]
            result["sample_text"] = [(p.extract_text() or "")[:500] for p in reader.pages[:5]]
            result["note"] = "Page dimensions and extractable text sampled; exact layout, fonts, images, and reading order require visual review."
        else:
            from PIL import Image
            image = Image.open(io.BytesIO(raw))
            if image.width * image.height > 50_000_000:
                raise ValueError("Image pixel limit exceeded")
            result["image_size_px"] = {"width": image.width, "height": image.height}
            result["mode"] = image.mode
            try:
                palette_image = image.convert("RGB").resize((min(image.width, 128), min(image.height, 128))).quantize(colors=8)
                palette = palette_image.getpalette() or []
                result["dominant_color_samples"] = ["#%02x%02x%02x" % tuple(palette[i:i+3]) for i in range(0, min(24, len(palette)), 3)]
            except Exception:
                result["dominant_color_samples"] = []
            result["note"] = "Image dimensions/profile extracted; OCR and visual layout reconstruction require a separate review step."
    except Exception as exc:
        # Generic error prevents parser internals or file content leaking.
        raise HTTPException(status_code=422, detail="Could not parse the supplied template reference") from exc
    return result


class RegistryChangeRequest(BaseModel):
    registry: str = Field(pattern=r"^(models|open_source_projects|tabs)$")
    operation: str = Field(pattern=r"^(propose_add|propose_update)$")
    record: dict[str, Any]
    reason: str = Field(min_length=5, max_length=2000)


@app.post(f"{API_PREFIX}/registry/changes/validate")
async def validate_registry_change(payload: RegistryChangeRequest):
    """Validate a proposed change without mutating the live registry."""
    rows = read_json(payload.registry + ".json")
    record = payload.record
    name = str(record.get("name") or record.get("name_as_written") or record.get("title") or record.get("id") or "").strip()
    if not name:
        raise HTTPException(status_code=422, detail="A record needs a name, title, or id")
    if len(json.dumps(record, ensure_ascii=False)) > 50_000:
        raise HTTPException(status_code=413, detail="Proposed registry record is too large")
    key = str(record.get("id") or name).casefold()
    duplicates = [r for r in rows if str(r.get("id") or r.get("name") or r.get("name_as_written") or r.get("title") or "").casefold() == key]
    if payload.operation == "propose_add" and duplicates:
        raise HTTPException(status_code=409, detail="A record with this identity already exists; use propose_update after review")
    if payload.operation == "propose_update" and not duplicates:
        raise HTTPException(status_code=404, detail="No matching record found to update")
    # New integrations/models stay unverified until tested and human-reviewed.
    proposed = dict(record)
    if payload.registry == "models":
        proposed["status"] = "UNVERIFIED"
        proposed.setdefault("exact_provider_model_id", None)
    elif payload.registry == "open_source_projects":
        proposed["status"] = "UNVERIFIED"
        proposed["open_source_status"] = "UNVERIFIED"
    return {"valid": True, "applied": False, "requires_approval": True, "registry": payload.registry,
            "operation": payload.operation, "reason": payload.reason, "existing_count": len(rows),
            "proposed_record": proposed, "note": "Validated proposal only. Live registries were not changed; review and approve via a future signed change workflow."}


@app.get(f"{API_PREFIX}/system/provider-models")
async def provider_models(provider: str = Query(pattern=r"^(openrouter|fireworks|huggingface)$")):
    """Fetch the live model catalog for a configured provider; no model is auto-approved."""
    return await list_provider_models(provider)


@app.get(f"{API_PREFIX}/documents/templates")
async def document_templates():
    return read_json("document_templates.json")


@app.post(f"{API_PREFIX}/documents/render-docx")
async def render_document_docx(payload: PDFRenderRequest):
    """Create an editable DOCX with headings, glossary, page field, and footer ornament."""
    try:
        render_payload = payload.model_dump()
        templates = read_json("document_templates.json")
        template = next((t for t in templates if t.get("id") == payload.template_id), None)
        if not template:
            raise HTTPException(status_code=422, detail="Unknown document template")
        for key, value in template.get("defaults", {}).items():
            if render_payload.get(key) is None:
                render_payload[key] = value
        content = render_docx(render_payload)
    except HTTPException:
        raise
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return Response(content=content, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    headers={"Content-Disposition": 'attachment; filename="kingdom-ai-document.docx"'})
