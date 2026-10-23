"""Tab 20: Music / Audio Vocal Tuning Router (10-Section Grammar + Demucs/GSnap/MAutoPitch/Graillon/94-808 Pipeline)."""

from __future__ import annotations

import asyncio

from fastapi import APIRouter

from backend.agents.vocal_tuning_agent import run_vocal_tuning_pipeline
from backend.api.routers._tab_factory import build_tab_router
from backend.core.schemas import VocalTuningRequest, VocalTuningResponse

router = build_tab_router("music")
domain_router = APIRouter(prefix="/api/music", tags=["domain:music"])


@domain_router.post("/vocal-tune", response_model=VocalTuningResponse)
async def post_vocal_tune(payload: VocalTuningRequest) -> VocalTuningResponse:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: run_vocal_tuning_pipeline(payload))
