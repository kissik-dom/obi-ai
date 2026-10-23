"""Hermes-Agent Swarm Specialist Router (14 Domain Specialists, toggleable via ENABLE_HERMES)."""

from __future__ import annotations

from typing import Dict, List, Optional

from backend.core import config
from backend.core.schemas import AgentRecord

HERMES_SPECIALISTS: List[Dict[str, str]] = [
    {"id": "hermes_researcher", "name": "Hermes Researcher", "role": "1M-Context Deep Synthesis", "keywords": "research,citation,study,arxiv,website"},
    {"id": "hermes_coder", "name": "Hermes Coder", "role": "Strict TypeScript & FastAPI Architect", "keywords": "code,typescript,python,fastapi,react,bug"},
    {"id": "hermes_analyst", "name": "Hermes Quant Analyst", "role": "Quantitative Financial & Market Modeling", "keywords": "finance,quant,portfolio,roi,valuation"},
    {"id": "hermes_strategist", "name": "Hermes Strategist", "role": "Executive Multi-Tab Planning", "keywords": "strategy,roadmap,plan,business,crm"},
    {"id": "hermes_writer", "name": "Hermes Editorial Writer", "role": "Multilingual Gazette & Copywriting", "keywords": "news,magazine,article,copy,translate"},
    {"id": "hermes_critic", "name": "Hermes Adversarial Critic", "role": "Red-Team & Contract Verification", "keywords": "audit,verify,review,risk,critique"},
    {"id": "hermes_architect", "name": "Hermes Systems Architect", "role": "Zero-Trust Cloud & Sandbox Topology", "keywords": "docker,vultr,wireguard,ebpf,sandbox"},
    {"id": "hermes_legal", "name": "Hermes Legal Counsel", "role": "DocAssemble, FSIA & Lien Notarization", "keywords": "legal,contract,lien,gazette,compliance"},
    {"id": "hermes_security", "name": "Hermes Cyber Sentinel", "role": "CrowdSec, Wazuh, Falco & Honeypot Ops", "keywords": "security,osint,honeypot,waf,siem"},
    {"id": "hermes_vision_director", "name": "Hermes Vision Director", "role": "Photoreal Biometric Isolation & Angles", "keywords": "image,photo,hair,jewelry,fashion,skin"},
    {"id": "hermes_cinema_producer", "name": "Hermes Cinema Producer", "role": "600-Clip Continuity & Dialogue Timing", "keywords": "video,movie,ugc,clip,hailuo,stitch"},
    {"id": "hermes_cad_engineer", "name": "Hermes CAD/SRE Engineer", "role": "GHIDRA P-Code, FreeCAD & Propulsion FEM", "keywords": "ghidra,freecad,screw,cad,propulsion,kicad"},
    {"id": "hermes_audio_producer", "name": "Hermes Audio Producer", "role": "Vocal Pitch Tuning & 94-808 Mastering", "keywords": "vocal,audio,music,808,stem,pitch"},
    {"id": "hermes_synthesizer", "name": "Hermes Batch Synthesizer", "role": "Single-Batch Deliverable Aggregator", "keywords": "batch,summary,zip,pdf,deliver"},
]


def list_hermes_agent_records() -> List[AgentRecord]:
    enabled = config.FLAGS.ENABLE_HERMES
    return [
        AgentRecord(
            id=sp["id"],
            name=sp["name"],
            role=sp["role"],
            group="hermes_swarm",
            primary_llm="obliteratus-hermes-3-70b",
            backup_llms=["qwen3.8-27b-2.19m", "llama-4-scout-10m"],
            tools=["cat-l-19", "cat-l-20", "cat-l-21"],
            tabs=["agents", "home"],
            turn_off_flag="ENABLE_HERMES",
            enabled=enabled,
            status="online" if enabled else "disabled",
            cadence="swarm-reactive",
            description=f"Hermes Swarm specialist ({sp['role']}) matching [{sp['keywords']}].",
        )
        for sp in HERMES_SPECIALISTS
    ]


def select_hermes_specialist(prompt: str) -> Optional[str]:
    """Select the highest-affinity Hermes specialist unless ENABLE_HERMES=false."""
    if not config.FLAGS.ENABLE_HERMES:
        return None
    lower = prompt.lower()
    best_id = "hermes_synthesizer"
    best_hits = 0
    for sp in HERMES_SPECIALISTS:
        hits = sum(1 for kw in sp["keywords"].split(",") if kw in lower)
        if hits > best_hits:
            best_hits = hits
            best_id = sp["id"]
    return best_id
