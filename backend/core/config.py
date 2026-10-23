"""Runtime configuration and live toggleable ENABLE_* turn-off flags for Kingdom AI OS."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field

BACKEND_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = BACKEND_ROOT.parent


def _resolve_runtime_dir() -> Path:
    candidate = BACKEND_ROOT / ".runtime"
    try:
        candidate.mkdir(parents=True, exist_ok=True)
        probe = candidate / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return candidate
    except OSError:
        fallback = Path("/tmp/kingdom_runtime")
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


RUNTIME_DIR = _resolve_runtime_dir()


def _env_bool(name: str, default: bool = True) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off"}


class FeatureFlags(BaseModel):
    """Granular turn-off flags (default True; any feature can be disabled cleanly)."""

    model_config = ConfigDict(extra="forbid")

    ENABLE_SANDBOX_EQUIP_ALL: bool = Field(default_factory=lambda: _env_bool("ENABLE_SANDBOX_EQUIP_ALL", True))
    ENABLE_DISCOVERY: bool = Field(default_factory=lambda: _env_bool("ENABLE_DISCOVERY", True))
    ENABLE_SANDBOX: bool = Field(default_factory=lambda: _env_bool("ENABLE_SANDBOX", True))
    ENABLE_SECURITY: bool = Field(default_factory=lambda: _env_bool("ENABLE_SECURITY", True))
    ENABLE_HERMES: bool = Field(default_factory=lambda: _env_bool("ENABLE_HERMES", True))
    ENABLE_LLM_ROUTER: bool = Field(default_factory=lambda: _env_bool("ENABLE_LLM_ROUTER", True))
    ENABLE_IMAGE_CONSISTENCY: bool = Field(default_factory=lambda: _env_bool("ENABLE_IMAGE_CONSISTENCY", True))
    ENABLE_VIDEO_AGENT: bool = Field(default_factory=lambda: _env_bool("ENABLE_VIDEO_AGENT", True))
    ENABLE_ENGINEERING: bool = Field(default_factory=lambda: _env_bool("ENABLE_ENGINEERING", True))
    ENABLE_VOCAL_TUNING: bool = Field(default_factory=lambda: _env_bool("ENABLE_VOCAL_TUNING", True))
    ENABLE_TESTING: bool = Field(default_factory=lambda: _env_bool("ENABLE_TESTING", True))
    ENABLE_SELF_UPDATE: bool = Field(default_factory=lambda: _env_bool("ENABLE_SELF_UPDATE", True))
    ENABLE_TAB_BUILDER: bool = Field(default_factory=lambda: _env_bool("ENABLE_TAB_BUILDER", True))
    ENABLE_NEVER_GIVE_UP: bool = Field(default_factory=lambda: _env_bool("ENABLE_NEVER_GIVE_UP", True))


class AppSettings(BaseModel):
    """Locked application configuration derived from environment variables."""

    model_config = ConfigDict(extra="ignore")

    app_name: str = "Kingdom AI OS Sovereign Control Plane"
    version: str = "2.4.0"
    qdrant_url: str = Field(default_factory=lambda: os.getenv("QDRANT_URL", "http://qdrant:6333"))
    qdrant_collection: str = Field(default_factory=lambda: os.getenv("QDRANT_COLLECTION", "kingdom_knowledge_768d"))
    minio_endpoint: str = Field(default_factory=lambda: os.getenv("MINIO_ENDPOINT", "minio:9000"))
    minio_root_user: str = Field(default_factory=lambda: os.getenv("MINIO_ROOT_USER", "minioadmin"))
    minio_root_password: str = Field(default_factory=lambda: os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123"))
    minio_secure: bool = Field(default_factory=lambda: _env_bool("MINIO_SECURE", False))
    finished_bucket: str = Field(default_factory=lambda: os.getenv("MINIO_FINISHED_BUCKET", "kingdom-finished"))
    requests_bucket: str = Field(default_factory=lambda: os.getenv("MINIO_REQUESTS_BUCKET", "kingdom-requests"))
    vault_addr: str = Field(default_factory=lambda: os.getenv("VAULT_ADDR", "http://vault:8200"))
    vault_token: str = Field(default_factory=lambda: os.getenv("VAULT_TOKEN", "root"))
    database_url: str = Field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://kingdom:kingdom123@postgres:5432/kingdom",
        )
    )
    redis_url: str = Field(default_factory=lambda: os.getenv("REDIS_URL", "redis://redis:6379/0"))
    github_repo: str = Field(default_factory=lambda: os.getenv("GITHUB_REPO", "YOURNAME/kingdom-ai-os"))
    vultr_region: str = Field(default_factory=lambda: os.getenv("VULTR_REGION", "ewr"))
    vultr_plan: str = Field(default_factory=lambda: os.getenv("VULTR_PLAN", "vcg-a100-1c-8g-40vram"))
    vultr_os_id: int = Field(default_factory=lambda: int(os.getenv("VULTR_OS_ID", "1743")))
    kingdom_internal_secret: str = Field(
        default_factory=lambda: os.getenv("KINGDOM_INTERNAL_SECRET", "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4")
    )
    test_interval: int = Field(default_factory=lambda: int(os.getenv("TEST_INTERVAL", "1200")))
    convex_webhook_url: str = Field(default_factory=lambda: os.getenv("CONVEX_WEBHOOK_URL", ""))


SETTINGS = AppSettings()
FLAGS = FeatureFlags()


def get_flags_dict() -> Dict[str, bool]:
    """Return current live feature flags."""
    return FLAGS.model_dump()


def update_flags(patch: Dict[str, bool]) -> FeatureFlags:
    """Update runtime feature flags without server restart."""
    global FLAGS
    merged = FLAGS.model_dump()
    for key, val in patch.items():
        if key in merged and isinstance(val, bool):
            merged[key] = val
            os.environ[key] = "true" if val else "false"
    FLAGS = FeatureFlags(**merged)
    return FLAGS


def get_openrouter_keys() -> list[str]:
    """Collect up to 10 OpenRouter keys configured for automatic failover."""
    keys: list[str] = []
    for i in range(1, 11):
        val = os.getenv(f"OPENROUTER_API_KEY_{i}", "").strip()
        if val and not val.startswith("sk-or-v1-replace"):
            keys.append(val)
    primary = os.getenv("OPENROUTER_API_KEY", "").strip()
    if primary and not primary.startswith("sk-or-v1-replace") and primary not in keys:
        keys.append(primary)
    return keys
