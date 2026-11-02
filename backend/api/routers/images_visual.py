"""Router for Images/Visual AI (images_visual)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "images_visual",
    "Images/Visual AI",
    "Image generation with FLUX.1, Juggernaut, SAM2, ControlNet, and vision models; visual QA and consistency.",
)

__all__ = ["router"]
