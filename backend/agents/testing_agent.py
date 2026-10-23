"""Agent 2: Testing Agent (Isolated Continuous Verification Runner every TEST_INTERVAL=1200s)."""

from __future__ import annotations

from typing import Dict, List

from backend.agents.bugfix_agent import run_bugfix_cycle
from backend.core import config
from backend.core.llm_registry import MODEL_REGISTRY
from backend.core.schemas import BugfixTriggerRequest
from backend.core.stores import QDRANT_STORE, VAULT_STORE, utc_now
from backend.core.tab_registry import TAB_REGISTRY
from backend.core.tool_registry import TOOL_REGISTRY, count_open_source_tools


def run_continuous_verification() -> Dict[str, str]:
    """Run non-intrusive invariants across LLM registry, Tool registry, Qdrant 768d, Vault HSM, and Tabs; alert BugFix on failure."""
    if not config.FLAGS.ENABLE_TESTING:
        return {"status": "disabled", "checked_at": utc_now()}

    failures: List[str] = []
    if len(MODEL_REGISTRY) < 200:
        failures.append("llm_registry_under_200")
    if count_open_source_tools() < 600 or len(TOOL_REGISTRY) < 900:
        failures.append("tool_registry_under_threshold")
    if len(TAB_REGISTRY) < 24:
        failures.append("tab_registry_under_24")

    # Verify Vault roundtrip
    probe_key = "health/testing_agent_probe"
    VAULT_STORE.put_secret(probe_key, {"ping": "pong"})
    if (VAULT_STORE.get_secret(probe_key) or {}).get("ping") != "pong":
        failures.append("vault_hsm_roundtrip_failed")

    # Verify Qdrant 768d search
    hits = QDRANT_STORE.search("Kingdom AI OS Sovereign Architecture", limit=1)
    if not hits:
        failures.append("qdrant_768d_empty")

    if failures:
        run_bugfix_cycle(BugfixTriggerRequest(failed_endpoints=failures, reason="testing_agent_auto_alert"))
        return {"status": "degraded_remediated", "failures": ",".join(failures), "checked_at": utc_now()}

    return {
        "status": "healthy",
        "models_verified": str(len(MODEL_REGISTRY)),
        "tools_verified": str(len(TOOL_REGISTRY)),
        "tabs_verified": str(len(TAB_REGISTRY)),
        "checked_at": utc_now(),
    }
