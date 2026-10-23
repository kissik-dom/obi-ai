"""Verify Vocal Tuning Pipeline (GSnap, MAutoPitch, Graillon 2, Demucs/Spleeter 2/4/5 Stems & 94 Free 808s)."""

from fastapi.testclient import TestClient

from backend.main import app


def test_vocal_tuning_and_94_808_kit() -> None:
    with TestClient(app) as client:
        res = client.post(
            "/api/music/vocal-tune",
            json={
                "track_title": "Kingdom Session 01",
                "key_scale": "F# Minor",
                "retune_speed_ms": 6,
                "stems": 5,
                "include_808_kit": True,
            },
        )
        assert res.status_code == 200
        body = res.json()
        assert len(body["stems_generated"]) == 5
        assert body["eight_oh_eight_samples_available"] == 94
        assert body["mastered_wav_uri"].endswith(".wav")
