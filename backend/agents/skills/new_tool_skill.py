"""Skill: Register a new lazy-loaded Open-Source ToolRecord into the 920+ Tool Registry."""

from __future__ import annotations

from typing import List

from backend.core.schemas import ToolCategory, ToolRecord
from backend.core.tool_registry import STAGE_BY_CATEGORY, register_tool


def execute_new_tool_skill(
    tool_id: str,
    name: str,
    category: ToolCategory = "L",
    tabs_used_by: List[str] | None = None,
) -> ToolRecord:
    rec = ToolRecord(
        id=tool_id,
        name=name,
        category=category,
        categoryName=f"Dynamic Category {category}",
        version="2026.10",
        license="MIT",
        install_cmd=f"pip install --lazy {tool_id}",
        python_import=f"lazy_adapters.{tool_id.replace('-', '_')}",
        docker_stage=STAGE_BY_CATEGORY.get(category, "base"),
        api_endpoint=f"/api/tools/execute/{tool_id}",
        tabs_used_by=tabs_used_by or ["opensource", "home"],
        lazy_loaded=True,
        open_source=True,
    )
    return register_tool(rec)
