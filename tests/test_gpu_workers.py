"""Verify GPU Worker Agent concurrency partitioning across Vultr A100 worker slots."""

from backend.agents.gpu_worker_agent import run_parallel_gpu_batch


def test_gpu_worker_partitioning() -> None:
    res = run_parallel_gpu_batch(total_images=100, workers=20, model_id="gemma-4-it-qat-12b", sandbox_id="sbx-gpu-100")
    assert res["workers_allocated"] == 20
    assert res["images_per_worker"] == 5
    assert res["total_images_generated"] == 100
    assert res["single_unified_batch"] is True
