"""Hermes-Tool-Use: Deterministic JSON Schema Tool Invoker across all 920 Tools."""

from __future__ import annotations

from typing import Dict

from backend.core import config
from backend.core.schemas import ToolExecuteRequest, ToolExecuteResponse
from backend.core.tool_registry import lazy_execute_tool


def invoke_hermes_tool(tool_id: str, tab: str, params: Dict[str, str]) -> ToolExecuteResponse:
    """Invoke a registered tool through Hermes-Tool-Use structured validation."""
    if not config.FLAGS.ENABLE_HERMES:
        return lazy_execute_tool(ToolExecuteRequest(tool_id=tool_id, tab=tab, action="direct_bypass", params=params))
    return lazy_execute_tool(ToolExecuteRequest(tool_id=tool_id, tab=tab, action="hermes_structured_call", params=params))
