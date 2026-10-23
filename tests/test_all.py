"""End-to-end verification of all 24->28+ tabs, 10-endpoint grammar, sandboxes, and ENABLE_* turn-off flags."""

from fastapi.testclient import TestClient

from backend.main import app

GRAMMAR_PATHS = [
    "chat",
    "agents",
    "open-tasks",
    "completed-tasks",
    "training",
    "knowledge",
    "files",
    "tools",
    "outputs",
    "settings",
]


def test_healthz_and_metrics() -> None:
    with TestClient(app) as client:
        hz = client.get("/healthz")
        assert hz.status_code == 200
        body = hz.json()
        assert body["status"] in {"healthy", "degraded", "offline"}
        assert body["tabs_registered"] >= 28
        assert body["models_registered"] >= 205
        assert body["open_source_tools"] >= 620
        assert body["total_tools"] >= 920

        mt = client.get("/metrics")
        assert mt.status_code == 200
        assert "kingdom_models_total" in mt.text


def test_all_28_tabs_expose_identical_10_section_grammar() -> None:
    with TestClient(app) as client:
        tabs_res = client.get("/api/tabs?include_extended=true")
        assert tabs_res.status_code == 200
        tabs = tabs_res.json()
        assert len(tabs) >= 28
        core_tabs = [t for t in tabs if t["core"]]
        assert len(core_tabs) == 24

        for tab in tabs[:28]:
            slug = tab["slug"]
            for section in GRAMMAR_PATHS:
                res = client.get(f"/api/tabs/{slug}/{section}")
                assert res.status_code == 200, f"Failed GET /api/tabs/{slug}/{section}: {res.text}"


def test_quick_request_and_finished_folder_lifecycle() -> None:
    with TestClient(app) as client:
        qr = client.post("/api/requests", json={"prompt": "Synthesize sovereign parcel brief", "tab": "real_estate"})
        assert qr.status_code == 200
        bundle = qr.json()
        sbid = bundle["sandbox_id"]
        assert bundle["request_json"]["lifecycle"] == "queued -> running -> completed"
        assert bundle["equip_status"]["equipped_all"] is True

        req_get = client.get(f"/api/requests/{sbid}")
        assert req_get.status_code == 200
        fin_get = client.get(f"/api/finished/{sbid}")
        assert fin_get.status_code == 200
        assert "OpenTimestamps Proof" in fin_get.json()["summary_md"]


def test_dynamic_add_tab_and_turn_off_flags_without_crash() -> None:
    with TestClient(app) as client:
        add_res = client.post(
            "/api/tabs/add",
            json={
                "slug": "quantum_foundry",
                "title": "Quantum Foundry",
                "purpose": "Cryogenic QPU control and pulse calibration.",
                "best_llm": "qwen3-coder-next-80b",
                "tool_categories": ["H", "L"],
                "accent": "magenta",
            },
        )
        assert add_res.status_code == 200
        assert client.get("/api/tabs/quantum_foundry/chat").status_code == 200

        # Toggle ENABLE_HERMES and ENABLE_SANDBOX_EQUIP_ALL off cleanly, verify chat still works, then restore
        off = client.put("/api/flags", json={"flags": {"ENABLE_HERMES": False, "ENABLE_SANDBOX_EQUIP_ALL": False}})
        assert off.status_code == 200
        chat = client.post("/api/tabs/home/chat", json={"message": "Status check with Hermes disabled"})
        assert chat.status_code == 200
        assert chat.json()["hermes_specialist"] is None

        client.put("/api/flags", json={"flags": {"ENABLE_HERMES": True, "ENABLE_SANDBOX_EQUIP_ALL": True}})

    # Clean up dynamically generated test router artifact so git worktree stays clean
    from pathlib import Path
    from backend.core.tab_registry import CUSTOM_TABS_FILE, TAB_REGISTRY

    qf_router = Path("backend/api/routers/quantum_foundry.py")
    if qf_router.exists():
        qf_router.unlink()
    TAB_REGISTRY.pop("quantum_foundry", None)
    if CUSTOM_TABS_FILE.exists():
        CUSTOM_TABS_FILE.unlink()
