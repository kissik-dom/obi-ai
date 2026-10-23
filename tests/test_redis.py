"""Verify Redis FIFO queue enqueue, depth, and dequeue semantics."""

from backend.core.stores import REDIS_STORE


def test_redis_fifo_queue_roundtrip() -> None:
    qname = "kingdom:test:queue"
    REDIS_STORE.enqueue(qname, {"job": "first"})
    REDIS_STORE.enqueue(qname, {"job": "second"})
    assert REDIS_STORE.depth(qname) >= 2
    assert REDIS_STORE.dequeue(qname) == {"job": "first"}
    assert REDIS_STORE.dequeue(qname) == {"job": "second"}
