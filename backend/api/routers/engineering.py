"""Tab 12: Engineering GHIDRA Anti-Gravity Router (10-Section Grammar + GHIDRA / FreeCAD / Propulsion Endpoints)."""

from __future__ import annotations

import asyncio
from typing import Dict, List

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from backend.agents.engineering_agent import (
    analyze_binary_with_ghidra,
    generate_freecad_screw_enclosure,
    simulate_propulsion_physics,
)
from backend.api.routers._tab_factory import build_tab_router

router = build_tab_router("engineering")
domain_router = APIRouter(prefix="/api/engineering", tags=["domain:engineering"])


class GhidraAnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    binary_name: str = Field(default="flight_controller_fw.elf", min_length=1)
    hex_sample: str = Field(default="7f454c4602010100")


class GhidraAnalyzeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    binary_name: str
    sha256_prefix: str
    engine: str
    llm_sre_model: str
    escalation_model: str
    functions_recovered: List[Dict[str, str]]
    vulnerabilities_flagged: int
    decompiled_c_preview: str


class FreeCadScrewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    thread_spec: str = Field(default="M3x10mm ISO 4762")
    material: str = Field(default="Al 7075-T6")
    boss_count: int = Field(default=8, ge=1, le=64)


class FreeCadScrewResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    thread_spec: str
    standard: str
    material: str
    pitch_mm: float
    through_hole_clearance_mm: float
    counterbore_diameter_mm: float
    recommended_torque_nm: float
    boss_count: int
    bom_manager: str
    openscad_script: str
    stl_artifact: str
    step_artifact: str


class PropulsionSimRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: str = Field(default="mach_effect_piezo_resonator")
    drive_freq_khz: float = Field(default=36.4, gt=0.1)


class PropulsionSimResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: str
    solvers: List[str]
    drive_frequency_khz: float
    resonator_q_factor: float
    reactive_stored_energy_joules: float
    predicted_net_force_micro_newtons: float
    thermal_margin_kelvin: float
    kicad_hv_clearance_mm: float
    status: str


@domain_router.post("/ghidra/analyze", response_model=GhidraAnalyzeResponse)
async def post_ghidra_analyze(payload: GhidraAnalyzeRequest) -> GhidraAnalyzeResponse:
    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(
        None,
        lambda: analyze_binary_with_ghidra(payload.binary_name, payload.hex_sample),
    )
    return GhidraAnalyzeResponse(**res)  # type: ignore[arg-type]


@domain_router.post("/freecad/screw", response_model=FreeCadScrewResponse)
async def post_freecad_screw(payload: FreeCadScrewRequest) -> FreeCadScrewResponse:
    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(
        None,
        lambda: generate_freecad_screw_enclosure(payload.thread_spec, payload.material, payload.boss_count),
    )
    return FreeCadScrewResponse(**res)  # type: ignore[arg-type]


@domain_router.post("/anti-gravity", response_model=PropulsionSimResponse)
async def post_propulsion_sim(payload: PropulsionSimRequest) -> PropulsionSimResponse:
    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(
        None,
        lambda: simulate_propulsion_physics(payload.mode, payload.drive_freq_khz),
    )
    return PropulsionSimResponse(**res)  # type: ignore[arg-type]
