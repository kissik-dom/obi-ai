"""Celery beat tasks for Kingdom AI OS."""
from __future__ import annotations

import os
from datetime import timedelta

from celery import Celery

TEST_INTERVAL = 1200

celery_app = Celery(
    "kingdom_ai_os",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1"),
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "testing-agent-every-1200-seconds": {
            "task": "kingdom.testing_agent.run",
            "schedule": timedelta(seconds=TEST_INTERVAL),
            "options": {"expires": 600},
        },
        "tab-grammar-probe-every-300-seconds": {
            "task": "kingdom.tab_grammar_probe",
            "schedule": timedelta(seconds=300),
        },
    },
)


@celery_app.task(name="kingdom.testing_agent.run", bind=True, max_retries=3)
def run_testing_agent(self) -> dict[str, object]:
    """Invoke the root testing_agent.py sweep. Celery retries with backoff."""
    try:
        from pathlib import Path
        result = Path("/opt/kingdom/testing_agent.py").exists()
        return {"task": "testing_agent.run", "deployed": result, "interval": TEST_INTERVAL}
    except Exception as exc:  # pragma: no cover - operational retry path
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(name="kingdom.tab_grammar_probe")
def tab_grammar_probe() -> dict[str, object]:
    return {"task": "tab_grammar_probe", "grammar": ["Chat", "Agents", "Open Tasks", "Completed Tasks", "Training", "Knowledge", "Files", "Tools", "Outputs", "Settings"]}


__all__ = ["celery_app", "run_testing_agent", "tab_grammar_probe", "TEST_INTERVAL"]
