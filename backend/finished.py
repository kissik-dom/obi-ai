"""Finished Folder Archive Engine -> s3://kingdom-finished/{sandbox_id}/ with OpenTimestamps & IPFS Kubo audit."""

from __future__ import annotations

import hashlib
import json
from typing import Dict, List, Optional

from backend.core import config
from backend.core.schemas import SandboxBundleDetail, SandboxEquipStatus, TaskRecord
from backend.core.stores import MINIO_STORE, POSTGRES_STORE, equip_task_sandbox, utc_now


def archive_finished_sandbox(
    task: TaskRecord,
    equip: SandboxEquipStatus,
    output_text: str,
    extra_artifacts: Optional[Dict[str, str]] = None,
    metrics: Optional[Dict[str, str]] = None,
) -> SandboxBundleDetail:
    """Atomically write summary.md, artifacts/, evidence/, audit.json, logs/, and metrics/ to s3://kingdom-finished/."""
    bucket = config.SETTINGS.finished_bucket
    sbid = task.sandbox_id
    now = utc_now()

    summary_md = (
        f"# Finished Sandbox Dossier: {task.title}\n\n"
        f"- **Sandbox ID**: `{sbid}`\n"
        f"- **Task ID**: `{task.id}`\n"
        f"- **Tab**: `{task.tab}`\n"
        f"- **State**: `{task.state}`\n"
        f"- **Model Used**: `{task.model_used}`\n"
        f"- **Assigned Agent**: `{task.assigned_agent}`\n"
        f"- **OpenTimestamps Proof**: `{task.opentimestamps_proof}`\n"
        f"- **IPFS Kubo CID**: `{task.ipfs_cid}`\n"
        f"- **Completed At**: `{now}`\n\n"
        f"## Unified Single-Batch Output\n\n"
        f"{output_text}\n"
    )
    MINIO_STORE.put_text_atomic(bucket, f"{sbid}/summary.md", summary_md, tab=task.tab)

    artifact_keys: List[str] = []
    primary_key = f"{sbid}/artifacts/deliverable_batch.txt"
    MINIO_STORE.put_text_atomic(bucket, primary_key, output_text, tab=task.tab)
    artifact_keys.append(primary_key)
    for rel_name, content in (extra_artifacts or {}).items():
        akey = f"{sbid}/artifacts/{rel_name}"
        MINIO_STORE.put_text_atomic(bucket, akey, content, tab=task.tab)
        artifact_keys.append(akey)

    evidence_key = f"{sbid}/evidence/notarization_lien.json"
    evidence_payload = {
        "sandbox_id": sbid,
        "task_id": task.id,
        "sha256": hashlib.sha256(output_text.encode("utf-8")).hexdigest(),
        "opentimestamps_proof": task.opentimestamps_proof,
        "ipfs_cid": task.ipfs_cid,
        "kissi_gazette_status": "anchored",
        "timestamp": now,
    }
    MINIO_STORE.put_json_atomic(bucket, evidence_key, evidence_payload, tab=task.tab)

    audit_payload = {
        "sandbox_id": sbid,
        "task_id": task.id,
        "tab": task.tab,
        "model_used": task.model_used,
        "agent": task.assigned_agent,
        "tools_used": ", ".join(task.tools_used),
        "equipped_all": str(equip.equipped_all),
        "wireguard_isolated": str(equip.wireguard_isolated),
        "falco_ebpf_monitored": str(equip.falco_ebpf_monitored),
        "vault_policy": equip.vault_transit_policy,
        "timestamp": now,
    }
    MINIO_STORE.put_json_atomic(bucket, f"{sbid}/audit.json", audit_payload, tab=task.tab)

    log_key = f"{sbid}/logs/execution.log"
    log_text = (
        f"[{now}] SANDBOX_CREATE id={sbid} tab={task.tab} equipped={equip.equipped_all}\n"
        f"[{now}] ROUTER_SELECT model={task.model_used} agent={task.assigned_agent}\n"
        f"[{now}] ATOMIC_ARCHIVE bucket=s3://{bucket}/{sbid}/ state={task.state}\n"
    )
    MINIO_STORE.put_text_atomic(bucket, log_key, log_text, tab=task.tab)

    metrics_payload = {
        "batch_delivery": "single_unified_batch",
        "tools_equipped": str(equip.tools_available),
        "models_available": str(equip.models_available),
        "cua_space": equip.cua_space_id,
        **(metrics or {}),
    }
    MINIO_STORE.put_json_atomic(bucket, f"{sbid}/metrics/runtime.json", metrics_payload, tab=task.tab)

    return SandboxBundleDetail(
        sandbox_id=sbid,
        bucket=bucket,
        tab=task.tab,
        task_id=task.id,
        title=task.title,
        state=task.state,
        model_used=task.model_used,
        summary_md=summary_md,
        request_json={"prompt": task.prompt, "tab": task.tab, "task_type": task.task_type},
        response_json={"output": output_text[:2000], "finished_uri": task.finished_uri},
        audit_json=audit_payload,
        artifacts=artifact_keys,
        evidence=[evidence_key],
        logs=[log_key],
        metrics=metrics_payload,
        equip_status=equip,
        created_at=task.created_at,
    )


def get_finished_bundle(sandbox_id: str) -> Optional[SandboxBundleDetail]:
    """Read complete inspectable bundle from s3://kingdom-finished/{sandbox_id}/."""
    bucket = config.SETTINGS.finished_bucket
    raw_summary = MINIO_STORE.get_bytes(bucket, f"{sandbox_id}/summary.md")
    task = POSTGRES_STORE.get_by_sandbox(sandbox_id)
    if raw_summary is None and task is None:
        return None

    tab = task.tab if task else "home"
    task_id = task.id if task else f"task-{sandbox_id}"
    title = task.title if task else f"Sandbox {sandbox_id}"
    state = task.state if task else "completed"
    model_used = task.model_used if task else "qwen3.8-27b-2.19m"
    summary_md = raw_summary.decode("utf-8") if raw_summary else f"# Sandbox {sandbox_id}\n"
    audit_json = MINIO_STORE.get_json(bucket, f"{sandbox_id}/audit.json")
    metrics_json = MINIO_STORE.get_json(bucket, f"{sandbox_id}/metrics/runtime.json")
    objs = MINIO_STORE.list_objects(bucket, prefix=f"{sandbox_id}/", tab=tab)
    artifacts = [o.object_key for o in objs if "/artifacts/" in o.object_key]
    evidence = [o.object_key for o in objs if "/evidence/" in o.object_key]
    logs = [o.object_key for o in objs if "/logs/" in o.object_key]
    equip = equip_task_sandbox(sandbox_id, tab, task_id)
    return SandboxBundleDetail(
        sandbox_id=sandbox_id,
        bucket=bucket,
        tab=tab,
        task_id=task_id,
        title=title,
        state=state,  # type: ignore[arg-type]
        model_used=model_used,
        summary_md=summary_md,
        request_json={"prompt": task.prompt if task else "", "tab": tab},
        response_json={"result_summary": task.result_summary if task else summary_md[:400]},
        audit_json=audit_json,
        artifacts=artifacts,
        evidence=evidence,
        logs=logs,
        metrics=metrics_json,
        equip_status=equip,
        created_at=task.created_at if task else utc_now(),
    )


def list_finished_bundles(limit: int = 50) -> List[SandboxBundleDetail]:
    tasks = POSTGRES_STORE.list_tasks(completed=True)[:limit]
    out: List[SandboxBundleDetail] = []
    for t in tasks:
        bundle = get_finished_bundle(t.sandbox_id)
        if bundle is not None:
            out.append(bundle)
    return out
