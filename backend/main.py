"""Kingdom AI OS backend entrypoint.

This module owns the FastAPI application, process lifespan, CORS policy,
``/healthz``, and dynamic mounting of the 24 API routers that live in
``backend/api/routers``.
"""

from __future__ import annotations

import asyncio
import importlib
import logging
import os
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

LOGGER_NAME = "kingdom.backend"
logger = logging.getLogger(LOGGER_NAME)
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

# The 24 domain routers that make up the core Kingdom AI OS API surface.
# Each name maps to ``backend/api/routers/<name>.py`` and is mounted with the
# router's own prefix.
ROUTER_MODULES: tuple[str, ...] = (
    "agents",
    "auth",
    "blueprints",
    "chat",
    "discovery",
    "documents",
    "embeddings",
    "events",
    "files",
    "gateway",
    "hermes",
    "integrations",
    "jobs",
    "knowledge",
    "memory",
    "metrics",
    "models",
    "orchestration",
    "prompts",
    "sandbox",
    "search",
    "security",
    "sessions",
    "workflows",
)

# Depending on how the application is launched, the same router package can be
# addressed as either of these absolute import paths.
ROUTER_PACKAGE_CANDIDATES = ("backend.api.routers", "api.routers")

HEALTHY = "healthy"
DEGRADED = "degraded"
OFFLINE = "offline"
DISABLED = "disabled"


@dataclass
class AppState:
    """Mutable state attached to ``app.state.kingdom`` for the lifespan."""

    started_at: float | None = None
    shutting_down: bool = False


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _env_bool(name: str, default: bool = False) -> bool:
    value = _env(name)
    if not value:
        return default
    return value.lower() in {"1", "true", "yes", "on", "enabled"}


def _import_router_module(name: str):
    """Import one router module, trying the supported launch layouts."""
    errors: list[str] = []

    for package in ROUTER_PACKAGE_CANDIDATES:
        qualified_name = f"{package}.{name}"
        try:
            return importlib.import_module(qualified_name)
        except ModuleNotFoundError as exc:
            package_segments = set(package.split(".")) | {package, qualified_name}
            if exc.name and (
                exc.name in package_segments or package.startswith(f"{exc.name}.")
            ):
                errors.append(f"{qualified_name}: {exc}")
                continue
            raise

    raise ImportError(
        f"Unable to import router module {name!r}; attempted "
        f"{', '.join(ROUTER_PACKAGE_CANDIDATES)}. Errors: {errors}"
    )


def _mount_routers(app: FastAPI) -> None:
    """Mount every router declared in :data:`ROUTER_MODULES`."""
    mounted = 0
    for module_name in ROUTER_MODULES:
        module = _import_router_module(module_name)
        router = getattr(module, "router", None)
        if router is None:
            raise AttributeError(
                f"Router module {module_name!r} must expose an APIRouter named 'router'"
            )
        app.include_router(router)
        mounted += 1

    if mounted != len(ROUTER_MODULES):
        raise RuntimeError(
            f"Expected to mount {len(ROUTER_MODULES)} routers, only mounted {mounted}"
        )
    logger.info("Mounted %d Kingdom AI OS routers", mounted)


def _ensure_http_url(value: str, path: str = "") -> str:
    """Return a full HTTP URL, accepting endpoints supplied without a scheme.

    Empty values are passed through unchanged so that optional dependencies can
    be disabled by leaving their environment variable blank.
    """
    if not value:
        return ""
    if not value.startswith(("http://", "https://")):
        value = f"http://{value}"
    return f"{value.rstrip('/')}{path}"


def _host_and_port(url: str, default_port: int) -> tuple[str, int]:
    """Extract host/port from a database/redis-style URL."""
    if "://" not in url:
        url = f"//{url}"
    parsed = urlparse(url)
    return parsed.hostname or "localhost", parsed.port or default_port


async def _check_tcp(url: str, default_port: int, timeout: float = 1.0) -> str:
    if not url:
        return DISABLED

    try:
        host, port = _host_and_port(url, default_port)
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        try:
            writer.close()
            await writer.wait_closed()
        finally:
            reader.feed_eof()
        return HEALTHY
    except Exception as exc:  # noqa: BLE001 - health checks intentionally broad
        logger.debug("TCP health check failed for %s: %s", url, exc)
        return OFFLINE


async def _check_http(url: str, timeout: float = 1.0) -> str:
    if not url:
        return DISABLED

    try:
        full_url = _ensure_http_url(url)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(full_url)
        return HEALTHY if response.status_code < 500 else DEGRADED
    except Exception as exc:  # noqa: BLE001 - health checks intentionally broad
        logger.debug("HTTP health check failed for %s: %s", url, exc)
        return OFFLINE


async def _collect_service_status() -> dict[str, str]:
    """Check the Kingdom AI OS dependency services concurrently."""
    qdrant_url = _env("QDRANT_URL", "http://localhost:6333")
    minio_endpoint = _env("MINIO_ENDPOINT", "localhost:9000")
    vault_addr = _env("VAULT_ADDR", "http://localhost:8200")
    database_url = _env(
        "DATABASE_URL", "postgresql://user:pass@localhost:5432/kingdom"
    )
    redis_url = _env("REDIS_URL", "redis://localhost:6379")

    (
        postgres_status,
        redis_status,
        qdrant_status,
        minio_status,
        vault_status,
    ) = await asyncio.gather(
        _check_tcp(database_url, 5432),
        _check_tcp(redis_url, 6379),
        _check_http(_ensure_http_url(qdrant_url, "/")),
        _check_http(_ensure_http_url(minio_endpoint, "/minio/health/live")),
        _check_http(_ensure_http_url(vault_addr, "/v1/sys/health")),
    )

    return {
        "backend": HEALTHY,
        "postgres": postgres_status,
        "redis": redis_status,
        "qdrant": qdrant_status,
        "minio": minio_status,
        "vault": vault_status,
    }


def _overall_status(services: dict[str, str]) -> str:
    """Derive the aggregate healthz state from dependency checks."""
    dependency_statuses = {
        value for key, value in services.items() if key != "backend" and value != DISABLED
    }
    if not dependency_statuses:
        return HEALTHY
    if dependency_statuses == {OFFLINE}:
        return OFFLINE
    if OFFLINE in dependency_statuses or DEGRADED in dependency_statuses:
        return DEGRADED
    return HEALTHY


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Kingdom AI OS startup and shutdown hooks."""
    state = AppState(started_at=time.time())
    app.state.kingdom = state

    logger.info(
        "Kingdom AI OS backend starting "
        "(sandbox=%s discovery=%s security=%s hermes=%s sandbox_equip_all=%s)",
        _env_bool("ENABLE_SANDBOX", True),
        _env_bool("ENABLE_DISCOVERY", True),
        _env_bool("ENABLE_SECURITY", True),
        _env_bool("ENABLE_HERMES", True),
        _env_bool("ENABLE_SANDBOX_EQUIP_ALL", True),
    )

    try:
        yield
    finally:
        state.shutting_down = True
        state.started_at = None
        logger.info("Kingdom AI OS backend stopped")


app = FastAPI(
    title="Kingdom AI OS API",
    description="Core backend for the Kingdom AI OS agent platform.",
    version="0.1.0",
    lifespan=lifespan,
)

# Dev-friendly CORS: allow every origin. This is intentionally permissive for
# local development and should be tightened for production deployments.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

_mount_routers(app)


@app.get("/healthz")
async def healthz() -> JSONResponse:
    """Report aggregate backend health and individual dependency status."""
    try:
        services = await _collect_service_status()
        aggregate_status = _overall_status(services)
    except Exception:  # noqa: BLE001 - healthz must never fail open
        logger.exception("Unexpected error while collecting dependency health")
        services = {"backend": DEGRADED}
        aggregate_status = DEGRADED

    status_code = 200 if aggregate_status == HEALTHY else 503
    return JSONResponse(
        content={
            "status": aggregate_status,
            "services": services,
        },
        status_code=status_code,
    )


if __name__ == "__main__":
    import uvicorn

    # ``backend.main:app`` is used by ``python -m backend.main``/``uvicorn``
    # from the repository root; ``main:app`` is used by the Dockerfile where
    # the backend directory itself is the working directory.
    app_import = "backend.main:app" if __package__ else "main:app"
    uvicorn.run(
        app_import,
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("ENVIRONMENT", "development").lower()
        in {"development", "dev", "local"},
    )