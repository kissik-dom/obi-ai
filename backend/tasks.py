"""Celery Distributed Worker & Celery Beat Autonomous Schedules (6h Scout A, Daily Optimizer B, TEST_INTERVAL Testing, 10s BugFix)."""

from __future__ import annotations

from celery import Celery
from celery.schedules import crontab

from backend.agents.bugfix_agent import run_bugfix_cycle
from backend.agents.external_scout_agent import run_external_scout_scan
from backend.agents.internal_optimizer_agent import run_internal_optimizer
from backend.agents.testing_agent import run_continuous_verification
from backend.core import config
from backend.core.schemas import BugfixTriggerRequest

celery_app = Celery(
    "kingdom_ai_os",
    broker=config.SETTINGS.redis_url,
    backend=config.SETTINGS.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "bugfix-self-heal-every-10s": {
            "task": "backend.tasks.bugfix_heartbeat_task",
            "schedule": 10.0,
        },
        "testing-agent-interval": {
            "task": "backend.tasks.testing_agent_task",
            "schedule": float(config.SETTINGS.test_interval),
        },
        "external-scout-every-6h": {
            "task": "backend.tasks.external_scout_task",
            "schedule": crontab(minute=0, hour="*/6"),
        },
        "internal-optimizer-daily": {
            "task": "backend.tasks.internal_optimizer_task",
            "schedule": crontab(minute=0, hour=2),
        },
    },
)


@celery_app.task(name="backend.tasks.bugfix_heartbeat_task")
def bugfix_heartbeat_task() -> dict[str, object]:
    if not config.FLAGS.ENABLE_SELF_UPDATE:
        return {"status": "disabled"}
    return run_bugfix_cycle(BugfixTriggerRequest(failed_endpoints=[], reason="10s-beat")).model_dump()


@celery_app.task(name="backend.tasks.testing_agent_task")
def testing_agent_task() -> dict[str, str]:
    return run_continuous_verification()


@celery_app.task(name="backend.tasks.external_scout_task")
def external_scout_task() -> dict[str, str]:
    return run_external_scout_scan()


@celery_app.task(name="backend.tasks.internal_optimizer_task")
def internal_optimizer_task() -> dict[str, str]:
    return run_internal_optimizer()
