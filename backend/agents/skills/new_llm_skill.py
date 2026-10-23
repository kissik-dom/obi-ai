"""Skill: Register a new LLM ModelRecord into the 205+ Sovereign Registry."""

from __future__ import annotations

import hashlib

from backend.core.llm_registry import register_model
from backend.core.schemas import GuardrailLevel, MaturityLevel, ModelRecord, ModelTier


def execute_new_llm_skill(
    model_id: str,
    canonical_name: str,
    specialty: str,
    tier: ModelTier = "X",
    guardrail: GuardrailLevel = "OBLITERATED",
    maturity: MaturityLevel = "quarantine",
    context_tokens: int = 131072,
    vram_gb: int = 24,
) -> ModelRecord:
    rec = ModelRecord(
        id=model_id,
        canonicalName=canonical_name,
        provider="openrouter/huihui-ai",
        repo=f"https://huggingface.co/huihui-ai/{model_id}",
        checksum=hashlib.sha256(model_id.encode("utf-8")).hexdigest()[:16],
        family=canonical_name.split("-")[0],
        tier=tier,
        tierCode=f"{tier}999",
        type="llm",
        modalities=["text", "tools"],
        parameters="32B",
        contextTokens=context_tokens,
        license="Apache-2.0",
        commercialUse=True,
        local=True,
        endpoints=[f"https://openrouter.ai/api/v1/{model_id}"],
        costPerMillionTokens=0.20,
        vramGb=vram_gb,
        guardrail=guardrail,
        maturity=maturity,
        priority=210,
        benchmarkScore=88.5,
        health="healthy",
        fallbacks=["qwen3.8-27b-2.19m", "deepseek-v4-flash"],
        specialty=specialty,
    )
    return register_model(rec)
