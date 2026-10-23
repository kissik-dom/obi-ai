"""Verify 200x5=1,000 Parallel GPU Pictures & 7-Subagent Biometric Isolation delivered in ONE batch."""

from fastapi.testclient import TestClient

from backend.main import app


def test_1000_pics_and_biometric_isolation_single_batch() -> None:
    with TestClient(app) as client:
        res = client.post(
            "/api/images/consistency",
            json={
                "prompt": "Photoreal editorial portrait with natural pores and freckles",
                "isolation_mode": "jewelry_only",
                "stone_filter": "diamonds_only",
                "batch_count": 1000,
            },
        )
        assert res.status_code == 200
        body = res.json()
        assert body["model_used"] == "gemma-4-it-qat-12b"
        assert body["total_images_in_single_batch"] == 1000
        assert body["gpu_workers_allocated"] == 200
        assert body["zero_skin_bleed_verified"] is True
        assert len(body["subagents_deployed"]) == 7
        assert body["unified_zip_uri"].endswith(".zip")
