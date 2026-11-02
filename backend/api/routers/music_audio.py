"""Router for Music/Audio Vocal Tuning (music_audio)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "music_audio",
    "Music/Audio Vocal Tuning",
    "Music and audio vocal tuning with GSnap, MAutoPitch, Spleeter, Demucs, RVC, and mixing tools.",
)

__all__ = ["router"]
