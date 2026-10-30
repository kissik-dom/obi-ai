"""TV / Movie Studio: any-length movies on free local models, with long-term memory.

How it works (Letta-style memory, no extra services):
- Clock: an N-minute movie is split into 15-minute acts (+ a short epilogue). Every scene carries
  its start/end minute, so you can jump to any minute ("show me 84-86").
- Core memory blocks (always loaded): human, persona, movie_bible, style_bible, current_act.
- Archival memory (unlimited): every act summary, scene and research note is saved in SQLite
  with full-text search, and the relevant pieces are recalled into the prompt for each new act.
- Template lock: on Ollama the model must answer in the exact JSON schema (structured output),
  so scenes always have INT/EXT, location, action, dialogue, camera, color and music.
"""
from __future__ import annotations

import json
import math
import re
import time
import uuid
from typing import Any

import httpx

from app.services import assistant, store

ACT_MINUTES = 15
MIN_EPILOGUE = 5  # a remainder shorter than this becomes an epilogue
BLOCKS = ("human", "persona", "movie_bible", "style_bible", "current_act")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS studio_projects (
  id TEXT PRIMARY KEY, title TEXT NOT NULL, minutes INTEGER NOT NULL, premise TEXT NOT NULL,
  model_id TEXT, clock TEXT NOT NULL, created_at REAL NOT NULL, updated_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS studio_blocks (
  project_id TEXT NOT NULL REFERENCES studio_projects(id) ON DELETE CASCADE,
  label TEXT NOT NULL, value TEXT NOT NULL, PRIMARY KEY (project_id, label)
);
CREATE TABLE IF NOT EXISTS studio_acts (
  project_id TEXT NOT NULL REFERENCES studio_projects(id) ON DELETE CASCADE,
  act INTEGER NOT NULL, data TEXT NOT NULL, model_id TEXT, created_at REAL NOT NULL,
  PRIMARY KEY (project_id, act)
);
CREATE VIRTUAL TABLE IF NOT EXISTS studio_archive USING fts5(project_id UNINDEXED, kind UNINDEXED, text);
"""


def _db():
    conn = store._connect()
    conn.executescript(_SCHEMA)
    return conn


# ---------- clock ----------
def plan_clock(minutes: int) -> list[dict[str, Any]]:
    """Split N minutes into 15-minute acts; a short remainder becomes an epilogue."""
    full, rest = divmod(minutes, ACT_MINUTES)
    spans = [ACT_MINUTES] * full
    if rest:
        spans.append(rest)  # under MIN_EPILOGUE minutes it is labelled an epilogue
    acts, start = [], 0
    for i, span in enumerate(spans, 1):
        epilogue = i == len(spans) and span < MIN_EPILOGUE and len(spans) > 1
        acts.append({"act": i, "label": "Epilogue" if epilogue else f"Act {i}", "start": start, "end": start + span})
        start += span
    return acts


# ---------- JSON schemas (template lock) ----------
BIBLE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "logline": {"type": "string"},
        "genre": {"type": "string"},
        "world": {"type": "string"},
        "characters": {"type": "array", "items": {"type": "object", "properties": {
            "name": {"type": "string"}, "role": {"type": "string"}, "look": {"type": "string"}, "want": {"type": "string"}},
            "required": ["name", "role", "look", "want"]}},
        "style": {"type": "object", "properties": {
            "color_palette": {"type": "string"}, "lenses_camera": {"type": "string"}, "music": {"type": "string"}, "tone": {"type": "string"}},
            "required": ["color_palette", "lenses_camera", "music", "tone"]},
        "act_beats": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["logline", "genre", "world", "characters", "style", "act_beats"],
}

SCENE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "act_summary": {"type": "string"},
        "scenes": {"type": "array", "items": {"type": "object", "properties": {
            "minute_start": {"type": "number"}, "minute_end": {"type": "number"},
            "int_ext": {"type": "string", "enum": ["INT.", "EXT.", "INT./EXT."]},
            "location": {"type": "string"}, "time_of_day": {"type": "string"},
            "action": {"type": "string"},
            "dialogue": {"type": "array", "items": {"type": "object", "properties": {
                "character": {"type": "string"}, "line": {"type": "string"}}, "required": ["character", "line"]}},
            "camera": {"type": "string"}, "color": {"type": "string"}, "music": {"type": "string"}},
            "required": ["minute_start", "minute_end", "int_ext", "location", "time_of_day", "action", "dialogue", "camera", "color", "music"]}},
    },
    "required": ["act_summary", "scenes"],
}


class StudioError(RuntimeError):
    pass


def _parse_json(text: str) -> dict[str, Any]:
    text = text.strip()
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise StudioError("model did not return JSON")
    return json.loads(m.group(0))


async def _structured(model_id: str | None, system: str, user: str, schema: dict[str, Any], max_tokens: int) -> tuple[dict[str, Any], str]:
    """Ask a model for JSON that matches `schema`. Ollama enforces the schema while generating."""
    model = model_id or assistant.default_model()
    base = assistant.ollama_base()
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    if model.startswith("ollama/") and base:
        payload = {"model": model.removeprefix("ollama/"), "messages": messages, "format": schema, "stream": False,
                   "options": {"temperature": 0.8, "num_predict": max_tokens, "num_ctx": 8192}}
        root = base[:-3] if base.endswith("/v1") else base
        async with httpx.AsyncClient(timeout=1800.0) as client:
            r = await client.post(root + "/api/chat", json=payload)
        if r.status_code != 200:
            raise StudioError(f"{model}: HTTP {r.status_code} {r.text[:200]}")
        content = (r.json().get("message") or {}).get("content") or ""
        try:
            return json.loads(content), model
        except ValueError as exc:
            raise StudioError(f"{model}: output was cut off; try a shorter act or a bigger model") from exc
    # Free cloud models: describe the schema and validate the reply.
    messages[0]["content"] += "\nReply with ONLY JSON matching this schema:\n" + json.dumps(schema)
    res = await assistant.answer(model, messages, web=False, max_tokens=max_tokens)
    return _parse_json(res["content"]), res["model_id"]


# ---------- memory ----------
def _set_block(conn, pid: str, label: str, value: str) -> None:
    conn.execute("INSERT INTO studio_blocks(project_id,label,value) VALUES(?,?,?) "
                 "ON CONFLICT(project_id,label) DO UPDATE SET value=excluded.value", (pid, label, value))


def _blocks(conn, pid: str) -> dict[str, str]:
    return {r["label"]: r["value"] for r in conn.execute("SELECT label,value FROM studio_blocks WHERE project_id=?", (pid,))}


def archive(pid: str, kind: str, text: str) -> None:
    with store._LOCK, _db() as conn:
        conn.execute("INSERT INTO studio_archive(project_id,kind,text) VALUES(?,?,?)", (pid, kind, text))


def recall(pid: str, query: str, limit: int = 6) -> list[dict[str, str]]:
    words = [w for w in re.findall(r"[A-Za-z0-9]{3,}", query)][:20]
    if not words:
        return []
    q = " OR ".join(f'"{w}"' for w in words)
    with store._LOCK, _db() as conn:
        rows = conn.execute("SELECT kind,text FROM studio_archive WHERE project_id=? AND studio_archive MATCH ? "
                            "ORDER BY rank LIMIT ?", (pid, q, limit)).fetchall()
    return [{"kind": r["kind"], "text": r["text"]} for r in rows]


def _core_memory(blocks: dict[str, str]) -> str:
    return "\n\n".join(f"<{k}>\n{blocks.get(k, '')}\n</{k}>" for k in BLOCKS if blocks.get(k))


# ---------- projects ----------
async def create_project(title: str, minutes: int, premise: str, persona: str, human: str, model_id: str | None) -> dict[str, Any]:
    clock = plan_clock(minutes)
    system = (persona or "You are a visionary film director and showrunner.") + (
        " Build a production bible: vivid world, distinct characters with exact looks, a precise visual style, "
        f"and exactly {len(clock)} act beats (one per act) that form a complete story arc.")
    user = f"Title: {title}\nLength: {minutes} minutes in {len(clock)} acts.\nPremise: {premise}"
    bible, used = await _structured(model_id, system, user, BIBLE_SCHEMA, 1500)
    beats = list(bible.get("act_beats") or [])
    for i, act in enumerate(clock):
        act["beat"] = beats[i] if i < len(beats) else ""
    pid, now = uuid.uuid4().hex[:12], time.time()
    style = bible.get("style") or {}
    movie_bible = json.dumps({k: bible.get(k) for k in ("logline", "genre", "world", "characters")}, ensure_ascii=False)
    with store._LOCK, _db() as conn:
        conn.execute("INSERT INTO studio_projects VALUES(?,?,?,?,?,?,?,?)",
                     (pid, title, minutes, premise, model_id, json.dumps(clock), now, now))
        _set_block(conn, pid, "human", human or "The creator of this movie.")
        _set_block(conn, pid, "persona", persona or "You are a visionary film director and showrunner.")
        _set_block(conn, pid, "movie_bible", movie_bible)
        _set_block(conn, pid, "style_bible", json.dumps(style, ensure_ascii=False))
        _set_block(conn, pid, "current_act", "")
    archive(pid, "bible", movie_bible)
    for c in bible.get("characters") or []:
        archive(pid, "character", json.dumps(c, ensure_ascii=False))
    return {**get_project(pid), "model_used": used}


def list_projects() -> list[dict[str, Any]]:
    with store._LOCK, _db() as conn:
        rows = conn.execute("SELECT p.id,p.title,p.minutes,p.updated_at,(SELECT COUNT(*) FROM studio_acts a WHERE a.project_id=p.id) "
                            "AS acts_written, json_array_length(p.clock) AS acts_total FROM studio_projects p ORDER BY updated_at DESC").fetchall()
    return [dict(r) for r in rows]


def get_project(pid: str) -> dict[str, Any]:
    with store._LOCK, _db() as conn:
        p = conn.execute("SELECT * FROM studio_projects WHERE id=?", (pid,)).fetchone()
        if p is None:
            raise KeyError(pid)
        acts = {r["act"]: {**json.loads(r["data"]), "model_id": r["model_id"]} for r in
                conn.execute("SELECT act,data,model_id FROM studio_acts WHERE project_id=? ORDER BY act", (pid,))}
        blocks = _blocks(conn, pid)
        n_archive = conn.execute("SELECT COUNT(*) FROM studio_archive WHERE project_id=?", (pid,)).fetchone()[0]
    clock = json.loads(p["clock"])
    for a in clock:
        a["written"] = a["act"] in acts
    return {"id": p["id"], "title": p["title"], "minutes": p["minutes"], "premise": p["premise"], "model_id": p["model_id"],
            "clock": clock, "acts": {str(k): v for k, v in acts.items()}, "memory": blocks, "archive_items": n_archive}


def delete_project(pid: str) -> bool:
    with store._LOCK, _db() as conn:
        conn.execute("DELETE FROM studio_archive WHERE project_id=?", (pid,))
        conn.execute("DELETE FROM studio_acts WHERE project_id=?", (pid,))
        conn.execute("DELETE FROM studio_blocks WHERE project_id=?", (pid,))
        return conn.execute("DELETE FROM studio_projects WHERE id=?", (pid,)).rowcount > 0


def _normalize_scenes(scenes: list[dict[str, Any]], start: int, end: int) -> list[dict[str, Any]]:
    """Make scenes cover the act's minutes in order, with no gaps or overlaps."""
    scenes = [s for s in scenes if isinstance(s, dict)]
    if not scenes:
        raise StudioError("the model returned no scenes")
    span = end - start
    weights = [max(0.25, float(s.get("minute_end", 0)) - float(s.get("minute_start", 0))) for s in scenes]
    total, t = sum(weights), float(start)
    for s, w in zip(scenes, weights):
        s["minute_start"] = round(t, 2)
        t += span * w / total
        s["minute_end"] = round(t, 2)
    scenes[-1]["minute_end"] = float(end)
    return scenes


async def write_act(pid: str, act_no: int, model_id: str | None = None, notes: str = "") -> dict[str, Any]:
    proj = get_project(pid)
    clock = {a["act"]: a for a in proj["clock"]}
    if act_no not in clock:
        raise KeyError(f"act {act_no}")
    act = clock[act_no]
    prev = proj["acts"].get(str(act_no - 1))
    query = " ".join([act.get("beat", ""), notes, (prev or {}).get("act_summary", "")])
    memories = recall(pid, query)
    span = act["end"] - act["start"]
    n_scenes = max(2, min(8, round(span / 2.5)))
    system = proj["memory"].get("persona", "") + (
        "\nYou write screenplay acts in a strict template. Stay true to the movie bible and style bible in your memory: "
        "same character names, looks and colors. Every scene needs real dialogue and a concrete camera, color and music choice. "
        "Use EXT. for outdoor places and INT. for indoor ones; location is only the place name (time goes in time_of_day).\n\n"
        "CORE MEMORY:\n" + _core_memory(proj["memory"]))
    if memories:
        system += "\n\nRECALLED FROM ARCHIVAL MEMORY:\n" + "\n".join(f"- ({m['kind']}) {m['text'][:600]}" for m in memories)
    user = (f"Write {act['label']} of '{proj['title']}' covering minutes {act['start']} to {act['end']} ({span} minutes) "
            f"in about {n_scenes} scenes. Beat for this act: {act.get('beat') or 'continue the story'}.\n"
            + (f"Previously: {prev['act_summary']}\n" if prev else "")
            + (f"Creator notes: {notes}\n" if notes else ""))
    data, used = await _structured(model_id or proj["model_id"], system, user, SCENE_SCHEMA, 3500)
    data["scenes"] = _normalize_scenes(list(data.get("scenes") or []), act["start"], act["end"])
    data.update({"act": act_no, "label": act["label"], "start": act["start"], "end": act["end"]})
    now = time.time()
    with store._LOCK, _db() as conn:
        conn.execute("INSERT OR REPLACE INTO studio_acts VALUES(?,?,?,?,?)", (pid, act_no, json.dumps(data, ensure_ascii=False), used, now))
        _set_block(conn, pid, "current_act", f"{act['label']} ({act['start']}-{act['end']} min): {data.get('act_summary', '')}")
        conn.execute("UPDATE studio_projects SET updated_at=? WHERE id=?", (now, pid))
    archive(pid, f"act {act_no} summary", data.get("act_summary", ""))
    for s in data["scenes"]:
        archive(pid, f"act {act_no} scene", f"{s['int_ext']} {s['location']} - {s['time_of_day']}: {s['action']} "
                + " ".join(f"{d['character']}: {d['line']}" for d in s.get("dialogue") or []))
    return {**data, "model_id": used, "recalled": len(memories)}


def scenes_between(pid: str, a: float, b: float) -> list[dict[str, Any]]:
    proj = get_project(pid)
    out = []
    for act in proj["acts"].values():
        for s in act["scenes"]:
            if s["minute_end"] > a and s["minute_start"] < b:
                out.append({**s, "act": act["act"]})
    return sorted(out, key=lambda s: s["minute_start"])


def _mmss(m: float) -> str:
    return f"{int(m // 60):d}:{int(m % 60):02d}:{int(round((m % 1) * 60)) % 60:02d}"


def screenplay(pid: str) -> str:
    """Fountain screenplay text (opens in Highland, Fade In, WriterSolo, Final Draft import)."""
    proj = get_project(pid)
    lines = [f"Title: {proj['title']}", f"Credit: Written with Kingdom AI OS", f"Notes: {proj['minutes']} minutes", "", ""]
    for act in sorted(proj["acts"].values(), key=lambda x: x["act"]):
        lines += [f"# {act['label']} ({act['start']}-{act['end']} min)", ""]
        for s in act["scenes"]:
            lines += [f"{s['int_ext']} {s['location'].upper()} - {s['time_of_day'].upper()}", "",
                      f"[[{_mmss(s['minute_start'])} to {_mmss(s['minute_end'])} | Camera: {s['camera']} | Color: {s['color']} | Music: {s['music']}]]", "",
                      s["action"], ""]
            for d in s.get("dialogue") or []:
                lines += [d["character"].upper(), d["line"], ""]
    return "\n".join(lines)


def shot_list(pid: str) -> list[dict[str, Any]]:
    """One prompt per scene for video models (Wan 2.1 / LTX-Video / ComfyUI)."""
    proj = get_project(pid)
    style = proj["memory"].get("style_bible", "")
    shots = []
    for act in sorted(proj["acts"].values(), key=lambda x: x["act"]):
        for i, s in enumerate(act["scenes"], 1):
            shots.append({"id": f"A{act['act']:02d}S{i:02d}", "minute_start": s["minute_start"], "minute_end": s["minute_end"],
                          "seconds": round((s["minute_end"] - s["minute_start"]) * 60),
                          "prompt": f"{s['int_ext']} {s['location']}, {s['time_of_day']}. {s['action']} Camera: {s['camera']}. "
                                    f"Color: {s['color']}.",
                          "music": s["music"], "style_bible": style})
    return shots


async def research(pid: str, question: str) -> list[dict[str, str]]:
    """Free web research (DuckDuckGo) saved to the movie's archival memory."""
    get_project(pid)
    import asyncio
    from app.services import shield
    shield.check_user(question)
    hits = await assistant.web_search(question, limit=6)
    hits = await asyncio.to_thread(shield.clean_untrusted, hits)
    for h in hits:
        archive(pid, "research", f"{h['title']} ({h['url']}): {h['snippet']}")
    return hits
