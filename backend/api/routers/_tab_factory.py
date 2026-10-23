"""Shared 10-Section Tab Grammar Router Factory (ensures 100% identical structure across Tabs 1->28+)."""

from __future__ import annotations

import asyncio
from typing import List

from fastapi import APIRouter, HTTPException

from backend.agents.registry import list_all_agents, run_agent_task
from backend.agents.skills.hermes.hermes_agent import select_hermes_specialist
from backend.core import config
from backend.core.convex_adapter import emit_convex_event
from backend.core.llm_registry import complete_with_failover, route_model
from backend.core.schemas import (
    AgentRecord,
    AgentRunRequest,
    AgentRunResponse,
    ChatMessageRecord,
    ChatTurnRequest,
    ChatTurnResponse,
    FileCreateRequest,
    FileRecord,
    KnowledgeQueryRequest,
    KnowledgeQueryResponse,
    OutputDeliverableRecord,
    RouterDecisionRequest,
    TabSettingsModel,
    TabSettingsUpdateRequest,
    TaskCreateRequest,
    TaskRecord,
    TaskStateUpdateRequest,
    ToolExecuteRequest,
    ToolExecuteResponse,
    ToolRecord,
    TrainingDocumentRecord,
    TrainingIngestRequest,
)
from backend.core.stores import (
    MINIO_STORE,
    POSTGRES_STORE,
    QDRANT_STORE,
    equip_task_sandbox,
    list_tab_outputs,
)
from backend.core.tab_registry import get_tab
from backend.core.tool_registry import lazy_execute_tool, list_tools
from backend.finished import archive_finished_sandbox


def build_tab_router(tab_slug: str) -> APIRouter:
    """Create a FastAPI APIRouter implementing all 10 standardized grammar sections for `tab_slug`."""
    router = APIRouter(prefix=f"/api/tabs/{tab_slug}", tags=[f"tab:{tab_slug}"])

    # 1. CHAT (GET history + async POST completion in equipped sandbox)
    @router.get("/chat", response_model=List[ChatMessageRecord])
    async def get_chat_history() -> List[ChatMessageRecord]:
        return POSTGRES_STORE.list_chat_messages(tab=tab_slug)

    @router.post("/chat", response_model=ChatTurnResponse)
    async def post_chat_turn(payload: ChatTurnRequest) -> ChatTurnResponse:
        spec = get_tab(tab_slug)
        if spec is None:
            raise HTTPException(status_code=404, detail=f"Unknown tab '{tab_slug}'")

        settings = POSTGRES_STORE.get_tab_settings(tab_slug)
        preferred = payload.preferred_model_id or None
        decision = route_model(
            RouterDecisionRequest(
                tab=tab_slug,
                prompt=payload.message,
                preferred_model_id=preferred,
            )
        )
        agent_id = payload.agent_id or (spec.agents[0] if spec.agents else "internal_optimizer_agent")
        hermes_spec = select_hermes_specialist(payload.message) if payload.use_hermes_swarm else None

        task = POSTGRES_STORE.create_task(
            TaskCreateRequest(
                title=f"[{spec.title}] {payload.message[:72]}",
                prompt=payload.message,
                tab=tab_slug,
                task_type=payload.isolation_mode or "chat_turn",
                state="running",
                assigned_agent=agent_id,
            ),
            model_used=decision.selected_model.id,
            tools_used=spec.top_tools[:5],
        )
        equip = equip_task_sandbox(
            task.sandbox_id,
            tab_slug,
            task.id,
            force_equip=settings.equip_sandbox_all,
        )
        user_msg = POSTGRES_STORE.save_chat_message(
            tab=tab_slug,
            role="user",
            content=payload.message,
            model_id=decision.selected_model.id,
            agent_id=agent_id,
            sandbox_id=task.sandbox_id,
        )
        reply_text = await complete_with_failover(
            tab=tab_slug,
            prompt=payload.message,
            decision=decision,
            agent_id=agent_id,
            hermes_specialist=hermes_spec,
        )
        assistant_msg = POSTGRES_STORE.save_chat_message(
            tab=tab_slug,
            role="assistant",
            content=reply_text,
            model_id=decision.selected_model.id,
            agent_id=agent_id,
            sandbox_id=task.sandbox_id,
        )
        done_task = POSTGRES_STORE.update_state(task.id, "completed", reply_text[:500]) or task
        archive_finished_sandbox(done_task, equip, reply_text)
        await emit_convex_event("chat_turn_completed", {"tab": tab_slug, "sandbox_id": done_task.sandbox_id})
        return ChatTurnResponse(
            tab=tab_slug,
            user_message=user_msg,
            assistant_message=assistant_msg,
            router_decision=decision,
            sandbox=equip,
            task=done_task,
            hermes_specialist=hermes_spec,
        )

    # 2. AGENTS
    @router.get("/agents", response_model=List[AgentRecord])
    async def get_tab_agents() -> List[AgentRecord]:
        return list_all_agents(tab=tab_slug)

    @router.post("/agents", response_model=AgentRunResponse)
    async def post_tab_agent_run(payload: AgentRunRequest) -> AgentRunResponse:
        req = AgentRunRequest(
            agent_id=payload.agent_id,
            tab=tab_slug,
            objective=payload.objective,
            equip_sandbox=payload.equip_sandbox,
        )
        return await run_agent_task(req)

    # 3. OPEN TASKS
    @router.get("/open-tasks", response_model=List[TaskRecord])
    async def get_open_tasks() -> List[TaskRecord]:
        return POSTGRES_STORE.list_tasks(tab=tab_slug, completed=False)

    @router.post("/open-tasks", response_model=TaskRecord)
    async def create_open_task(payload: TaskCreateRequest) -> TaskRecord:
        decision = route_model(
            RouterDecisionRequest(tab=tab_slug, prompt=payload.prompt or payload.title, preferred_model_id=payload.preferred_model)
        )
        req = payload.model_copy(update={"tab": tab_slug})
        task = POSTGRES_STORE.create_task(req, model_used=decision.selected_model.id)
        equip = equip_task_sandbox(task.sandbox_id, tab_slug, task.id)
        if payload.auto_complete and payload.state == "completed":
            archive_finished_sandbox(task, equip, task.result_summary)
        return task

    @router.patch("/open-tasks/{task_id}", response_model=TaskRecord)
    async def update_task_status(task_id: str, payload: TaskStateUpdateRequest) -> TaskRecord:
        updated = POSTGRES_STORE.update_state(task_id, payload.state, payload.result_summary)
        if updated is None:
            raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
        if updated.state == "completed":
            equip = equip_task_sandbox(updated.sandbox_id, updated.tab, updated.id)
            archive_finished_sandbox(updated, equip, updated.result_summary)
        return updated

    # 4. COMPLETED TASKS
    @router.get("/completed-tasks", response_model=List[TaskRecord])
    async def get_completed_tasks() -> List[TaskRecord]:
        return POSTGRES_STORE.list_tasks(tab=tab_slug, completed=True)

    # 5. TRAINING
    @router.get("/training", response_model=List[TrainingDocumentRecord])
    async def get_training_corpus() -> List[TrainingDocumentRecord]:
        return QDRANT_STORE.list_documents(tab=tab_slug)

    @router.post("/training", response_model=TrainingDocumentRecord)
    async def post_training_document(payload: TrainingIngestRequest) -> TrainingDocumentRecord:
        loop = asyncio.get_running_loop()
        doc = await loop.run_in_executor(
            None,
            lambda: QDRANT_STORE.upsert_document(
                tab=tab_slug,
                title=payload.title,
                content=payload.content,
                source_uri=payload.source_uri,
            ),
        )
        MINIO_STORE.put_text_atomic(
            config.SETTINGS.finished_bucket,
            f"{tab_slug}/training/{doc.doc_id}.txt",
            payload.content,
            tab=tab_slug,
        )
        return doc

    # 6. KNOWLEDGE
    @router.get("/knowledge", response_model=KnowledgeQueryResponse)
    async def get_default_knowledge(q: str = "Kingdom AI OS") -> KnowledgeQueryResponse:
        hits = QDRANT_STORE.search(query=q, tab=tab_slug, limit=6)
        return KnowledgeQueryResponse(tab=tab_slug, query=q, hits=hits)

    @router.post("/knowledge", response_model=KnowledgeQueryResponse)
    async def query_knowledge(payload: KnowledgeQueryRequest) -> KnowledgeQueryResponse:
        hits = QDRANT_STORE.search(query=payload.query, tab=tab_slug, limit=payload.limit)
        return KnowledgeQueryResponse(tab=tab_slug, query=payload.query, hits=hits)

    # 7. FILES
    @router.get("/files", response_model=List[FileRecord])
    async def get_tab_files() -> List[FileRecord]:
        fin = MINIO_STORE.list_objects(config.SETTINGS.finished_bucket, prefix="", tab=tab_slug)
        filtered = [f for f in fin if f.object_key.startswith(f"{tab_slug}/") or len(fin) <= 25]
        return filtered[:50]

    @router.post("/files", response_model=FileRecord)
    async def upload_tab_file(payload: FileCreateRequest) -> FileRecord:
        bucket = (
            config.SETTINGS.requests_bucket
            if payload.bucket_kind == "requests"
            else config.SETTINGS.finished_bucket
        )
        safe_name = payload.filename.replace("..", "").lstrip("/")
        return MINIO_STORE.put_text_atomic(bucket, f"{tab_slug}/files/{safe_name}", payload.content, tab=tab_slug)

    # 8. TOOLS
    @router.get("/tools", response_model=List[ToolRecord])
    async def get_tab_tools() -> List[ToolRecord]:
        return list_tools(tab=tab_slug)[:120]

    @router.post("/tools", response_model=ToolExecuteResponse)
    async def execute_tab_tool(payload: ToolExecuteRequest) -> ToolExecuteResponse:
        loop = asyncio.get_running_loop()
        req = payload.model_copy(update={"tab": tab_slug})
        return await loop.run_in_executor(None, lambda: lazy_execute_tool(req))

    # 9. OUTPUTS
    @router.get("/outputs", response_model=List[OutputDeliverableRecord])
    async def get_tab_outputs() -> List[OutputDeliverableRecord]:
        return list_tab_outputs(tab=tab_slug)

    # 10. SETTINGS
    @router.get("/settings", response_model=TabSettingsModel)
    async def get_settings() -> TabSettingsModel:
        return POSTGRES_STORE.get_tab_settings(tab_slug)

    @router.put("/settings", response_model=TabSettingsModel)
    async def update_settings(payload: TabSettingsUpdateRequest) -> TabSettingsModel:
        if payload.flags:
            config.update_flags(payload.flags)
        return POSTGRES_STORE.save_tab_settings(
            tab=tab_slug,
            default_model_id=payload.default_model_id,
            guardrail_filter=payload.guardrail_filter,
            equip_sandbox_all=payload.equip_sandbox_all,
            hermes_enabled=payload.hermes_enabled,
            auto_notarize_ipfs=payload.auto_notarize_ipfs,
        )

    return router
