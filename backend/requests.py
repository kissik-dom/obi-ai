"""Requests Folder Engine -> s3://kingdom-requests/{sandbox_id}/ (Quick Request intake & queued->running->completed lifecycle)."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Guard: if invoked with cwd=backend/ such that `import requests` resolves here, re-export site-packages `requests` symbols
if __name__ == "requests":
    _this_dir = str(Path(__file__).resolve().parent)
    _search_paths = [p for p in sys.path if str(Path(p or ".").resolve()) != _this_dir]
    _spec = importlib.machinery.PathFinder.find_spec("requests", _search_paths)
    if _spec is not None and _spec.loader is not None:
        _real_requests = importlib.util.module_from_spec(_spec)
        sys.modules["requests"] = _real_requests
        _spec.loader.exec_module(_real_requests)

from backend.core import config  # noqa: E402
from backend.core.llm_registry import complete_with_failover, route_model  # noqa: E402
from backend.core.schemas import (  # noqa: E402
    QuickRequestCreate,
    RouterDecisionRequest,
    SandboxBundleDetail,
    TaskCreateRequest,
)
from backend.core.stores import MINIO_STORE, POSTGRES_STORE, equip_task_sandbox, utc_now  # noqa: E402
from backend.finished import archive_finished_sandbox  # noqa: E402


async def submit_quick_request(payload: QuickRequestCreate) -> SandboxBundleDetail:
    """Create isolated sandbox in s3://kingdom-requests/{sandbox_id}/, transition queued -> running -> completed, and mirror to finished."""
    decision = route_model(RouterDecisionRequest(tab=payload.tab, prompt=payload.prompt))
    # 1. State: queued
    task = POSTGRES_STORE.create_task(
        TaskCreateRequest(
            title=f"Quick Request ({payload.tab}): {payload.prompt[:72]}",
            prompt=payload.prompt,
            tab=payload.tab,
            task_type=payload.task_type,
            state="queued",
            assigned_agent="cua_fleet_agent" if payload.tab in {"web", "social", "leads"} else "internal_optimizer_agent",
        ),
        model_used=decision.selected_model.id,
        tools_used=["qdrant-768d", "minio-atomic", "vault-hsm", "litellm-10key"],
    )
    sbid = task.sandbox_id
    req_bucket = config.SETTINGS.requests_bucket
    equip = equip_task_sandbox(sbid, payload.tab, task.id)

    req_doc: Dict[str, str] = {
        "sandbox_id": sbid,
        "task_id": task.id,
        "tab": payload.tab,
        "task_type": payload.task_type,
        "prompt": payload.prompt,
        "isolation_mode": payload.isolation_mode or "standard",
        "lifecycle": "queued",
        "created_at": task.created_at,
    }
    MINIO_STORE.put_json_atomic(req_bucket, f"{sbid}/request.json", req_doc, tab=payload.tab)

    # 2. State: running
    POSTGRES_STORE.update_state(task.id, "running", f"Executing in equipped sandbox {sbid}")
    req_doc["lifecycle"] = "queued -> running"
    MINIO_STORE.put_json_atomic(req_bucket, f"{sbid}/request.json", req_doc, tab=payload.tab)

    synthesis = await complete_with_failover(
        tab=payload.tab,
        prompt=payload.prompt,
        decision=decision,
        agent_id=task.assigned_agent,
    )

    # 3. State: completed
    completed_task = POSTGRES_STORE.update_state(task.id, "completed", synthesis[:500]) or task
    req_doc["lifecycle"] = "queued -> running -> completed"
    MINIO_STORE.put_json_atomic(req_bucket, f"{sbid}/request.json", req_doc, tab=payload.tab)

    resp_doc: Dict[str, str] = {
        "sandbox_id": sbid,
        "task_id": completed_task.id,
        "model_used": decision.selected_model.id,
        "router_score": str(decision.score),
        "status": "completed",
        "output": synthesis,
        "completed_at": utc_now(),
    }
    MINIO_STORE.put_json_atomic(req_bucket, f"{sbid}/response.json", resp_doc, tab=payload.tab)
    MINIO_STORE.put_text_atomic(req_bucket, f"{sbid}/artifacts/quick_output.txt", synthesis, tab=payload.tab)
    MINIO_STORE.put_json_atomic(
        req_bucket,
        f"{sbid}/evidence/provenance.json",
        {"opentimestamps": completed_task.opentimestamps_proof, "ipfs_cid": completed_task.ipfs_cid},
        tab=payload.tab,
    )
    audit_doc: Dict[str, str] = {
        "sandbox_id": sbid,
        "equipped_all": str(equip.equipped_all),
        "cua_space_id": equip.cua_space_id,
        "vault_policy": equip.vault_transit_policy,
        "lifecycle": "queued -> running -> completed",
    }
    MINIO_STORE.put_json_atomic(req_bucket, f"{sbid}/audit.json", audit_doc, tab=payload.tab)

    # Mirror finished package into s3://kingdom-finished/{sandbox_id}/
    archive_finished_sandbox(completed_task, equip, synthesis)

    objs = MINIO_STORE.list_objects(req_bucket, prefix=f"{sbid}/", tab=payload.tab)
    return SandboxBundleDetail(
        sandbox_id=sbid,
        bucket=req_bucket,
        tab=payload.tab,
        task_id=completed_task.id,
        title=completed_task.title,
        state=completed_task.state,
        model_used=completed_task.model_used,
        summary_md=synthesis,
        request_json=req_doc,
        response_json=resp_doc,
        audit_json=audit_doc,
        artifacts=[o.object_key for o in objs if "/artifacts/" in o.object_key],
        evidence=[o.object_key for o in objs if "/evidence/" in o.object_key],
        logs=[],
        metrics={"lifecycle": "queued -> running -> completed"},
        equip_status=equip,
        created_at=completed_task.created_at,
    )


def get_request_bundle(sandbox_id: str) -> Optional[SandboxBundleDetail]:
    req_bucket = config.SETTINGS.requests_bucket
    req_doc = MINIO_STORE.get_json(req_bucket, f"{sandbox_id}/request.json")
    if not req_doc:
        return None
    resp_doc = MINIO_STORE.get_json(req_bucket, f"{sandbox_id}/response.json")
    audit_doc = MINIO_STORE.get_json(req_bucket, f"{sandbox_id}/audit.json")
    tab = req_doc.get("tab", "home")
    task_id = req_doc.get("task_id", f"task-{sandbox_id}")
    task = POSTGRES_STORE.get_by_sandbox(sandbox_id)
    objs = MINIO_STORE.list_objects(req_bucket, prefix=f"{sandbox_id}/", tab=tab)
    equip = equip_task_sandbox(sandbox_id, tab, task_id)
    return SandboxBundleDetail(
        sandbox_id=sandbox_id,
        bucket=req_bucket,
        tab=tab,
        task_id=task_id,
        title=task.title if task else f"Quick Request {sandbox_id}",
        state=task.state if task else "completed",
        model_used=resp_doc.get("model_used", "qwen3.8-27b-2.19m"),
        summary_md=resp_doc.get("output", ""),
        request_json=req_doc,
        response_json=resp_doc,
        audit_json=audit_doc,
        artifacts=[o.object_key for o in objs if "/artifacts/" in o.object_key],
        evidence=[o.object_key for o in objs if "/evidence/" in o.object_key],
        logs=[],
        metrics={"lifecycle": req_doc.get("lifecycle", "completed")},
        equip_status=equip,
        created_at=req_doc.get("created_at", utc_now()),
    )


def list_request_bundles(limit: int = 50) -> List[SandboxBundleDetail]:
    req_bucket = config.SETTINGS.requests_bucket
    objs = MINIO_STORE.list_objects(req_bucket)
    seen: List[str] = []
    for o in objs:
        if o.object_key.endswith("/request.json"):
            sbid = o.object_key.split("/")[0]
            if sbid not in seen:
                seen.append(sbid)
    out: List[SandboxBundleDetail] = []
    for sbid in reversed(seen[-limit:]):
        b = get_request_bundle(sbid)
        if b is not None:
            out.append(b)
    return out
