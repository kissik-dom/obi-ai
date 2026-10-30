"""TV / Movie Studio: clock math, template lock, memory recall, minute jump, exports (model mocked)."""
import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import studio


def test_clock_any_length():
    acts = studio.plan_clock(137)
    assert len(acts) == 10 and acts[-1]["label"] == "Epilogue" and acts[-1]["end"] == 137
    assert [a["end"] - a["start"] for a in acts[:9]] == [15] * 9
    assert studio.plan_clock(73)[-1] == {"act": 5, "label": "Act 5", "start": 60, "end": 73}
    assert studio.plan_clock(3) == [{"act": 1, "label": "Act 1", "start": 0, "end": 3}]


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("KAIOS_DB_PATH", str(tmp_path / "t.db"))

    async def fake(model_id, system, user, schema, max_tokens):
        if "act_beats" in schema["properties"]:
            return {"logline": "A keeper guards a light.", "genre": "drama", "world": "Stormy island",
                    "characters": [{"name": "Mara", "role": "keeper", "look": "green eyes, red coat", "want": "peace"}],
                    "style": {"color_palette": "teal and amber", "lenses_camera": "35mm", "music": "cello", "tone": "quiet"},
                    "act_beats": ["arrival", "storm"]}, "ollama/test"
        assert "Mara" in system  # core memory is loaded into every act
        return {"act_summary": "Mara arrives at the lighthouse.", "scenes": [
            {"minute_start": 0, "minute_end": 9, "int_ext": "EXT.", "location": "Pier", "time_of_day": "Dusk", "action": "Mara lands.",
             "dialogue": [{"character": "Mara", "line": "Hello, light."}], "camera": "wide", "color": "amber", "music": "cello"},
            {"minute_start": 9, "minute_end": 30, "int_ext": "INT.", "location": "Lamp room", "time_of_day": "Night", "action": "She lights it.",
             "dialogue": [], "camera": "close", "color": "teal", "music": "silence"}]}, "ollama/test"
    monkeypatch.setattr(studio, "_structured", fake)
    return TestClient(app)


def test_movie_flow(client):
    r = client.post("/api/v1/studio/projects", json={"title": "Light", "minutes": 20, "premise": "A keeper and a storm"})
    assert r.status_code == 200, r.text
    m = r.json(); pid = m["id"]
    assert [a["label"] for a in m["clock"]] == ["Act 1", "Act 2"] and m["clock"][0]["beat"] == "arrival"
    assert "Mara" in m["memory"]["movie_bible"] and "teal" in m["memory"]["style_bible"]
    a = client.post(f"/api/v1/studio/projects/{pid}/acts/1", json={}).json()
    assert a["scenes"][0]["minute_start"] == 0 and a["scenes"][-1]["minute_end"] == 15  # normalized to the act
    assert client.get(f"/api/v1/studio/projects/{pid}").json()["memory"]["current_act"].startswith("Act 1")
    assert any("lighthouse" in x["text"] for x in client.get(f"/api/v1/studio/projects/{pid}/recall?q=lighthouse").json())
    hits = client.get(f"/api/v1/studio/projects/{pid}/minutes?start=10&end=11").json()
    assert len(hits) == 1 and hits[0]["location"] == "Lamp room"
    fountain = client.get(f"/api/v1/studio/projects/{pid}/screenplay.fountain").text
    assert "EXT. PIER - DUSK" in fountain and "MARA" in fountain
    shots = client.get(f"/api/v1/studio/projects/{pid}/shots").json()
    assert shots[0]["id"] == "A01S01" and shots[0]["seconds"] > 0
    assert client.post(f"/api/v1/studio/projects/{pid}/acts/9", json={}).status_code == 404
    assert client.get("/api/v1/studio/projects").json()[0]["acts_written"] == 1
    assert client.delete(f"/api/v1/studio/projects/{pid}").json() == {"deleted": True}
