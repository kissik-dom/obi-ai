"""Verify 205+ LLM Registry, OBLITERATED Tier S priority, ranking formula, hard filters, and 10-key proxy config."""

from pathlib import Path

from backend.core.llm_registry import list_models, route_model
from backend.core.schemas import RouterDecisionRequest


def test_registry_has_over_200_models_and_tier_s_first() -> None:
    models = list_models()
    assert len(models) >= 205
    assert models[0].tier == "S"
    assert models[0].guardrail == "OBLITERATED"


def test_domain_specialized_routing() -> None:
    img = route_model(RouterDecisionRequest(tab="images", prompt="photoreal skin biometric hair only"))
    assert img.selected_model.id == "gemma-4-it-qat-12b"

    vid = route_model(RouterDecisionRequest(tab="video", prompt="600 clips ugc video"))
    assert vid.selected_model.id == "minimax-hailuo-02"

    res = route_model(RouterDecisionRequest(tab="research", prompt="whole website deep research"))
    assert res.selected_model.id == "ling-3.1-flash-1m"

    osint = route_model(RouterDecisionRequest(tab="osint", prompt="spiderfoot osint recon"))
    assert osint.selected_model.id == "cyberstrike-offsec-35b"

    legal = route_model(RouterDecisionRequest(tab="legal", prompt="fsia contract review"))
    assert legal.selected_model.id == "qwen3.8-27b-2.19m"

    eng = route_model(RouterDecisionRequest(tab="engineering", prompt="ghidra freecad anti-gravity"))
    assert eng.selected_model.id == "qwen3-coder-next-80b"


def test_hard_filters_context_and_vram() -> None:
    huge_ctx = route_model(RouterDecisionRequest(tab="legal", required_context_tokens=2_000_000))
    assert huge_ctx.selected_model.contextTokens >= 2_000_000

    low_vram = route_model(RouterDecisionRequest(tab="social", local_only=True, available_vram_gb=8))
    assert low_vram.selected_model.vramGb <= 8
    assert low_vram.selected_model.local is True


def test_litellm_proxy_config_has_10_keys_and_retries() -> None:
    cfg = Path("backend/litellm_proxy_config.yaml").read_text(encoding="utf-8")
    for idx in range(1, 11):
        assert f"OPENROUTER_API_KEY_{idx}" in cfg
    assert "num_retries: 3" in cfg
    assert "timeout: 60" in cfg
