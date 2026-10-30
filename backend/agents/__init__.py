"""Kingdom AI OS agent fleet."""
from __future__ import annotations

from backend.agents.bugfix import BugFixAgent
from backend.agents.testing import TestingAgent
from backend.agents.external_scout import ExternalScoutAgent
from backend.agents.internal_optimizer import InternalOptimizerAgent
from backend.agents.cua_fleet import CuaFleetAgent
from backend.agents.gpu_worker import GpuWorkerAgent
from backend.agents.video_stitching import VideoStitchingAgent
from backend.agents.image_consistency import ImageConsistencyAgent
from backend.agents.security_honeypot import SecurityHoneypotAgent
from backend.agents.passport_omnividens import PassportOmnividensAgent
from backend.agents.engineering_ghidra import EngineeringGhidraAgent
from backend.agents.vocal_tuning import VocalTuningAgent

AGENTS = [
    BugFixAgent,
    TestingAgent,
    ExternalScoutAgent,
    InternalOptimizerAgent,
    CuaFleetAgent,
    GpuWorkerAgent,
    VideoStitchingAgent,
    ImageConsistencyAgent,
    SecurityHoneypotAgent,
    PassportOmnividensAgent,
    EngineeringGhidraAgent,
    VocalTuningAgent,
]

AGENT_BY_NAME = {agent.name: agent for agent in (cls() for cls in AGENTS)}

__all__ = ["AGENTS", "AGENT_BY_NAME"]
