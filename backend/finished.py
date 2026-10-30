"""Atomic write logic for the sandbox Finished Folder.

Each completed task writes a JSON manifest and content artifact with
write-to-temp + fsync + os.replace so readers never observe partial files.
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


def ensure_finished_root() -> Path:
    root = Path(os.getenv("FINISHED_FOLDER", "/var/lib/kingdom/finished"))
    root.mkdir(parents=True, exist_ok=True)
    return root


def _atomic_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + f".tmp-{uuid.uuid4().hex}")
    with temp.open("w", encoding="utf-8") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def write_finished_artifact(tab: str, task_id: str, payload: Dict[str, Any], idempotency_key: str = "") -> Path:
    """Persist a completed sandbox artifact idempotently."""
    key = idempotency_key or task_id
    folder = ensure_finished_root() / tab
    manifest_path = folder / f"{key}.manifest.json"
    manifest: Dict[str, Any] = {
        "schema": "kingdom.finished.v1",
        "tab": tab,
        "task_id": task_id,
        "idempotency_key": key,
        "completed_at": utcnow(),
        "content_file": f"{key}.artifact.json",
        "payload": payload,
    }
    _atomic_write(folder / manifest["content_file"], json.dumps(payload, indent=2, sort_keys=True))
    _atomic_write(manifest_path, json.dumps(manifest, indent=2, sort_keys=True))
    return manifest_path


__all__ = ["ensure_finished_root", "write_finished_artifact", "utcnow"]
