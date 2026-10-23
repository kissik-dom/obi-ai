"""Agent 3: External Scout Agent A (6h Discovery of New OBLITERATED LLMs & Open-Source Tools -> Quarantine)."""

from __future__ import annotations

from typing import Dict

from backend.agents.skills.new_llm_skill import execute_new_llm_skill
from backend.core import config
from backend.core.stores import QDRANT_STORE, utc_now


def run_external_scout_scan(topic: str = "huihui-ai obliterated releases") -> Dict[str, str]:
    """Scan model/tool ecosystem and stage newly discovered candidates in quarantine maturity first."""
    if not config.FLAGS.ENABLE_DISCOVERY:
        return {"status": "disabled", "timestamp": utc_now()}

    candidate_id = "huihui-scout-qwen3.9-preview-32b"
    rec = execute_new_llm_skill(
        model_id=candidate_id,
        canonical_name="Huihui-Scout-Qwen3.9-Preview-32B-OBLITERATED",
        specialty=f"Scouted candidate for '{topic}' staged in quarantine before benchmark gate",
        tier="X",
        guardrail="OBLITERATED",
        maturity="quarantine",
    )
    QDRANT_STORE.upsert_document(
        tab="marketplace",
        title=f"External Scout Discovery: {rec.canonicalName}",
        content=f"Discovered {rec.id} with license {rec.license}; placed in quarantine pending Testing Agent pass.",
        source_uri="scout://huggingface-openrouter-6h",
    )
    return {
        "status": "staged_in_quarantine",
        "discovered_model": rec.id,
        "maturity": rec.maturity,
        "timestamp": utc_now(),
    }
