"""Kingdom AI OS backend.

FastAPI application with lifespan-aware infrastructure probes, CORS, security
middleware, and the same 10-section tab grammar mounted at /api/<tab>.
"""
from __future__ import annotations

import importlib
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import AsyncIterator, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.security_middleware import KingdomSecurityMiddleware

TAB_SLUGS: List[str] = [
    "home", "llm", "research", "legal", "osint", "finance", "investments",
    "real_estate", "business", "leads", "urban_planning", "engineering_ghidra",
    "coding", "web_scraping", "news", "social_marketing", "fashion",
    "images_visual", "video_ugc", "music_audio", "agents_comms", "tasks",
    "open_source", "security_admin",
]

SERVICE_FLAGS = {
    "qdrant": os.getenv("FLAG_QDRANT", "1"),
    "minio": os.getenv("FLAG_MINIO", "1"),
    "vault": os.getenv("FLAG_VAULT", "1"),
    "postgres": os.getenv("FLAG_POSTGRES", "1"),
    "redis": os.getenv("FLAG_REDIS", "1"),
    "cua_fleet": os.getenv("FLAG_CUA_FLEET", "1"),
    "gpu_workers": os.getenv("FLAG_GPU_WORKERS", "1"),
    "security_stack": os.getenv("FLAG_SECURITY_STACK", "1"),
}


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _enabled(name: str) -> bool:
    return SERVICE_FLAGS.get(name, "1") == "1"


def include_tab_routers(app: FastAPI) -> None:
    """Mount one router per tab. Imports stay explicit so failures are visible."""
    for slug in TAB_SLUGS:
        module = importlib.import_module(f"backend.api.routers.{slug}")
        app.include_router(module.router)


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # Lazy imports keep opt-in native/protobuf clients out of startup until
        # their service flag is enabled.
        if _enabled("qdrant"):
            try:
                from qdrant_client import QdrantClient  # noqa: F401
            except Exception:
                app.state.qdrant_ready = False
            else:
                app.state.qdrant_ready = os.getenv("QDRANT_URL", "http://qdrant:6333") is not None
        if _enabled("vault"):
            try:
                import hvac  # noqa: F401
            except Exception:
                app.state.vault_ready = False
            else:
                app.state.vault_ready = os.getenv("VAULT_ADDR", "http://vault:8200") is not None
        app.state.started_at = _utcnow()
        yield
        app.state.stopped_at = _utcnow()

    app = FastAPI(
        title="Kingdom AI OS",
        description="24-tab sovereign AI operating system: FastAPI backend -> Qdrant, MinIO, Vault, Postgres, Redis, CUA Fleet, GPU Workers.",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(KingdomSecurityMiddleware)
    include_tab_routers(app)

    @app.get("/", tags=["system"])
    def root() -> Dict[str, str]:
        return {"name": "Kingdom AI OS", "version": "1.0.0", "docs": "/docs", "tabs": "/api/home"}

    @app.get("/healthz", tags=["system"])
    def healthz() -> Dict[str, object]:
        return {
            "status": "ok",
            "tabs": len(TAB_SLUGS),
            "flags": {name: _enabled(name) for name in SERVICE_FLAGS},
            "now": _utcnow(),
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "8000")), reload=os.getenv("RELOAD", "0") == "1")
