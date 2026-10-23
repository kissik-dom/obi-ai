"""Verify MinIO (minio-py only) atomic temp-then-rename object writes with zero leftover .tmp artifacts."""

from backend.core import config
from backend.core.stores import MINIO_STORE


def test_minio_atomic_temp_then_rename() -> None:
    bucket = config.SETTINGS.finished_bucket
    payload = b"atomic-sovereign-deliverable-bytes"
    rec = MINIO_STORE.put_bytes_atomic(bucket, "test_atomic/output.bin", payload, tab="coding")
    assert rec.size_bytes == len(payload)
    assert MINIO_STORE.get_bytes(bucket, "test_atomic/output.bin") == payload

    folder = MINIO_STORE.root / bucket / "test_atomic"
    leftover_tmps = [p.name for p in folder.iterdir() if ".tmp." in p.name]
    assert leftover_tmps == []
