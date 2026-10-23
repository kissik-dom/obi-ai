"""Tab 18: Images / Visual AI Router (10-Section Grammar + 7-Subagent Biometric Isolation & 1000-Pic Batch)."""

from __future__ import annotations

import asyncio

from fastapi import APIRouter

from backend.agents.image_consistency_agent import run_image_consistency_batch
from backend.api.routers._tab_factory import build_tab_router
from backend.core.schemas import ImageConsistencyRequest, ImageConsistencyResponse

router = build_tab_router("images")
domain_router = APIRouter(prefix="/api/images", tags=["domain:images"])


@domain_router.post("/consistency", response_model=ImageConsistencyResponse)
async def post_image_consistency(payload: ImageConsistencyRequest) -> ImageConsistencyResponse:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: run_image_consistency_batch(payload))
