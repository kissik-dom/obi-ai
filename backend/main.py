"""Kingdom AI OS Sovereign FastAPI Application (24->28+ Tabs, 205+ LLMs, 920 Tools, 12 Sovereign Agents)."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, ConfigDict

from backend import finished as finished_service
from backend import requests as requests_service
from backend.agents.cua_fleet_agent import verify_cua_space_isolation
from backend.agents.external_scout_agent import run_external_scout_scan
from backend.agents.gpu_worker_agent import run_parallel_gpu_batch
from backend.agents.internal_optimizer_agent import run_internal_optimizer
from backend.agents.registry import list_all_agents, list_sovereign_12, run_agent_task
from backend.agents.skills.new_tab_skill import execute_new_tab_skill
from backend.api.routers import (
    agents as tab_agents,
    bugfix,
    business,
    city,
    coding,
    engineering,
    fashion,
    finance,
    home,
    images,
    investments,
    kyc,
    leads,
    legal,
    llm,
    marketplace,
    music,
    news,
    opensource,
    osint,
    passport,
    real_estate,
    research,
    security,
    social,
    tasks,
    templates,
    training,
    video,
    web,
)
from backend.api.routers._tab_factory import build_tab_router
from backend.core import config
from backend.core.llm_registry import MODEL_REGISTRY, list_models, route_model
from backend.core.schemas import (
    AgentRecord,
    AgentRunRequest,
    AgentRunResponse,
    GuardrailLevel,
    HealthzResponse,
    ModelRecord,
    NewTabSkillRequest,
    NewTabSkillResponse,
    QuickRequestCreate,
    RouterDecisionRequest,
    RouterDecisionResponse,
    SandboxBundleDetail,
    TabSpecRecord,
    ToolCategory,
    ToolExecuteRequest,
    ToolExecuteResponse,
    ToolRecord,
)
from backend.core.stores import (
    MINIO_STORE,
    QDRANT_STORE,
    REDIS_STORE,
    RELATIONAL_MODE,
    VAULT_STORE,
    seed_initial_knowledge_once,
    utc_now,
)
from backend.core.tab_registry import TAB_REGISTRY, list_tabs
from backend.core.tool_registry import TOOL_REGISTRY, count_open_source_tools, lazy_execute_tool, list_tools
from backend.security_middleware import SecurityMiddleware

MOUNTED_TAB_SLUGS: set[str] = set()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    seed_initial_knowledge_once()
    yield


app = FastAPI(
    title="Kingdom AI OS Sovereign Control Plane",
    version=config.SETTINGS.version,
    description=(
        "Sovereign multi-agent AI operating system: 24 core tabs extensible to 28+ tabs, "
        "205+ OBLITERATED & multimodal LLMs, 920 lazy-loaded tools, isolated sandboxes, and Zero-Trust security."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityMiddleware)

# Mount all 24 core + 4 extensible tab routers
STATIC_TAB_ROUTERS = [
    ("home", home.router),
    ("llm", llm.router),
    ("research", research.router),
    ("legal", legal.router),
    ("osint", osint.router),
    ("finance", finance.router),
    ("investments", investments.router),
    ("real_estate", real_estate.router),
    ("business", business.router),
    ("leads", leads.router),
    ("city", city.router),
    ("engineering", engineering.router),
    ("coding", coding.router),
    ("web", web.router),
    ("news", news.router),
    ("social", social.router),
    ("fashion", fashion.router),
    ("images", images.router),
    ("video", video.router),
    ("music", music.router),
    ("agents", tab_agents.router),
    ("tasks", tasks.router),
    ("opensource", opensource.router),
    ("security", security.router),
    ("templates", templates.router),
    ("passport", passport.router),
    ("training", training.router),
    ("marketplace", marketplace.router),
]

for slug, rtr in STATIC_TAB_ROUTERS:
    app.include_router(rtr)
    MOUNTED_TAB_SLUGS.add(slug)

# Mount any persisted custom tabs > 28
for dyn_slug in list(TAB_REGISTRY.keys()):
    if dyn_slug not in MOUNTED_TAB_SLUGS:
        app.include_router(build_tab_router(dyn_slug))
        MOUNTED_TAB_SLUGS.add(dyn_slug)

# Mount specialized domain routers
app.include_router(engineering.domain_router)
app.include_router(images.domain_router)
app.include_router(video.domain_router)
app.include_router(music.domain_router)
app.include_router(security.domain_router)
app.include_router(kyc.router)
app.include_router(kyc.passport_domain_router)
app.include_router(bugfix.router)


class FlagsUpdatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    flags: Dict[str, bool]


class FlagsStateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    flags: Dict[str, bool]


class GpuBatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    total_images: int = 1000
    workers: int = 200
    model_id: str = "gemma-4-it-qat-12b"


class GenericDictResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    status: str = "ok"


@app.get("/healthz", response_model=HealthzResponse, tags=["system"])
async def healthz() -> HealthzResponse:
    subsystems = {
        "postgres_sqlalchemy": RELATIONAL_MODE,
        "qdrant_768d_cosine": QDRANT_STORE.mode,
        "minio_atomic_s3": MINIO_STORE.mode,
        "vault_hsm_transit": VAULT_STORE.mode,
        "redis_queue": REDIS_STORE.mode,
        "litellm_10key_router": "healthy" if config.FLAGS.ENABLE_LLM_ROUTER else "degraded",
    }
    degraded = any(v == "offline" for v in subsystems.values())
    state = "degraded" if degraded else "healthy"
    return HealthzResponse(
        status=state,  # type: ignore[arg-type]
        version=config.SETTINGS.version,
        tabs_registered=len(TAB_REGISTRY),
        models_registered=len(MODEL_REGISTRY),
        open_source_tools=count_open_source_tools(),
        total_tools=len(TOOL_REGISTRY),
        agents_registered=len(list_sovereign_12()),
        subsystems=subsystems,
        flags=config.get_flags_dict(),
        timestamp=utc_now(),
    )


@app.get("/metrics", response_class=PlainTextResponse, tags=["system"])
async def metrics() -> PlainTextResponse:
    lines = [
        "# HELP kingdom_tabs_total Total active tabs in Kingdom AI OS",
        "# TYPE kingdom_tabs_total gauge",
        f"kingdom_tabs_total {len(TAB_REGISTRY)}",
        "# HELP kingdom_models_total Total registered LLMs and multimodal models",
        "# TYPE kingdom_models_total gauge",
        f"kingdom_models_total {len(MODEL_REGISTRY)}",
        "# HELP kingdom_open_source_tools_total Total open-source tools registered",
        "# TYPE kingdom_open_source_tools_total gauge",
        f"kingdom_open_source_tools_total {count_open_source_tools()}",
        "# HELP kingdom_ecosystem_tools_total Total open-source + Composio tools registered",
        "# TYPE kingdom_ecosystem_tools_total gauge",
        f"kingdom_ecosystem_tools_total {len(TOOL_REGISTRY)}",
        "# HELP kingdom_sovereign_agents_total Core Sovereign Agents active",
        "# TYPE kingdom_sovereign_agents_total gauge",
        f"kingdom_sovereign_agents_total {len(list_sovereign_12())}",
    ]
    return PlainTextResponse("\n".join(lines) + "\n")


@app.get("/api/tabs", response_model=List[TabSpecRecord], tags=["tabs"])
async def api_list_tabs(include_extended: bool = True) -> List[TabSpecRecord]:
    return list_tabs(include_extended=include_extended)


@app.post("/api/tabs/add", response_model=NewTabSkillResponse, tags=["tabs"])
async def api_add_tab(payload: NewTabSkillRequest) -> NewTabSkillResponse:
    result = execute_new_tab_skill(payload)
    if result.tab.slug not in MOUNTED_TAB_SLUGS:
        app.include_router(build_tab_router(result.tab.slug))
        MOUNTED_TAB_SLUGS.add(result.tab.slug)
    return result


@app.get("/api/flags", response_model=FlagsStateResponse, tags=["system"])
async def api_get_flags() -> FlagsStateResponse:
    return FlagsStateResponse(flags=config.get_flags_dict())


@app.put("/api/flags", response_model=FlagsStateResponse, tags=["system"])
async def api_put_flags(payload: FlagsUpdatePayload) -> FlagsStateResponse:
    config.update_flags(payload.flags)
    return FlagsStateResponse(flags=config.get_flags_dict())


@app.get("/api/llm/models", response_model=List[ModelRecord], tags=["llm"])
async def api_list_models(tier: Optional[str] = None, guardrail: Optional[GuardrailLevel] = None) -> List[ModelRecord]:
    return list_models(tier=tier, guardrail=guardrail)


@app.post("/api/llm/route", response_model=RouterDecisionResponse, tags=["llm"])
async def api_route_model(payload: RouterDecisionRequest) -> RouterDecisionResponse:
    return route_model(payload)


@app.post("/api/llm/scout", response_model=Dict[str, str], tags=["llm"])
async def api_run_scout() -> Dict[str, str]:
    return run_external_scout_scan()


@app.post("/api/llm/optimize", response_model=Dict[str, str], tags=["llm"])
async def api_run_optimizer() -> Dict[str, str]:
    return run_internal_optimizer()


@app.get("/api/tools", response_model=List[ToolRecord], tags=["tools"])
async def api_list_tools(category: Optional[ToolCategory] = None, tab: Optional[str] = None) -> List[ToolRecord]:
    return list_tools(category=category, tab=tab)


@app.post("/api/tools/execute", response_model=ToolExecuteResponse, tags=["tools"])
async def api_execute_tool(payload: ToolExecuteRequest) -> ToolExecuteResponse:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: lazy_execute_tool(payload))


@app.get("/api/agents", response_model=List[AgentRecord], tags=["agents"])
async def api_list_agents(tab: Optional[str] = None) -> List[AgentRecord]:
    return list_all_agents(tab=tab)


@app.post("/api/agents/run", response_model=AgentRunResponse, tags=["agents"])
async def api_run_agent(payload: AgentRunRequest) -> AgentRunResponse:
    return await run_agent_task(payload)


@app.get("/api/agents/cua/isolation", response_model=GenericDictResponse, tags=["agents"])
async def api_cua_isolation() -> GenericDictResponse:
    info = verify_cua_space_isolation()
    return GenericDictResponse(status="verified", **info)


@app.post("/api/agents/gpu/batch", response_model=GenericDictResponse, tags=["agents"])
async def api_gpu_batch(payload: GpuBatchRequest) -> GenericDictResponse:
    loop = asyncio.get_running_loop()
    info = await loop.run_in_executor(
        None,
        lambda: run_parallel_gpu_batch(
            total_images=payload.total_images,
            workers=payload.workers,
            model_id=payload.model_id,
        ),
    )
    return GenericDictResponse(status="completed", **info)


@app.get("/api/requests", response_model=List[SandboxBundleDetail], tags=["sandboxes"])
async def api_list_requests() -> List[SandboxBundleDetail]:
    return requests_service.list_request_bundles()


@app.post("/api/requests", response_model=SandboxBundleDetail, tags=["sandboxes"])
async def api_create_quick_request(payload: QuickRequestCreate) -> SandboxBundleDetail:
    return await requests_service.submit_quick_request(payload)


@app.get("/api/requests/{sandbox_id}", response_model=SandboxBundleDetail, tags=["sandboxes"])
async def api_get_request(sandbox_id: str) -> SandboxBundleDetail:
    bundle = requests_service.get_request_bundle(sandbox_id)
    if bundle is None:
        raise HTTPException(status_code=404, detail=f"Request sandbox '{sandbox_id}' not found")
    return bundle


@app.get("/api/finished", response_model=List[SandboxBundleDetail], tags=["sandboxes"])
async def api_list_finished() -> List[SandboxBundleDetail]:
    return finished_service.list_finished_bundles()


@app.get("/api/finished/{sandbox_id}", response_model=SandboxBundleDetail, tags=["sandboxes"])
async def api_get_finished(sandbox_id: str) -> SandboxBundleDetail:
    bundle = finished_service.get_finished_bundle(sandbox_id)
    if bundle is None:
        raise HTTPException(status_code=404, detail=f"Finished sandbox '{sandbox_id}' not found")
    return bundle
