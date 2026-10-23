"""Verify 600+ Open-Source Tools (Categories A-L, >=50 in each A-K) + 300 Composio = 920+ Total Tools & Lazy Loader."""

from backend.core.schemas import ToolExecuteRequest
from backend.core.tool_registry import count_open_source_tools, lazy_execute_tool, list_tools


def test_tool_counts_per_category() -> None:
    assert count_open_source_tools() >= 620
    assert len(list_tools()) >= 920
    for cat in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]:
        cat_items = list_tools(category=cat)  # type: ignore[arg-type]
        assert len(cat_items) >= 50, f"Category {cat} has fewer than 50 tools: {len(cat_items)}"


def test_lazy_tool_execution_and_graceful_fallback() -> None:
    ok = lazy_execute_tool(ToolExecuteRequest(tool_id="cat-h-01", tab="engineering", action="decompile"))
    assert ok.status == "completed"
    assert ok.lazy_loaded is True

    fb = lazy_execute_tool(ToolExecuteRequest(tool_id="nonexistent-tool-xyz", tab="opensource", action="probe"))
    assert fb.status == "fallback_completed"
