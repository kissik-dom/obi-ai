"""Skill: Dynamically register a custom AgentRecord into the Sovereign Agent Registry."""

from __future__ import annotations

from typing import Dict, List

from backend.core.schemas import AgentRecord

CUSTOM_AGENTS: Dict[str, AgentRecord] = {}


def execute_new_agent_skill(
    agent_id: str,
    name: str,
    role: str,
    primary_llm: str = "qwen3.8-27b-2.19m",
    tabs: List[str] | None = None,
) -> AgentRecord:
    rec = AgentRecord(
        id=agent_id,
        name=name,
        role=role,
        group="custom",
        primary_llm=primary_llm,
        backup_llms=["deepseek-v4-flash", "ling-3.1-flash-1m"],
        tools=["cat-l-01", "cat-l-02", "cat-l-03"],
        tabs=tabs or ["agents", "home"],
        turn_off_flag="ENABLE_SELF_UPDATE",
        enabled=True,
        status="online",
        cadence="on-demand",
        description=f"Custom registered agent: {role}",
    )
    CUSTOM_AGENTS[agent_id] = rec
    return rec
