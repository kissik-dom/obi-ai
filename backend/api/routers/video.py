"""Tab 19: Video / UGC / TV / Movies Router (10-Section Grammar + 600-Clip Parallel Stitcher)."""

from __future__ import annotations

import asyncio

from fastapi import APIRouter

from backend.agents.video_stitching_agent import run_video_stitching_pipeline
from backend.api.routers._tab_factory import build_tab_router
from backend.core.schemas import VideoPipelineRequest, VideoPipelineResponse

router = build_tab_router("video")
domain_router = APIRouter(prefix="/api/video", tags=["domain:video"])


@domain_router.post("/stitch", response_model=VideoPipelineResponse)
async def post_video_stitch(payload: VideoPipelineRequest) -> VideoPipelineResponse:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: run_video_stitching_pipeline(payload))
