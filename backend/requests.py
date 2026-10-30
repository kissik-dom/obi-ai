"""Request Folder sandbox bootstrap.

Every task receives a new sandbox with a Requests Folder, unless the per-tab
sandbox flag is turned off. The manifest records idempotency key, tab, CUA
space, GPU worker, and MinIO bucket assignments.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
import uuid


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_requests_root() -> Path:
    root = Path(os.getenv("REQUESTS_FOLDER", "/var/lib/kingdom/requests"))
    root.mkdir(parents=True, exist_ok=True)
    return root


def create_request_folder(tab: str, idempotency_key: str = "", cua_space: int | None = None, gpu_worker: int | None = None) -> Path:
    """Create a sandbox Requests Folder atomically.

    The folder is created in a temp name then renamed, so tooling that scans
    Requests Folders never locks a half-created sandbox.
    """
    key = idempotency_key or uuid.uuid4().hex
    root = ensure_requests_root()
    folder = root / tab / key
    if folder.exists():
        return folder
    temp = root / tab / f".{key}.tmp-{uuid.uuid4().hex}"
    temp.mkdir(parents=True, exist_ok=False)
    manifest: Dict[str, Any] = {
        "schema": "kingdom.request.v1",
        "tab": tab,
        "idempotency_key": key,
        "sandbox": {
            "enabled": os.getenv(f"FLAG_SANDBOX_{tab.upper()}", os.getenv("FLAG_SANDBOX", "1")) == "1",
            "cua_space": cua_space,
            "gpu_worker": gpu_worker,
            "minio_bucket": f"kingdom-sandboxes-{tab}",
            "requests_folder": str(folder),
            "finished_folder": f"/var/lib/kingdom/finished/{tab}",
        },
        "created_at": utcnow(),
    }
    (temp / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    try:
        os.rename(temp, folder)
    except FileNotFoundError:
        folder.mkdir(parents=True, exist_ok=True)
    return folder


def write_request_file(folder: Path, name: str, content: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / name
    temp = folder / f".{name}.tmp-{uuid.uuid4().hex}"
    temp.write_text(content, encoding="utf-8")
    os.replace(temp, target)
    return target


__all__ = ["create_request_folder", "ensure_requests_root", "write_request_file", "utcnow"]
