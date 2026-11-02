"""Hermes gateway: never-fail cascade, 14 specialist Hermes agents, and skill registry."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass(slots=True)
class HermesSkill:
    id: str
    name: str
    description: str
    fallback_model: str
    turnoff_flag: str


HERMES_SKILLS: List[HermesSkill] = [
    HermesSkill("hermes-router", "Hermes Router", "Routes every tab request to the best specialist and model fallback chain.", "tier-s-auto", "hermes_router"),
    HermesSkill("hermes-research", "Hermes Research", "Deep research ensemble with citation graph and re-ranking.", "tier-s-research", "hermes_research"),
    HermesSkill("hermes-scout", "Hermes External Scout", "External OSINT/news/scraping collection with source credibility scoring.", "tier-b-scout", "hermes_scout"),
    HermesSkill("hermes-coder", "Hermes Coder", "Plan, patch, test, and review code in isolated sandboxes.", "tier-s-coder", "hermes_coder"),
    HermesSkill("hermes-legal", "Hermes Legal", "Jurisdiction-aware legal research and privilege-conscious drafting.", "tier-s-legal", "hermes_legal"),
    HermesSkill("hermes-finance", "Hermes Finance", "Financial model, ledger, and investment analysis.", "tier-s-finance", "hermes_finance"),
    HermesSkill("hermes-osint", "Hermes OSINT", "Evidence-custody OSINT with tool orchestration.", "tier-s-osint", "hermes_osint"),
    HermesSkill("hermes-image", "Hermes Image", "Visual AI prompt, consistency, and QA routing.", "tier-v-image", "hermes_image"),
    HermesSkill("hermes-video", "Hermes Video", "Shot list, stitching, and UGC/cinematic generation.", "tier-v-video", "hermes_video"),
    HermesSkill("hermes-audio", "Hermes Audio", "Stem separation, vocal tuning, and mix delivery.", "tier-b-audio", "hermes_audio"),
    HermesSkill("hermes-security", "Hermes Security", "Triage alerts from CrowdSec, Wazuh, Suricata, Falco, Tetragon, and Cowrie.", "tier-s-admin", "hermes_security"),
    HermesSkill("hermes-cua", "Hermes CUA", "Computer-Use Agent orchestration across isolated CUA spaces.", "tier-b-cua", "hermes_cua"),
    HermesSkill("hermes-engineer", "Hermes Engineering", "GHIDRA/FreeCAD/OpenSCAD/Blender/KiCad engineering pipelines.", "tier-s-engineering", "hermes_engineering"),
    HermesSkill("hermes-comms", "Hermes Comms", "WAHA/Baileys/Evolution API messaging and conversation state.", "tier-b-comms", "hermes_comms"),
]


async def dispatch_hermes(payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Select a Hermes skill and return a LiteLLM Router fallback plan."""
    payload = payload or {}
    skill_id = str(payload.get("skill", "hermes-router"))
    model = str(payload.get("model", "tier-s-auto"))
    skill = next((item for item in HERMES_SKILLS if item.id == skill_id), HERMES_SKILLS[0])
    return {
        "gateway": "Obliteratus Hermes",
        "skill": skill.id,
        "model": model,
        "fallback_model": skill.fallback_model,
        "num_retries": 3,
        "timeout_seconds": 60,
        "routed_at": datetime.now(timezone.utc).isoformat(),
    }


__all__ = ["HERMES_SKILLS", "dispatch_hermes", "HermesSkill"]
