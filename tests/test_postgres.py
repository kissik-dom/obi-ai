"""Verify SQLAlchemy 2.0 relational task store, idempotency deduplication, and all 10 task states."""

from backend.core.schemas import TaskCreateRequest, TaskState
from backend.core.stores import POSTGRES_STORE


def test_idempotency_and_all_10_task_states() -> None:
    req = TaskCreateRequest(
        title="Idempotent Ledger Audit",
        prompt="Verify bilateral ledger",
        tab="finance",
        idempotency_key="idem-fixed-ledger-001",
    )
    t1 = POSTGRES_STORE.create_task(req)
    t2 = POSTGRES_STORE.create_task(req)
    assert t1.id == t2.id

    all_states: list[TaskState] = [
        "queued",
        "running",
        "waiting",
        "approval_required",
        "blocked",
        "failed",
        "scheduled",
        "recurring",
        "cancelled",
        "completed",
    ]
    for st in all_states:
        updated = POSTGRES_STORE.update_state(t1.id, st, f"State={st}")
        assert updated is not None
        assert updated.state == st
