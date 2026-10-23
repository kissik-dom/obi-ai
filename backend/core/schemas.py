"""Strict Pydantic v2 request/response models for Kingdom AI OS (zero unvalidated raw dicts)."""

from __future__ import annotations

from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

GuardrailLevel = Literal["OBLITERATED", "LOW_GUARDRAIL", "NORMAL", "HIGH_SAFETY"]
MaturityLevel = Literal["production", "staging", "experimental", "quarantine"]
ModelTier = Literal["S", "A", "B", "C", "V", "X"]
ModelType = Literal["llm", "vision", "image", "video", "audio", "embedding", "reranker"]
HealthState = Literal["healthy", "degraded", "offline"]
TaskState = Literal[
    "queued",
    "running",
    "waiting",
    "approval_required",
    "blocked",
    "completed",
    "failed",
    "cancelled",
    "scheduled",
    "recurring",
]
ToolCategory = Literal["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
IsolationMode = Literal[
    "face_only_biometric",
    "hair_only",
    "jewelry_only",
    "clothes_only",
    "background_only",
    "combined_directors_cut",
]


class ModelRecord(BaseModel):
    """Typed registry record for all 205+ LLMs and multimodal models."""

    model_config = ConfigDict(extra="forbid")

    id: str
    canonicalName: str
    provider: str
    repo: str
    revision: str = "main"
    checksum: str
    family: str
    tier: ModelTier
    tierCode: str
    type: ModelType
    modalities: List[str]
    parameters: str
    contextTokens: int = Field(ge=512)
    license: str
    commercialUse: bool = True
    local: bool = True
    endpoints: List[str]
    costPerMillionTokens: float = Field(ge=0.0)
    quotaNotes: str = "10-key OpenRouter pool + local vLLM fallback"
    vramGb: int = Field(ge=1)
    guardrail: GuardrailLevel
    maturity: MaturityLevel = "production"
    priority: int = Field(ge=1)
    benchmarkScore: float = Field(ge=0.0, le=100.0)
    health: HealthState = "healthy"
    fallbacks: List[str]
    specialty: str
    provenance: str = "huihui-vault-v2"
    lastVerifiedAt: str = "2026-10-23T00:00:00Z"


class RouterDecisionRequest(BaseModel):
    """Input payload for deterministic priority LLM routing."""

    model_config = ConfigDict(extra="forbid")

    tab: str = "home"
    prompt: str = ""
    required_modality: str = "text"
    required_context_tokens: int = Field(default=4096, ge=1)
    require_tools: bool = False
    local_only: bool = False
    available_vram_gb: int = Field(default=80, ge=1)
    require_commercial_license: bool = False
    preferred_model_id: Optional[str] = None


class ScoredCandidate(BaseModel):
    """Scored candidate from the router ranking equation."""

    model_config = ConfigDict(extra="forbid")

    model_id: str
    canonical_name: str
    tier_code: str
    guardrail: GuardrailLevel
    priority: int
    score: float
    fallbacks: List[str]
    specialty: str


class RouterDecisionResponse(BaseModel):
    """Deterministic LLM router output."""

    model_config = ConfigDict(extra="forbid")

    selected_model: ModelRecord
    score: float
    formula: str
    fallback_chain: List[str]
    reasoning: str
    openrouter_key_slots: int
    num_retries: int = 3
    timeout_seconds: int = 60
    top_candidates: List[ScoredCandidate]


class ToolRecord(BaseModel):
    """Typed registry record for all 920+ open-source and Composio tools."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    category: ToolCategory
    categoryName: str
    version: str = "1.0.0"
    license: str = "MIT/Apache-2.0"
    install_cmd: str
    python_import: str
    docker_stage: str
    api_endpoint: str
    env_vars: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    tabs_used_by: List[str]
    lazy_loaded: bool = True
    open_source: bool = True


class ToolExecuteRequest(BaseModel):
    """Lazy-imported tool execution request."""

    model_config = ConfigDict(extra="forbid")

    tool_id: str
    tab: str = "opensource"
    action: str = "run"
    params: Dict[str, str] = Field(default_factory=dict)


class ToolExecuteResponse(BaseModel):
    """Validated output from lazy-imported tool runner."""

    model_config = ConfigDict(extra="forbid")

    tool_id: str
    tool_name: str
    category: ToolCategory
    docker_stage: str
    lazy_loaded: bool = True
    status: Literal["completed", "fallback_completed", "disabled"]
    summary: str
    artifact_path: str
    timestamp: str


class AgentRecord(BaseModel):
    """Typed specification for each of the 12 Sovereign Agents + Hermes specialists."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    role: str
    group: Literal["sovereign_12", "hermes_swarm", "custom"]
    primary_llm: str
    backup_llms: List[str]
    tools: List[str]
    tabs: List[str]
    turn_off_flag: str
    enabled: bool = True
    status: Literal["online", "standby", "disabled"] = "online"
    cadence: str = "on-demand"
    description: str


class AgentRunRequest(BaseModel):
    """Trigger payload for executing an agent inside an isolated sandbox."""

    model_config = ConfigDict(extra="forbid")

    agent_id: str
    tab: str = "agents"
    objective: str = Field(min_length=1)
    equip_sandbox: Optional[bool] = None


class AgentRunResponse(BaseModel):
    """Agent execution result linked to sandbox artifacts."""

    model_config = ConfigDict(extra="forbid")

    agent_id: str
    agent_name: str
    sandbox_id: str
    model_used: str
    status: Literal["completed", "disabled"]
    output: str
    finished_path: str
    timestamp: str


class SandboxEquipStatus(BaseModel):
    """Detailed equip manifest proving what resources were attached to a task sandbox."""

    model_config = ConfigDict(extra="forbid")

    sandbox_id: str
    equipped_all: bool
    qdrant_namespace: str
    minio_requests_uri: str
    minio_finished_uri: str
    vault_transit_policy: str
    postgres_task_id: str
    redis_stream: str
    cua_space_id: str
    wireguard_isolated: bool
    falco_ebpf_monitored: bool
    gpu_worker_pool: str
    tools_available: int
    models_available: int
    hermes_enabled: bool


class TaskCreateRequest(BaseModel):
    """Create a task in any tab or via Quick Request."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=300)
    prompt: str = Field(default="")
    tab: str = Field(default="tasks")
    task_type: str = Field(default="standard")
    state: TaskState = Field(default="queued")
    assigned_agent: str = Field(default="bugfix_agent")
    preferred_model: Optional[str] = None
    idempotency_key: Optional[str] = None
    auto_complete: bool = True

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("title must not be blank")
        return cleaned


class TaskStateUpdateRequest(BaseModel):
    """Transition a task across the 10 valid states."""

    model_config = ConfigDict(extra="forbid")

    state: TaskState
    result_summary: Optional[str] = None


class TaskRecord(BaseModel):
    """Relational task record stored in Postgres/SQLAlchemy and mirrored to MinIO."""

    model_config = ConfigDict(extra="forbid")

    id: str
    idempotency_key: str
    sandbox_id: str
    tab: str
    task_type: str
    title: str
    prompt: str
    state: TaskState
    assigned_agent: str
    model_used: str
    tools_used: List[str]
    result_summary: str
    requests_uri: str
    finished_uri: str
    opentimestamps_proof: str
    ipfs_cid: str
    created_at: str
    updated_at: str


class QuickRequestCreate(BaseModel):
    """Quick Request button payload -> s3://kingdom-requests/{sandbox_id}/."""

    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(min_length=1)
    tab: str = "home"
    task_type: str = "quick"
    isolation_mode: Optional[str] = None
    refs: Dict[str, str] = Field(default_factory=dict)


class SandboxFileEntry(BaseModel):
    """File entry inside s3://kingdom-requests/ or s3://kingdom-finished/."""

    model_config = ConfigDict(extra="forbid")

    path: str
    size_bytes: int
    Bucket: str
    content_preview: str = ""


class SandboxBundleDetail(BaseModel):
    """Complete inspectable dossier for Finished Folder & Requests Folder."""

    model_config = ConfigDict(extra="forbid")

    sandbox_id: str
    bucket: str
    tab: str
    task_id: str
    title: str
    state: TaskState
    model_used: str
    summary_md: str
    request_json: Dict[str, str]
    response_json: Dict[str, str]
    audit_json: Dict[str, str]
    artifacts: List[str]
    evidence: List[str]
    logs: List[str]
    metrics: Dict[str, str]
    equip_status: SandboxEquipStatus
    created_at: str


class ChatTurnRequest(BaseModel):
    """Chat message submitted inside any of the 24->28 tabs."""

    model_config = ConfigDict(extra="forbid")

    message: str = Field(min_length=1)
    preferred_model_id: Optional[str] = None
    agent_id: Optional[str] = None
    use_hermes_swarm: bool = True
    isolation_mode: Optional[IsolationMode] = None

    @field_validator("message")
    @classmethod
    def validate_msg(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("message cannot be empty")
        return s


class ChatMessageRecord(BaseModel):
    """Persisted chat turn."""

    model_config = ConfigDict(extra="forbid")

    id: str
    tab: str
    role: Literal["user", "assistant"]
    content: str
    model_id: str
    agent_id: str
    sandbox_id: str
    created_at: str


class ChatTurnResponse(BaseModel):
    """Unified one-batch chat response with full routing provenance and sandbox ID."""

    model_config = ConfigDict(extra="forbid")

    tab: str
    user_message: ChatMessageRecord
    assistant_message: ChatMessageRecord
    router_decision: RouterDecisionResponse
    sandbox: SandboxEquipStatus
    task: TaskRecord
    hermes_specialist: Optional[str] = None


class TrainingIngestRequest(BaseModel):
    """Ingest document/corpus into Qdrant 768d Cosine memory for a tab."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    source_uri: str = "manual://training-tab"


class TrainingDocumentRecord(BaseModel):
    """Ingested training corpus item."""

    model_config = ConfigDict(extra="forbid")

    doc_id: str
    tab: str
    title: str
    tokens_estimated: int
    vector_dim: int = 768
    qdrant_collection: str
    minio_uri: str
    ingested_at: str


class KnowledgeQueryRequest(BaseModel):
    """Semantic search against Qdrant 768d Cosine store."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=25)


class KnowledgeHit(BaseModel):
    """Vector similarity match."""

    model_config = ConfigDict(extra="forbid")

    doc_id: str
    tab: str
    title: str
    excerpt: str
    cosine_score: float
    source_uri: str


class KnowledgeQueryResponse(BaseModel):
    """Semantic search response."""

    model_config = ConfigDict(extra="forbid")

    tab: str
    query: str
    vector_dim: int = 768
    hits: List[KnowledgeHit]


class FileCreateRequest(BaseModel):
    """Upload or register a file inside a tab's MinIO bucket namespace."""

    model_config = ConfigDict(extra="forbid")

    filename: str = Field(min_length=1)
    content: str = ""
    bucket_kind: Literal["requests", "finished"] = "finished"


class FileRecord(BaseModel):
    """Stored MinIO object metadata."""

    model_config = ConfigDict(extra="forbid")

    object_key: str
    bucket: str
    tab: str
    size_bytes: int
    sha256: str
    created_at: str


class OutputDeliverableRecord(BaseModel):
    """Unified single-batch output item for a tab."""

    model_config = ConfigDict(extra="forbid")

    output_id: str
    sandbox_id: str
    tab: str
    title: str
    batch_format: str
    uri: str
    opentimestamps_proof: str
    ipfs_cid: str
    created_at: str


class TabSettingsModel(BaseModel):
    """Per-tab configurable routing and sandbox settings."""

    model_config = ConfigDict(extra="forbid")

    tab: str
    default_model_id: str
    guardrail_filter: GuardrailLevel = "OBLITERATED"
    equip_sandbox_all: bool = True
    hermes_enabled: bool = True
    auto_notarize_ipfs: bool = True
    flags: Dict[str, bool]


class TabSettingsUpdateRequest(BaseModel):
    """Patch per-tab settings and global ENABLE_* flags."""

    model_config = ConfigDict(extra="forbid")

    default_model_id: Optional[str] = None
    guardrail_filter: Optional[GuardrailLevel] = None
    equip_sandbox_all: Optional[bool] = None
    hermes_enabled: Optional[bool] = None
    auto_notarize_ipfs: Optional[bool] = None
    flags: Dict[str, bool] = Field(default_factory=dict)


class TabSpecRecord(BaseModel):
    """Complete metadata for each of the 24 core tabs and extensible 25-28+ tabs."""

    model_config = ConfigDict(extra="forbid")

    index: int
    slug: str
    title: str
    chapter: str
    accent: Literal["magenta", "turquoise", "orange"]
    purpose: str
    best_llm: str
    top_llms: List[str]
    tool_categories: List[ToolCategory]
    top_tools: List[str]
    agents: List[str]
    router_logic: str
    core: bool = True
    grammar: List[str] = Field(
        default_factory=lambda: [
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
    )


class SecurityAttemptRecord(BaseModel):
    """Cowrie Honeypot + CrowdSec + Falco eBPF security telemetry record."""

    model_config = ConfigDict(extra="forbid")

    attempt_id: str
    timestamp: str
    ip: str
    asn: str
    geoip: str
    ja3: str
    wifi_ssid: str
    vultr_location: str
    path: str
    actor_type: str
    is_bot: bool
    action: str
    honeypot_recording_id: str


class SecurityAttemptsResponse(BaseModel):
    """Response for GET /api/security/attempts."""

    model_config = ConfigDict(extra="forbid")

    status: str
    layers: List[str]
    attempts: List[SecurityAttemptRecord]


class BiometricOptInRequest(BaseModel):
    """Legal opt-in consent payload for VideoKYC / CompreFace FIDO2."""

    model_config = ConfigDict(extra="forbid")

    consent: bool
    bipa_gdpr_acknowledged: bool = True
    subject_id: str = "sovereign-operator"
    video_clip_hash: str = ""


class BiometricOptInResponse(BaseModel):
    """Validated BIPA/GDPR VideoKYC opt-in result."""

    model_config = ConfigDict(extra="forbid")

    verified: bool
    can_access_financial: bool
    vault_hsm_key_id: str
    retention_days: int = 30
    storage_location: str
    legal_notice: str
    is_owner_allowlisted: bool


class BotCheckRequest(BaseModel):
    """JA3 + pointer entropy bot check."""

    model_config = ConfigDict(extra="forbid")

    ja3: str = "unknown"
    mouse_moves: int = Field(default=10, ge=0)
    request_interval_ms: int = Field(default=500, ge=0)


class BotCheckResponse(BaseModel):
    """Bot detection verdict with owner allowlist protection."""

    model_config = ConfigDict(extra="forbid")

    is_bot: bool
    allow_financial: bool
    owner_allowlisted: bool
    reason: str


class BugfixTriggerRequest(BaseModel):
    """Payload sent by testing_agent.py when an endpoint degrades."""

    model_config = ConfigDict(extra="forbid")

    failed_endpoints: List[str] = Field(default_factory=list)
    reason: str = "automated-healthcheck"


class BugfixStatusResponse(BaseModel):
    """Status of BugFix + Testing self-healing loop."""

    model_config = ConfigDict(extra="forbid")

    status: str
    check_interval_seconds: int = 10
    test_interval_seconds: int
    detectors: List[str]
    remediations_run: int
    last_checked_at: str


class ImageConsistencyRequest(BaseModel):
    """7-Subagent Director's Cut & Biometric Isolation batch request."""

    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(min_length=1)
    isolation_mode: IsolationMode = "combined_directors_cut"
    face_refs: List[str] = Field(default_factory=lambda: ["Face1"])
    hair_refs: List[str] = Field(default_factory=lambda: ["Hair1"])
    jewelry_refs: List[str] = Field(default_factory=lambda: ["Jewelry1"])
    clothes_refs: List[str] = Field(default_factory=lambda: ["Outfit1"])
    background_ref: str = "Studio1"
    stone_filter: Optional[Literal["all", "diamonds_only", "rubies_only", "emeralds_only"]] = "all"
    recolor_hair: Optional[str] = None
    batch_count: int = Field(default=12, ge=1, le=1000)


class ImageConsistencyResponse(BaseModel):
    """Unified single-batch response from Image Consistency Director."""

    model_config = ConfigDict(extra="forbid")

    sandbox_id: str
    model_used: str
    isolation_mode: IsolationMode
    subagents_deployed: List[str]
    angles_rendered: List[str]
    biometrics_preserved: List[str]
    zero_skin_bleed_verified: bool
    face_cosine_similarity: float
    total_images_in_single_batch: int
    gpu_workers_allocated: int
    unified_zip_uri: str
    contact_sheet_pdf_uri: str


class VideoPipelineRequest(BaseModel):
    """Long-form UGC/TV/Movie chunked generation & FFmpeg+WhisperX stitch request."""

    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(min_length=1)
    target_duration_seconds: int = Field(default=300, ge=10, le=18000)
    clip_duration_seconds: int = Field(default=30, ge=5, le=60)
    parallel_workers: int = Field(default=10, ge=1, le=200)
    primary_video_model: str = "minimax-hailuo-02"


class VideoPipelineResponse(BaseModel):
    """Unified single MP4 output manifest for long-form stitched video."""

    model_config = ConfigDict(extra="forbid")

    sandbox_id: str
    primary_model: str
    prompt_builder_model: str
    angle_selector_model: str
    total_clips_planned: int
    clip_duration_seconds: int
    parallel_speedup_factor: int
    audio_sync_engine: str
    stitcher_pipeline: List[str]
    face_consistency_verified: bool
    final_single_mp4_uri: str


class VocalTuningRequest(BaseModel):
    """Vocal stem isolation, pitch correction & 808 production request."""

    model_config = ConfigDict(extra="forbid")

    track_title: str = Field(min_length=1)
    key_scale: str = "C Minor"
    retune_speed_ms: int = Field(default=8, ge=0, le=100)
    stems: Literal[2, 4, 5] = 4
    include_808_kit: bool = True


class VocalTuningResponse(BaseModel):
    """Unified audio master and stem manifest."""

    model_config = ConfigDict(extra="forbid")

    sandbox_id: str
    track_title: str
    key_scale: str
    tuning_chain: List[str]
    stem_separator: str
    stems_generated: List[str]
    eight_oh_eight_samples_available: int = 94
    mastered_wav_uri: str


class NewTabSkillRequest(BaseModel):
    """Request to programmatically add a new tab (25..28+) with identical grammar."""

    model_config = ConfigDict(extra="forbid")

    slug: str = Field(min_length=2, max_length=40, pattern=r"^[a-z][a-z0-9_]*$")
    title: str = Field(min_length=2, max_length=80)
    purpose: str = Field(min_length=4, max_length=400)
    best_llm: str = "qwen3.8-27b-2.19m"
    tool_categories: List[ToolCategory] = Field(default_factory=lambda: ["F", "L"])
    accent: Literal["magenta", "turquoise", "orange"] = "turquoise"


class NewTabSkillResponse(BaseModel):
    """Result of executing backend/agents/skills/new_tab_skill.py."""

    model_config = ConfigDict(extra="forbid")

    tab: TabSpecRecord
    files_created: List[str]
    total_tabs_active: int
    status: str


class HealthzResponse(BaseModel):
    """Bank-grade /healthz payload."""

    model_config = ConfigDict(extra="forbid")

    status: HealthState
    version: str
    tabs_registered: int
    models_registered: int
    open_source_tools: int
    total_tools: int
    agents_registered: int
    subsystems: Dict[str, str]
    flags: Dict[str, bool]
    timestamp: str
