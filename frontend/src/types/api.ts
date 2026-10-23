export type GuardrailLevel = "OBLITERATED" | "LOW_GUARDRAIL" | "NORMAL" | "HIGH_SAFETY";
export type MaturityLevel = "production" | "staging" | "experimental" | "quarantine";
export type ModelTier = "S" | "A" | "B" | "C" | "V" | "X";
export type HealthState = "healthy" | "degraded" | "offline";
export type ToolCategory = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M";

export type TaskState =
  | "queued"
  | "running"
  | "waiting"
  | "approval_required"
  | "blocked"
  | "completed"
  | "failed"
  | "cancelled"
  | "scheduled"
  | "recurring";

export type GrammarSection =
  | "chat"
  | "agents"
  | "open-tasks"
  | "completed-tasks"
  | "training"
  | "knowledge"
  | "files"
  | "tools"
  | "outputs"
  | "settings";

export type IsolationMode =
  | "face_only_biometric"
  | "hair_only"
  | "jewelry_only"
  | "clothes_only"
  | "background_only"
  | "combined_directors_cut";

export interface TabSpecRecord {
  index: number;
  slug: string;
  title: string;
  chapter: string;
  accent: "magenta" | "turquoise" | "orange";
  purpose: string;
  best_llm: string;
  top_llms: string[];
  tool_categories: ToolCategory[];
  top_tools: string[];
  agents: string[];
  router_logic: string;
  core: boolean;
  grammar: string[];
}

export interface ModelRecord {
  id: string;
  canonicalName: string;
  provider: string;
  repo: string;
  revision: string;
  checksum: string;
  family: string;
  tier: ModelTier;
  tierCode: string;
  type: string;
  modalities: string[];
  parameters: string;
  contextTokens: number;
  license: string;
  commercialUse: boolean;
  local: boolean;
  endpoints: string[];
  costPerMillionTokens: number;
  quotaNotes: string;
  vramGb: number;
  guardrail: GuardrailLevel;
  maturity: MaturityLevel;
  priority: number;
  benchmarkScore: number;
  health: HealthState;
  fallbacks: string[];
  specialty: string;
  provenance: string;
  lastVerifiedAt: string;
}

export interface ScoredCandidate {
  model_id: string;
  canonical_name: string;
  tier_code: string;
  guardrail: GuardrailLevel;
  priority: number;
  score: number;
  fallbacks: string[];
  specialty: string;
}

export interface RouterDecisionResponse {
  selected_model: ModelRecord;
  score: number;
  formula: string;
  fallback_chain: string[];
  reasoning: string;
  openrouter_key_slots: number;
  num_retries: number;
  timeout_seconds: number;
  top_candidates: ScoredCandidate[];
}

export interface SandboxEquipStatus {
  sandbox_id: string;
  equipped_all: boolean;
  qdrant_namespace: string;
  minio_requests_uri: string;
  minio_finished_uri: string;
  vault_transit_policy: string;
  postgres_task_id: string;
  redis_stream: string;
  cua_space_id: string;
  wireguard_isolated: boolean;
  falco_ebpf_monitored: boolean;
  gpu_worker_pool: string;
  tools_available: number;
  models_available: number;
  hermes_enabled: boolean;
}

export interface TaskRecord {
  id: string;
  idempotency_key: string;
  sandbox_id: string;
  tab: string;
  task_type: string;
  title: string;
  prompt: string;
  state: TaskState;
  assigned_agent: string;
  model_used: string;
  tools_used: string[];
  result_summary: string;
  requests_uri: string;
  finished_uri: string;
  opentimestamps_proof: string;
  ipfs_cid: string;
  created_at: string;
  updated_at: string;
}

export interface ChatMessageRecord {
  id: string;
  tab: string;
  role: "user" | "assistant";
  content: string;
  model_id: string;
  agent_id: string;
  sandbox_id: string;
  created_at: string;
}

export interface ChatTurnResponse {
  tab: string;
  user_message: ChatMessageRecord;
  assistant_message: ChatMessageRecord;
  router_decision: RouterDecisionResponse;
  sandbox: SandboxEquipStatus;
  task: TaskRecord;
  hermes_specialist: string | null;
}

export interface AgentRecord {
  id: string;
  name: string;
  role: string;
  group: "sovereign_12" | "hermes_swarm" | "custom";
  primary_llm: string;
  backup_llms: string[];
  tools: string[];
  tabs: string[];
  turn_off_flag: string;
  enabled: boolean;
  status: "online" | "standby" | "disabled";
  cadence: string;
  description: string;
}

export interface AgentRunResponse {
  agent_id: string;
  agent_name: string;
  sandbox_id: string;
  model_used: string;
  status: "completed" | "disabled";
  output: string;
  finished_path: string;
  timestamp: string;
}

export interface ToolRecord {
  id: string;
  name: string;
  category: ToolCategory;
  categoryName: string;
  version: string;
  license: string;
  install_cmd: string;
  python_import: string;
  docker_stage: string;
  api_endpoint: string;
  env_vars: string[];
  dependencies: string[];
  tabs_used_by: string[];
  lazy_loaded: boolean;
  open_source: boolean;
}

export interface ToolExecuteResponse {
  tool_id: string;
  tool_name: string;
  category: ToolCategory;
  docker_stage: string;
  lazy_loaded: boolean;
  status: "completed" | "fallback_completed" | "disabled";
  summary: string;
  artifact_path: string;
  timestamp: string;
}

export interface TrainingDocumentRecord {
  doc_id: string;
  tab: string;
  title: string;
  tokens_estimated: number;
  vector_dim: number;
  qdrant_collection: string;
  minio_uri: string;
  ingested_at: string;
}

export interface KnowledgeHit {
  doc_id: string;
  tab: string;
  title: string;
  excerpt: string;
  cosine_score: number;
  source_uri: string;
}

export interface KnowledgeQueryResponse {
  tab: string;
  query: string;
  vector_dim: number;
  hits: KnowledgeHit[];
}

export interface FileRecord {
  object_key: string;
  bucket: string;
  tab: string;
  size_bytes: number;
  sha256: string;
  created_at: string;
}

export interface OutputDeliverableRecord {
  output_id: string;
  sandbox_id: string;
  tab: string;
  title: string;
  batch_format: string;
  uri: string;
  opentimestamps_proof: string;
  ipfs_cid: string;
  created_at: string;
}

export interface TabSettingsModel {
  tab: string;
  default_model_id: string;
  guardrail_filter: GuardrailLevel;
  equip_sandbox_all: boolean;
  hermes_enabled: boolean;
  auto_notarize_ipfs: boolean;
  flags: Record<string, boolean>;
}

export interface SandboxBundleDetail {
  sandbox_id: string;
  bucket: string;
  tab: string;
  task_id: string;
  title: string;
  state: TaskState;
  model_used: string;
  summary_md: string;
  request_json: Record<string, string>;
  response_json: Record<string, string>;
  audit_json: Record<string, string>;
  artifacts: string[];
  evidence: string[];
  logs: string[];
  metrics: Record<string, string>;
  equip_status: SandboxEquipStatus;
  created_at: string;
}

export interface HealthzResponse {
  status: HealthState;
  version: string;
  tabs_registered: number;
  models_registered: number;
  open_source_tools: number;
  total_tools: number;
  agents_registered: number;
  subsystems: Record<string, string>;
  flags: Record<string, boolean>;
  timestamp: string;
}

export interface GhidraAnalyzeResponse {
  binary_name: string;
  sha256_prefix: string;
  engine: string;
  llm_sre_model: string;
  escalation_model: string;
  functions_recovered: Array<Record<string, string>>;
  vulnerabilities_flagged: number;
  decompiled_c_preview: string;
}

export interface FreeCadScrewResponse {
  thread_spec: string;
  standard: string;
  material: string;
  pitch_mm: number;
  through_hole_clearance_mm: number;
  counterbore_diameter_mm: number;
  recommended_torque_nm: number;
  boss_count: number;
  bom_manager: string;
  openscad_script: string;
  stl_artifact: string;
  step_artifact: string;
}

export interface PropulsionSimResponse {
  mode: string;
  solvers: string[];
  drive_frequency_khz: number;
  resonator_q_factor: number;
  reactive_stored_energy_joules: number;
  predicted_net_force_micro_newtons: number;
  thermal_margin_kelvin: number;
  kicad_hv_clearance_mm: number;
  status: string;
}

export interface ImageConsistencyResponse {
  sandbox_id: string;
  model_used: string;
  isolation_mode: IsolationMode;
  subagents_deployed: string[];
  angles_rendered: string[];
  biometrics_preserved: string[];
  zero_skin_bleed_verified: boolean;
  face_cosine_similarity: number;
  total_images_in_single_batch: number;
  gpu_workers_allocated: number;
  unified_zip_uri: string;
  contact_sheet_pdf_uri: string;
}

export interface VideoPipelineResponse {
  sandbox_id: string;
  primary_model: string;
  prompt_builder_model: string;
  angle_selector_model: string;
  total_clips_planned: number;
  clip_duration_seconds: number;
  parallel_speedup_factor: number;
  audio_sync_engine: string;
  stitcher_pipeline: string[];
  face_consistency_verified: boolean;
  final_single_mp4_uri: string;
}

export interface VocalTuningResponse {
  sandbox_id: string;
  track_title: string;
  key_scale: string;
  tuning_chain: string[];
  stem_separator: string;
  stems_generated: string[];
  eight_oh_eight_samples_available: number;
  mastered_wav_uri: string;
}

export interface SecurityAttemptRecord {
  attempt_id: string;
  timestamp: string;
  ip: string;
  asn: string;
  geoip: string;
  ja3: string;
  wifi_ssid: string;
  vultr_location: string;
  path: string;
  actor_type: string;
  is_bot: boolean;
  action: string;
  honeypot_recording_id: string;
}

export interface SecurityAttemptsResponse {
  status: string;
  layers: string[];
  attempts: SecurityAttemptRecord[];
}

export interface BiometricOptInResponse {
  verified: boolean;
  can_access_financial: boolean;
  vault_hsm_key_id: string;
  retention_days: number;
  storage_location: string;
  legal_notice: string;
  is_owner_allowlisted: boolean;
}

export interface PassportIssueResponse {
  passport_id: string;
  holder: string;
  scope: string;
  qr_payload: string;
  vault_hsm_ref: string;
  opentimestamps_proof: string;
  ipfs_cid: string;
  issued_at: string;
}

export interface NewTabSkillResponse {
  tab: TabSpecRecord;
  files_created: string[];
  total_tabs_active: number;
  status: string;
}

export interface VaultKeyStatusResponse {
  vault_seal_ref: string;
  configured_openrouter_keys: number;
  masked_slots: string[];
  obliteratus_configured: boolean;
  composio_configured: boolean;
}
