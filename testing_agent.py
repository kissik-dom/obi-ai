#!/usr/bin/env python3
"""Kingdom AI OS testing agent.

Runs every TEST_INTERVAL=1200 seconds against the 24-tab grammar and
infrastructure healthchecks. The agent is safe for a clean checkout: file and
config checks always run, live network checks run only when KINGDOM_TEST_LIVE=1.
"""
from __future__ import annotations

import json
import os
import socket
import sys
import time
from pathlib import Path

TEST_INTERVAL = 1200
REPO_ROOT = Path(__file__).resolve().parent

LIVE_CHECKS = [
    ("qdrant", "qdr.ant", 6333),
    ("minio", "min.io", 9000),
    ("vault", "va.ult", 8200),
    ("postgres", "post.gres", 5432),
    ("redis", "re.dis", 6379),
    ("gpu-worker", "gpu.worker", 200),
    ("cua-1", "cua.one", 2000),
    ("cua-2", "cua.two", 2001),
    ("cua-3", "cua.three", 2002),
    ("cua-4", "cua.four", 2003),
    ("cua-5", "cua.five", 2004),
    ("honeypot", "honey.pot", 2222),
]

TABS = [
    "home", "llm", "research", "legal", "osint", "finance", "investments",
    "real_estate", "business", "leads", "urban_planning", "engineering_ghidra",
    "coding", "web_scraping", "news", "social_marketing", "fashion",
    "images_visual", "video_ugc", "music_audio", "agents_comms", "tasks",
    "open_source", "security_admin",
]

GRAMMAR = [
    "Chat", "Agents", "Open Tasks", "Completed Tasks", "Training",
    "Knowledge", "Files", "Tools", "Outputs", "Settings",
]


def check_files() -> dict[str, object]:
    failures: list[str] = []
    docs = (REPO_ROOT / "docs")
    expected_docs = [
        "ARCHITECTURE.md", "LLM_REGISTRY.md", "TOOL_REGISTRY.md", "TAB_SPEC.md",
        "SANDBOX_SPEC.md", "SECURITY_SPEC.md", "AGENT_SWARM_SPEC.md",
        "STACK_DECISION.md", "TESTING_SPEC.md", "GITHUB_SPEC.md",
    ]
    for doc in expected_docs:
        if not (docs / doc).exists():
            failures.append(f"missing docs/{doc}")

    routers = REPO_ROOT / "backend" / "api" / "routers"
    for tab in TABS:
        if not (routers / f"{tab}.py").exists():
            failures.append(f"missing backend router {tab}")

    agents_dir = REPO_ROOT / "backend" / "agents"
    for agent in ["bugfix", "testing", "external_scout", "internal_optimizer", "cua_fleet", "gpu_worker", "video_stitching", "image_consistency", "security_honeypot", "passport_omnividens", "engineering_ghidra", "vocal_tuning"]:
        if not (agents_dir / f"{agent}.py").exists():
            failures.append(f"missing agent {agent}")

    return {"ok": not failures, "failures": failures}


def check_litellm() -> dict[str, object]:
    config = (REPO_ROOT / "backend" / "litellm_proxy_config.yaml").read_text(encoding="utf-8")
    return {
        "model_count": config.count("  - model_name:"),
        "has_10_keys": all(f"OPENROUTER_API_KEY_{i}" in config for i in range(1, 11)),
        "has_retries": "num_retries: 3" in config,
        "has_timeout": "request_timeout: 60" in config,
        "has_fallbacks": "fallbacks:" in config,
    }


def check_live() -> dict[str, object]:
    if os.getenv("KINGDOM_TEST_LIVE") != "1":
        return {"skipped": True, "reason": "KINGDOM_TEST_LIVE is not 1"}
    results = {}
    for name, host, port in LIVE_CHECKS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1.5)
            results[name] = sock.connect_ex((host, port)) == 0
    return {"skipped": False, "results": results}


def run_once() -> int:
    files = check_files()
    litellm = check_litellm()
    live = check_live()
    report = {
        "schema": "kingdom.testing_agent.v1",
        "test_interval": TEST_INTERVAL,
        "files": files,
        "litellm": litellm,
        "live": live,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if files["ok"] else 1


def main() -> int:
    if os.getenv("RUN_ONCE") == "1":
        return run_once()
    while True:
        status = run_once()
        if status != 0:
            print("testing_agent: file check failed; retrying after interval", file=sys.stderr)
        time.sleep(TEST_INTERVAL)


if __name__ == "__main__":
    raise SystemExit(main())
