"""Skill: Programmatically create and register a new Tab (25->28+) with the 10-endpoint grammar."""

from __future__ import annotations

from pathlib import Path
from typing import List

from backend.core import config
from backend.core.schemas import NewTabSkillRequest, NewTabSkillResponse, TabSpecRecord
from backend.core.tab_registry import TAB_REGISTRY, register_dynamic_tab
from backend.core.tool_registry import list_tools


def execute_new_tab_skill(req: NewTabSkillRequest) -> NewTabSkillResponse:
    """Generate router module on disk and register the new tab live without breaking existing tabs."""
    if not config.FLAGS.ENABLE_TAB_BUILDER:
        existing = TAB_REGISTRY.get(req.slug) or list(TAB_REGISTRY.values())[0]
        return NewTabSkillResponse(
            tab=existing,
            files_created=[],
            total_tabs_active=len(TAB_REGISTRY),
            status="disabled_by_flag",
        )

    existing_spec = TAB_REGISTRY.get(req.slug)
    next_index = existing_spec.index if existing_spec else (max(t.index for t in TAB_REGISTRY.values()) + 1)
    cat_tools = []
    for cat in req.tool_categories:
        cat_tools.extend([t.name for t in list_tools(category=cat)[:4]])
    if not cat_tools:
        cat_tools = ["Qdrant 768d", "MinIO S3", "Vault HSM"]

    spec = TabSpecRecord(
        index=next_index,
        slug=req.slug,
        title=req.title,
        chapter=f"Chapter {next_index:02d}: {req.title}",
        accent=req.accent,
        purpose=req.purpose,
        best_llm=req.best_llm,
        top_llms=[req.best_llm, "qwen3.8-27b-2.19m", "ling-3.1-flash-1m", "deepseek-v4-flash", "agents-a1-35b"],
        tool_categories=req.tool_categories,
        top_tools=cat_tools[:10],
        agents=["internal_optimizer_agent", "testing_agent", "bugfix_agent"],
        router_logic=f"Routes '{req.slug}' workloads to {req.best_llm} inside equipped sovereign sandboxes.",
        core=False,
    )
    register_dynamic_tab(spec)

    router_path = config.BACKEND_ROOT / "api" / "routers" / f"{req.slug}.py"
    created: List[str] = []
    if not router_path.exists():
        router_code = (
            f'"""Auto-generated Sovereign Tab Router for {req.title} ({req.slug})."""\n\n'
            f"from backend.api.routers._tab_factory import build_tab_router\n\n"
            f'router = build_tab_router("{req.slug}")\n'
        )
        router_path.parent.mkdir(parents=True, exist_ok=True)
        router_path.write_text(router_code, encoding="utf-8")
        created.append(str(router_path.relative_to(config.REPO_ROOT)))

    return NewTabSkillResponse(
        tab=spec,
        files_created=created,
        total_tabs_active=len(TAB_REGISTRY),
        status="registered",
    )
