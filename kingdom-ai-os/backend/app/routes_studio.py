"""TV / Movie Studio API: any-length movies, long-term memory, minute scrubbing, exports."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from app.routes_workspace import API_PREFIX
from app.services import studio
from app.services.assistant import ProviderError

router = APIRouter(prefix=API_PREFIX + "/studio", tags=["studio"])


class NewMovie(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    minutes: int = Field(ge=1, le=600)
    premise: str = Field(min_length=3, max_length=8000)
    persona: str = Field(default="", max_length=4000)
    human: str = Field(default="", max_length=4000)
    model_id: str | None = Field(default=None, max_length=200)


class WriteAct(BaseModel):
    model_id: str | None = Field(default=None, max_length=200)
    notes: str = Field(default="", max_length=4000)


class Research(BaseModel):
    question: str = Field(min_length=3, max_length=500)


def _project(pid: str) -> dict[str, Any]:
    try:
        return studio.get_project(pid)
    except KeyError:
        raise HTTPException(404, "Movie not found") from None


@router.get("/clock")
async def clock(minutes: int = Query(ge=1, le=600)) -> list[dict[str, Any]]:
    return studio.plan_clock(minutes)


@router.get("/projects")
async def projects() -> list[dict[str, Any]]:
    return studio.list_projects()


@router.post("/projects")
async def create(payload: NewMovie) -> dict[str, Any]:
    try:
        return await studio.create_project(payload.title, payload.minutes, payload.premise, payload.persona, payload.human, payload.model_id)
    except (studio.StudioError, ProviderError, ValueError) as exc:
        raise HTTPException(502, str(exc)[:400]) from exc


@router.get("/projects/{pid}")
async def project(pid: str) -> dict[str, Any]:
    return _project(pid)


@router.delete("/projects/{pid}")
async def delete(pid: str) -> dict[str, bool]:
    if not studio.delete_project(pid):
        raise HTTPException(404, "Movie not found")
    return {"deleted": True}


@router.post("/projects/{pid}/acts/{act}")
async def write(pid: str, act: int, payload: WriteAct) -> dict[str, Any]:
    _project(pid)
    try:
        return await studio.write_act(pid, act, payload.model_id, payload.notes)
    except KeyError:
        raise HTTPException(404, "No such act in this movie") from None
    except (studio.StudioError, ProviderError, ValueError) as exc:
        raise HTTPException(502, str(exc)[:400]) from exc


@router.get("/projects/{pid}/minutes")
async def minutes(pid: str, start: float = Query(ge=0), end: float = Query(gt=0)) -> list[dict[str, Any]]:
    _project(pid)
    return studio.scenes_between(pid, start, end)


@router.get("/projects/{pid}/recall")
async def recall(pid: str, q: str = Query(min_length=2, max_length=300)) -> list[dict[str, str]]:
    _project(pid)
    return studio.recall(pid, q, limit=10)


@router.post("/projects/{pid}/research")
async def research(pid: str, payload: Research) -> list[dict[str, str]]:
    _project(pid)
    return await studio.research(pid, payload.question)


@router.get("/projects/{pid}/screenplay.fountain", response_class=PlainTextResponse)
async def fountain(pid: str) -> str:
    _project(pid)
    return studio.screenplay(pid)


@router.get("/projects/{pid}/shots")
async def shots(pid: str) -> list[dict[str, Any]]:
    _project(pid)
    return studio.shot_list(pid)
