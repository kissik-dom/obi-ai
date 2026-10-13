from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from uuid import uuid4
from datetime import datetime, timezone

app = FastAPI(title="Kingdom AI OS — Task Service", version="0.1.0")


class TaskStatus(str, Enum):
    queued = "queued"
    running = "running"
    done = "done"
    failed = "failed"


class TaskIn(BaseModel):
    workspace: str
    intent: str
    payload: dict = {}


class Task(TaskIn):
    id: str
    status: TaskStatus
    created_at: str


_TASKS: dict[str, Task] = {}


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True, "service": "kingdom-task-api", "version": app.version}


@app.post("/tasks", response_model=Task)
def create_task(body: TaskIn) -> Task:
    task = Task(
        id=str(uuid4()),
        status=TaskStatus.queued,
        created_at=datetime.now(timezone.utc).isoformat(),
        **body.model_dump(),
    )
    _TASKS[task.id] = task
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    return _TASKS[task_id]


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(_TASKS.values())
