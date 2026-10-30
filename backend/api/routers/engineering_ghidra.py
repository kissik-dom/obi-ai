"""Router for Engineering GHIDRA Anti-Gravity (engineering_ghidra)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "engineering_ghidra",
    "Engineering GHIDRA Anti-Gravity",
    "Reverse engineering and anti-gravity engineering sandbox with GHIDRA, FreeCAD, OpenSCAD, Blender, and KiCad.",
)

__all__ = ["router"]
