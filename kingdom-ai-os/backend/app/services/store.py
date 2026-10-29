"""Persistent storage for conversations, messages and model checks.

Uses SQLite (stdlib) so the app works on a single Vultr server with zero extra
services. Path comes from KAIOS_DB_PATH (default: <repo>/data/kaios.db).
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Any

_LOCK = threading.Lock()
_SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
  id TEXT PRIMARY KEY, tab_id TEXT NOT NULL, title TEXT NOT NULL,
  created_at REAL NOT NULL, updated_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_conv_tab ON conversations(tab_id, updated_at DESC);
CREATE TABLE IF NOT EXISTS messages (
  id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role TEXT NOT NULL, content TEXT NOT NULL, model_id TEXT, citations TEXT, usage TEXT,
  attachments TEXT, created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_msg_conv ON messages(conversation_id, created_at);
CREATE TABLE IF NOT EXISTS model_checks (
  model_id TEXT PRIMARY KEY, status TEXT NOT NULL, detail TEXT, checked_at REAL NOT NULL
);
"""


def db_path() -> Path:
    default = Path(__file__).resolve().parents[3] / "data" / "kaios.db"
    return Path(os.getenv("KAIOS_DB_PATH", str(default)))


def _connect() -> sqlite3.Connection:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(_SCHEMA)
    return conn


def _row(r: sqlite3.Row | None) -> dict[str, Any] | None:
    if r is None:
        return None
    d = dict(r)
    for key in ("citations", "usage", "attachments", "detail"):
        if key in d and isinstance(d[key], str) and d[key][:1] in "[{":
            try:
                d[key] = json.loads(d[key])
            except ValueError:
                pass
    return d


def health() -> str:
    try:
        with _LOCK, _connect() as c:
            c.execute("SELECT 1").fetchone()
        return "ok"
    except sqlite3.Error:
        return "unavailable"


def create_conversation(tab_id: str, title: str) -> dict[str, Any]:
    now = time.time()
    cid = uuid.uuid4().hex
    with _LOCK, _connect() as c:
        c.execute("INSERT INTO conversations VALUES (?,?,?,?,?)", (cid, tab_id, title[:120] or "New chat", now, now))
    return {"id": cid, "tab_id": tab_id, "title": title[:120] or "New chat", "created_at": now, "updated_at": now}


def list_conversations(tab_id: str | None, limit: int = 50) -> list[dict[str, Any]]:
    with _LOCK, _connect() as c:
        if tab_id:
            rows = c.execute("SELECT * FROM conversations WHERE tab_id=? ORDER BY updated_at DESC LIMIT ?", (tab_id, limit)).fetchall()
        else:
            rows = c.execute("SELECT * FROM conversations ORDER BY updated_at DESC LIMIT ?", (limit,)).fetchall()
    return [_row(r) for r in rows]


def get_conversation(cid: str) -> dict[str, Any] | None:
    with _LOCK, _connect() as c:
        conv = _row(c.execute("SELECT * FROM conversations WHERE id=?", (cid,)).fetchone())
        if conv is None:
            return None
        conv["messages"] = [_row(r) for r in c.execute("SELECT * FROM messages WHERE conversation_id=? ORDER BY created_at", (cid,)).fetchall()]
    return conv


def delete_conversation(cid: str) -> bool:
    with _LOCK, _connect() as c:
        return c.execute("DELETE FROM conversations WHERE id=?", (cid,)).rowcount > 0


def add_message(cid: str, role: str, content: str, model_id: str | None = None, citations: list | None = None,
                usage: dict | None = None, attachments: list | None = None) -> dict[str, Any]:
    now = time.time()
    mid = uuid.uuid4().hex
    with _LOCK, _connect() as c:
        c.execute(
            "INSERT INTO messages VALUES (?,?,?,?,?,?,?,?,?)",
            (mid, cid, role, content, model_id, json.dumps(citations or []), json.dumps(usage or {}), json.dumps(attachments or []), now),
        )
        c.execute("UPDATE conversations SET updated_at=? WHERE id=?", (now, cid))
    return {"id": mid, "conversation_id": cid, "role": role, "content": content, "model_id": model_id,
            "citations": citations or [], "usage": usage or {}, "attachments": attachments or [], "created_at": now}


def record_model_check(model_id: str, status: str, detail: dict) -> None:
    with _LOCK, _connect() as c:
        c.execute("INSERT OR REPLACE INTO model_checks VALUES (?,?,?,?)", (model_id, status, json.dumps(detail), time.time()))


def model_checks() -> dict[str, dict[str, Any]]:
    with _LOCK, _connect() as c:
        return {r["model_id"]: _row(r) for r in c.execute("SELECT * FROM model_checks").fetchall()}
