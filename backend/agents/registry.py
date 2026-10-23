"""Unified Sovereign Agent Catalog (12 Core Sovereign Agents + 14 Hermes Specialists + Custom Agents)."""

from __future__ import annotations

from typing import List, Optional

from backend.agents.skills.hermes.hermes_agent import list_hermes_agent_records
from backend.agents.skills.new_agent_skill import CUSTOM_AGENTS
from backend.core import config
from backend.core.llm_registry import complete_with_failover, route_model
from backend.core.schemas import (
    AgentRecord,
    AgentRunRequest,
    AgentRunResponse,
    RouterDecisionRequest,
    TaskCreateRequest,
)
from backend.core.stores import POSTGRES_STORE, equip_task_sandbox, utc_now
from backend.finished import archive_finished_sandbox


def _flag_enabled(flag_name: str) -> bool:
    return bool(config.get_flags_dict().get(flag_name, True))


def list_sovereign_12() -> List[AgentRecord]:
    defs = [
        ("bugfix_agent", "BugFix Agent", "10s OpenHands + SWE-agent + Aider Self-Healing", "qwen3-coder-next-80b", ["qwen3-coder-30b", "deepseek-v4-flash"], ["cat-l-13", "cat-l-14", "cat-l-15"], ["home", "coding", "engineering", "security", "tasks"], "ENABLE_SELF_UPDATE", "every 10s", "Continuously watches endpoints and container health via OpenHands, SWE-agent, Aider, Watchtower, and Keel."),
        ("testing_agent", "Testing Agent", "Isolated Continuous Verification Suite", "qwen3-coder-30b", ["qwen3-coder-next-80b", "deepseek-v4-flash"], ["cat-l-01", "cat-l-02", "cat-l-03"], ["home", "coding", "llm", "tasks", "marketplace"], "ENABLE_TESTING", "every TEST_INTERVAL (1200s)", "Executes non-intrusive invariants across registries, Qdrant 768d, MinIO, Vault HSM, and alerts BugFix Agent."),
        ("external_scout_agent", "External Scout Agent A", "6h Model & Open-Source Tool Discovery", "ling-3.1-flash-1m", ["huihui-qwen3.6-35b-a3b", "agents-a1-35b"], ["cat-f-01", "cat-d-01"], ["llm", "research", "opensource", "marketplace"], "ENABLE_DISCOVERY", "every 6h", "Scans HuggingFace, OpenRouter, GitHub, and Arxiv for new OBLITERATED models and open-source tools -> quarantine."),
        ("internal_optimizer_agent", "Internal Optimizer Agent B", "Daily Router, Prompt & Cost Optimizer", "deepseek-v4-flash", ["qwen3.8-27b-2.19m", "ling-3.1-flash-1m"], ["cat-l-09", "cat-l-10"], ["home", "llm", "finance", "investments", "business", "tasks"], "ENABLE_SELF_UPDATE", "daily 02:00 UTC", "Analyzes completed sandbox metrics to optimize LLM router scores, latency, and batch throughput."),
        ("cua_fleet_agent", "CUA Fleet Agent", "2,000 Cloud Spaces x 5 IG Business Accounts", "huihui4-moe-a4b-9b", ["ling-3.1-flash-1m", "moe-0.8b-2e"], ["cat-e-01", "cat-c-28", "cat-c-29"], ["web", "social", "leads", "real_estate", "osint"], "ENABLE_SANDBOX", "on-demand", "Controls 2,000 WireGuard + Falco eBPF isolated trycua/cua Boat cloud spaces managing 10,000 official accounts."),
        ("gpu_worker_agent", "GPU Worker Agent", "200x5=1,000 Parallel Render Aggregator", "gemma-4-it-qat-12b", ["gemma-4-e2b-5b", "qwen3.8-vision-28b"], ["cat-j-01", "cat-j-05", "cat-j-06"], ["images", "fashion", "video"], "ENABLE_IMAGE_CONSISTENCY", "on-demand", "Partitions 1,000-picture jobs across 200 GPU workers and packages all renders into one unified ZIP/PDF batch."),
        ("video_stitching_agent", "Video Stitching Agent", "600-Clip Parallel Cinema & UGC Stitcher", "minimax-hailuo-02", ["wan-2.1-14b", "ltx-video-13b", "qwythos-9b-classic"], ["cat-k-01", "cat-a-01", "cat-a-04", "cat-b-06"], ["video", "social", "music"], "ENABLE_VIDEO_AGENT", "on-demand", "Splits 2hr-5hr timelines into 600 parallel 30s clips and stitches via FFmpeg + MoviePy + WhisperX into one MP4."),
        ("image_consistency_agent", "Image Consistency Director", "7-Subagent Biometric Isolation & Photoreal Skin", "gemma-4-it-qat-12b", ["qwen3.8-vision-28b", "flux-1-dev-12b"], ["cat-j-15", "cat-j-16", "cat-j-21", "cat-j-22"], ["images", "fashion"], "ENABLE_IMAGE_CONSISTENCY", "on-demand", "Preserves Face1 biometrics while isolating Hair Only, Jewelry Only, Clothes Only, or Background Only with zero bleed."),
        ("security_honeypot_agent", "Security Honeypot Agent", "Cowrie Decoys, WAF/eBPF & BIPA VideoKYC", "cyberstrike-offsec-35b", ["glm-5.3-flash-fp8", "qwen3.8-27b-2.19m"], ["cat-g-01", "cat-g-02", "cat-g-04", "cat-g-09", "cat-g-10"], ["security", "finance", "osint", "passport"], "ENABLE_SECURITY", "continuous", "Isolates intruders inside Cowrie decoys, exports police PDF reports, and enforces explicit-consent VideoKYC."),
        ("passport_agent", "Passport OMNIVIDENS Agent", "Sovereign Seal QR, WBRG & Lien Notarization", "gemini-4-plus-400b", ["qwen3.8-27b-2.19m", "qwen3.8-vision-28b"], ["cat-l-25", "cat-l-26", "cat-l-27"], ["passport", "legal", "finance", "news"], "ENABLE_SECURITY", "on-demand", "Issues OMNIVIDENS cryptographic QR credentials and anchors artifacts to OpenTimestamps + IPFS Kubo."),
        ("engineering_agent", "Engineering GHIDRA Agent", "GHIDRA P-Code SRE, FreeCAD Torque & Propulsion FEM", "qwen3-coder-next-80b", ["gemini-4-argon-400b", "deepseek-v4-flash"], ["cat-h-01", "cat-h-04", "cat-h-05", "cat-h-14", "cat-h-43"], ["engineering", "city", "templates"], "ENABLE_ENGINEERING", "on-demand", "Runs headless GHIDRA binary analysis, generates ISO 4762 M3/M4 screw enclosures, and solves propulsion FEM."),
        ("vocal_tuning_agent", "Vocal Tuning Agent", "Pitch Correction, Stem Separation & 94-808 Suite", "qwen3.8-27b-2.19m", ["gemma-4-e2b-5b", "deepseek-v4-flash"], ["cat-i-01", "cat-i-02", "cat-i-03", "cat-i-07", "cat-i-14"], ["music", "video"], "ENABLE_VOCAL_TUNING", "on-demand", "Chains Demucs/Spleeter stems with GSnap, MAutoPitch, Graillon 2, RVC v2, and the 94-sample Free 808 Kit."),
    ]
    out: List[AgentRecord] = []
    for aid, name, role, prim, backups, tools, tabs, flag, cad, desc in defs:
        en = _flag_enabled(flag)
        out.append(
            AgentRecord(
                id=aid,
                name=name,
                role=role,
                group="sovereign_12",
                primary_llm=prim,
                backup_llms=backups,
                tools=tools,
                tabs=tabs,
                turn_off_flag=flag,
                enabled=en,
                status="online" if en else "disabled",
                cadence=cad,
                description=desc,
            )
        )
    return out


def list_all_agents(tab: Optional[str] = None) -> List[AgentRecord]:
    all_items = [*list_sovereign_12(), *list_hermes_agent_records(), *list(CUSTOM_AGENTS.values())]
    if tab and tab not in {"agents", "home"}:
        filtered = [a for a in all_items if tab in a.tabs or a.group == "hermes_swarm"]
        if filtered:
            return filtered
    return all_items


async def run_agent_task(req: AgentRunRequest) -> AgentRunResponse:
    catalog = {a.id: a for a in list_all_agents()}
    agent = catalog.get(req.agent_id) or list_sovereign_12()[0]
    if not agent.enabled:
        return AgentRunResponse(
            agent_id=agent.id,
            agent_name=agent.name,
            sandbox_id="none",
            model_used=agent.primary_llm,
            status="disabled",
            output=f"Agent '{agent.name}' is currently turned off via {agent.turn_off_flag}=false.",
            finished_path="none",
            timestamp=utc_now(),
        )

    decision = route_model(
        RouterDecisionRequest(tab=req.tab, prompt=req.objective, preferred_model_id=agent.primary_llm)
    )
    task = POSTGRES_STORE.create_task(
        TaskCreateRequest(
            title=f"[{agent.name}] {req.objective[:70]}",
            prompt=req.objective,
            tab=req.tab,
            task_type="agent_execution",
            state="running",
            assigned_agent=agent.id,
        ),
        model_used=decision.selected_model.id,
        tools_used=agent.tools,
    )
    equip = equip_task_sandbox(task.sandbox_id, req.tab, task.id, force_equip=req.equip_sandbox)
    output = await complete_with_failover(req.tab, req.objective, decision, agent_id=agent.id)
    done_task = POSTGRES_STORE.update_state(task.id, "completed", output[:500]) or task
    archive_finished_sandbox(done_task, equip, output)
    return AgentRunResponse(
        agent_id=agent.id,
        agent_name=agent.name,
        sandbox_id=done_task.sandbox_id,
        model_used=decision.selected_model.id,
        status="completed",
        output=output,
        finished_path=done_task.finished_uri,
        timestamp=utc_now(),
    )
