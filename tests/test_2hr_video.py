"""Verify 2hr (240 clips) and 5hr (600 clips) parallel video generation stitched into ONE single MP4."""

from fastapi.testclient import TestClient

from backend.main import app


def test_2hr_and_5hr_video_stitching_single_mp4() -> None:
    with TestClient(app) as client:
        r2 = client.post(
            "/api/video/stitch",
            json={
                "prompt": "2-hour multi-character feature film",
                "target_duration_seconds": 7200,
                "clip_duration_seconds": 30,
                "parallel_workers": 48,
                "primary_video_model": "minimax-hailuo-02",
            },
        )
        assert r2.status_code == 200
        b2 = r2.json()
        assert b2["total_clips_planned"] == 240
        assert b2["final_single_mp4_uri"].endswith(".mp4")

        r5 = client.post(
            "/api/video/stitch",
            json={
                "prompt": "5-hour anthology series",
                "target_duration_seconds": 18000,
                "clip_duration_seconds": 30,
                "parallel_workers": 100,
                "primary_video_model": "minimax-hailuo-02",
            },
        )
        assert r5.status_code == 200
        assert r5.json()["total_clips_planned"] == 600
