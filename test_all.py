#!/usr/bin/env python3
"""Full Kingdom AI OS test suite.

Runs without Docker or third-party packages on a clean checkout. Live network
probes are opt-in with KINGDOM_TEST_LIVE=1.
"""
from __future__ import annotations

import os
import socket
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

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


class DocumentationTests(unittest.TestCase):
    def test_planning_documents_exist(self) -> None:
        expected = [
            "ARCHITECTURE.md", "LLM_REGISTRY.md", "TOOL_REGISTRY.md", "TAB_SPEC.md",
            "SANDBOX_SPEC.md", "SECURITY_SPEC.md", "AGENT_SWARM_SPEC.md",
            "STACK_DECISION.md", "TESTING_SPEC.md", "GITHUB_SPEC.md",
        ]
        for doc in expected:
            with self.subTest(doc=doc):
                self.assertTrue((REPO_ROOT / "docs" / doc).exists(), doc)

    def test_llm_registry_has_200_models(self) -> None:
        text = (REPO_ROOT / "docs" / "LLM_REGISTRY.md").read_text(encoding="utf-8")
        self.assertIn("ModelRecord table (240 entries)", text)
        self.assertIn("Gemini 4 Plus", text)
        self.assertIn("MiniMax Hailuo-02", text)
        self.assertIn("num_retries: 3", text)
        self.assertIn("request_timeout: 60", text)

    def test_tool_registry_has_600_tools(self) -> None:
        text = (REPO_ROOT / "docs" / "TOOL_REGISTRY.md").read_text(encoding="utf-8")
        tool_rows = text.count("| `tool-")
        self.assertGreaterEqual(tool_rows, 600, "less than 600 ToolRecord rows")


class BackendTests(unittest.TestCase):
    def test_24_routers_and_grammar(self) -> None:
        routers = REPO_ROOT / "backend" / "api" / "routers"
        for tab in TABS:
            with self.subTest(tab=tab):
                content = (routers / f"{tab}.py").read_text(encoding="utf-8")
                self.assertIn("make_tab_router", content)

        grammar_src = (routers / "__init__.py").read_text(encoding="utf-8")
        for section in GRAMMAR:
            self.assertIn(section, grammar_src)

    def test_12_agents(self) -> None:
        agents = [
            "bugfix.py", "testing.py", "external_scout.py", "internal_optimizer.py",
            "cua_fleet.py", "gpu_worker.py", "video_stitching.py", "image_consistency.py",
            "security_honeypot.py", "passport_omnividens.py", "engineering_ghidra.py",
            "vocal_tuning.py",
        ]
        for agent in agents:
            self.assertTrue((REPO_ROOT / "backend" / "agents" / agent).exists(), agent)

    def test_litellm_config(self) -> None:
        config = (REPO_ROOT / "backend" / "litellm_proxy_config.yaml").read_text(encoding="utf-8")
        self.assertGreaterEqual(config.count("  - model_name:"), 200)
        self.assertIn("num_retries: 3", config)
        self.assertIn("request_timeout: 60", config)
        self.assertIn("fallbacks:", config)
        self.assertTrue(all(f"OPENROUTER_API_KEY_{i}" in config for i in range(1, 11)))

    def test_finished_atomic_write(self) -> None:
        from backend.finished import write_finished_artifact
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["FINISHED_FOLDER"] = tmp
            target = write_finished_artifact("home", "task-1", {"ok": True}, "idem-1")
            self.assertTrue(target.exists())
            self.assertIn("kingdom.finished.v1", target.read_text(encoding="utf-8"))

    def test_request_folder_duplicate_key(self) -> None:
        from backend.requests import create_request_folder
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["REQUESTS_FOLDER"] = tmp
            first = create_request_folder("home", "idem-9")
            second = create_request_folder("home", "idem-9")
            self.assertEqual(first, second)


class FrontendTests(unittest.TestCase):
    def test_24_tab_components(self) -> None:
        names = [
            "HomeCommandCenter", "LlmModels", "Research", "Legal", "Osint", "Finance",
            "Investments", "RealEstate", "BusinessCrm", "Leads", "CityUrbanPlanning",
            "EngineeringGhidraAntiGravity", "CodingDev", "WebScraping", "NewsMagazines",
            "SocialMarketing", "Fashion", "ImagesVisualAi", "VideoUgcTvMovies",
            "MusicAudioVocalTuning", "AgentsCommunications", "Tasks", "OpenSourceApps",
            "SecurityAdmin",
        ]
        for name in names:
            with self.subTest(name=name):
                content = (REPO_ROOT / "frontend" / "src" / "tabs" / f"{name}.tsx").read_text(encoding="utf-8")
                self.assertIn("GRAMMAR.map", content)
                self.assertIn("copy-button", content)

    def test_typescript_strict_and_no_any(self) -> None:
        tsconfig = (REPO_ROOT / "frontend" / "tsconfig.json").read_text(encoding="utf-8")
        self.assertIn('"strict": true', tsconfig)
        for path in (REPO_ROOT / "frontend" / "src").rglob("*.ts*"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(": any", text)
            self.assertNotIn("<any>", text)

    def test_required_visual_system(self) -> None:
        css = (REPO_ROOT / "frontend" / "src" / "styles.css").read_text(encoding="utf-8")
        for token in ["#ffffff", "#000000", "--kingdom-magenta", "--kingdom-turquoise", "--kingdom-orange", "--kingdom-gold", "font-size: 11px"]:
            self.assertIn(token, css)


class InfrastructureTests(unittest.TestCase):
    def test_compose_healthchecks_and_services(self) -> None:
        compose = (REPO_ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        required = ["frontend", "backend", "qdrant", "minio", "vault", "postgres", "redis", "cua-fleet", "gpu-workers", "crowdsec", "wazuh", "suricata", "falco", "tetragon", "cowrie", "compreface", "wireguard"]
        self.assertTrue(all(service in compose for service in required))
        self.assertIn("healthcheck:", compose)
        self.assertIn("2000-2004:2000", compose)
        self.assertIn("200-204:200", compose)

    def test_testing_agent_interval(self) -> None:
        content = (REPO_ROOT / "testing_agent.py").read_text(encoding="utf-8")
        self.assertIn("TEST_INTERVAL = 1200", content)


@unittest.skipUnless(os.getenv("KINGDOM_TEST_LIVE") == "1", "live probes opt-in")
class LiveInfrastructureTests(unittest.TestCase):
    def _open(self, host: str, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1.5)
            return sock.connect_ex((host, port)) == 0

    def test_core_services(self) -> None:
        probes = {
            "qdrant": ("qdrant", 6333),
            "minio": ("minio", 9000),
            "vault": ("vault", 8200),
            "postgres": ("postgres", 5432),
            "redis": ("redis", 6379),
        }
        for name, (host, port) in probes.items():
            with self.subTest(name=name):
                self.assertTrue(self._open(host, port), name)

    def test_cua_isolation_ports(self) -> None:
        for port in range(2000, 2005):
            with self.subTest(port=port):
                self.assertTrue(self._open("cua", port), port)

    def test_gpu_worker(self) -> None:
        self.assertTrue(self._open("gpu", 200))


if __name__ == "__main__":
    unittest.main(verbosity=2)
