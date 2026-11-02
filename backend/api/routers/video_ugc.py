"""Router for Video/UGC/TV/Movies (video_ugc)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "video_ugc",
    "Video/UGC/TV/Movies",
    "UGC and cinematic video with MiniMax Hailuo-02, Wan 2.1, LTX-Video, Kling 2.0, FFmpeg stitching, and shot lists.",
)

__all__ = ["router"]
