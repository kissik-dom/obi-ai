"""Hermes-Library: Reusable Sovereign Prompt & Workflow Templates."""

from __future__ import annotations

from typing import Dict

HERMES_TEMPLATES: Dict[str, str] = {
    "single_batch_directive": (
        "Deliver all outputs in one unified batch archive with zero fragmentation, "
        "preserving SHA-256 hashes, OpenTimestamps proofs, and IPFS Kubo CIDs."
    ),
    "biometric_isolation": (
        "Lock Face1 bone structure, skin tone, pores, and freckles; apply requested isolation mask "
        "(Hair Only, Jewelry Only, Clothes Only, Background Only) via SAM2 + DINOv2 pose-only vectors."
    ),
    "ghidra_freecad_audit": (
        "Decompile binary functions via GHIDRA P-code CFG and verify mechanical enclosure tolerances "
        "with ISO 4762 M3x10mm 1.2 N-m screw bosses."
    ),
}


def get_hermes_template(key: str) -> str:
    return HERMES_TEMPLATES.get(key, HERMES_TEMPLATES["single_batch_directive"])
