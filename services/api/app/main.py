from __future__ import annotations

import json
import os
import secrets
import sys
import threading
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Kingdom AI OS — Task Service", version="0.1.0")

TASK_STORE_PATH = Path(os.getenv("TASK_STORE_PATH", "data/tasks.json")).expanduser()


class TaskStatus(str, Enum):
    queued = "queued"
    running = "running"
    done = "done"
    failed = "failed"


class TaskIn(BaseModel):
    workspace: str
    intent: str
    payload: dict = {}


class Task(TaskIn):
    id: str
    status: TaskStatus
    created_at: str


def _load_workspace_keys() -> dict[str, str]:
    """Load ``TASK_API_KEYS`` as either a JSON object or ``workspace:token,...`` pairs.

    Each token grants read access only to tasks in the matching workspace.
    """
    raw = os.getenv("TASK_API_KEYS", "").strip()
    if not raw:
        return {}

    if raw.startswith("{"):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"Invalid TASK_API_KEYS; task reads are disabled: {exc}", file=sys.stderr)
            return {}
        if not isinstance(value, dict):
            print("Invalid TASK_API_KEYS; expected a JSON object.", file=sys.stderr)
            return {}
        return {
            str(workspace): str(token)
            for workspace, token in value.items()
            if str(workspace).strip() and str(token).strip()
        }

    keys: dict[str, str] = {}
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        separator = "=" if "=" in entry else ":" if ":" in entry else None
        if separator is None:
            continue
        workspace, token = entry.split(separator, 1)
        workspace = workspace.strip()
        token = token.strip()
        if workspace and token:
            keys[workspace] = token
    return keys


WORKSPACE_KEYS = _load_workspace_keys()


class TaskStore:
    """Durable JSON-file task store so tasks survive API process restarts."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.RLock()
        self._tasks: dict[str, Task] = {}
        self._load()

    def _quarantine_corrupt_file(self) -> None:
        suffix = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = self.path.with_name(f"{self.path.name}.corrupt-{suffix}")
        try:
            self.path.replace(backup)
            print(f"Moved unreadable task store to {backup}", file=sys.stderr)
        except OSError as exc:
            print(f"Could not move unreadable task store {self.path}: {exc}", file=sys.stderr)

    def _load(self) -> None:
        if not self.path.exists():
            return

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Could not read task store {self.path}: {exc}", file=sys.stderr)
            self._quarantine_corrupt_file()
            return

        items = raw.get("tasks", []) if isinstance(raw, dict) else raw
        if not isinstance(items, list):
            items = []

        self._tasks = {}
        for item in items:
            if not isinstance(item, dict) or "id" not in item:
                continue
            try:
                self._tasks[item["id"]] = Task.model_validate(item)
            except Exception as exc:
                print(f"Skipping invalid task {item.get('id')}: {exc}", file=sys.stderr)

    def _save_locked(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": 1,
            "tasks": [task.model_dump(mode="json") for task in self._tasks.values()],
        }
        tmp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp_path.replace(self.path)

    def all(self) -> list[Task]:
        with self._lock:
            return list(self._tasks.values())

    def get(self, task_id: str) -> Task | None:
        with self._lock:
            return self._tasks.get(task_id)

    def put(self, task: Task) -> None:
        with self._lock:
            self._tasks[task.id] = task
            self._save_locked()


STORE = TaskStore(TASK_STORE_PATH)


def _bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def _workspace_for_token(token: str | None) -> str | None:
    if not token:
        return None
    for workspace, expected in WORKSPACE_KEYS.items():
        if secrets.compare_digest(expected, token):
            return workspace
    return None


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid bearer token",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True, "service": "kingdom-task-api", "version": app.version}


@app.post("/tasks", response_model=Task)
def create_task(body: TaskIn) -> Task:
    task = Task(
        id=str(uuid4()),
        status=TaskStatus.queued,
        created_at=datetime.now(timezone.utc).isoformat(),
        **body.model_dump(),
    )
    STORE.put(task)
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str, authorization: Annotated[str | None, Header()] = None) -> Task:
    task = STORE.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    workspace = _workspace_for_token(_bearer_token(authorization))
    if workspace is None:
        raise _unauthorized()
    if task.workspace != workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks(authorization: Annotated[str | None, Header()] = None) -> list[Task]:
    workspace = _workspace_for_token(_bearer_token(authorization))
    if workspace is None:
        raise _unauthorized()
    return [task for task in STORE.all() if task.workspace == workspace]