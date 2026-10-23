import type {
  AgentRecord,
  AgentRunResponse,
  BiometricOptInResponse,
  ChatMessageRecord,
  ChatTurnResponse,
  FileRecord,
  FreeCadScrewResponse,
  GhidraAnalyzeResponse,
  HealthzResponse,
  ImageConsistencyResponse,
  IsolationMode,
  KnowledgeQueryResponse,
  ModelRecord,
  NewTabSkillResponse,
  OutputDeliverableRecord,
  PassportIssueResponse,
  PropulsionSimResponse,
  SandboxBundleDetail,
  SecurityAttemptsResponse,
  TabSettingsModel,
  TabSpecRecord,
  TaskRecord,
  TaskState,
  ToolCategory,
  ToolExecuteResponse,
  ToolRecord,
  TrainingDocumentRecord,
  VaultKeyStatusResponse,
  VideoPipelineResponse,
  VocalTuningResponse,
} from "../types/api";

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });
  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errText}`);
  }
  return (await response.json()) as T;
}

export const apiClient = {
  getHealthz: () => requestJson<HealthzResponse>("/healthz"),

  listTabs: (includeExtended = true) =>
    requestJson<TabSpecRecord[]>(`/api/tabs?include_extended=${includeExtended ? "true" : "false"}`),

  addTab: (payload: {
    slug: string;
    title: string;
    purpose: string;
    best_llm: string;
    tool_categories: ToolCategory[];
    accent: "magenta" | "turquoise" | "orange";
  }) =>
    requestJson<NewTabSkillResponse>("/api/tabs/add", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  listModels: () => requestJson<ModelRecord[]>("/api/llm/models"),

  listAllTools: (category?: ToolCategory) =>
    requestJson<ToolRecord[]>(category ? `/api/tools?category=${category}` : "/api/tools"),

  // 10-Section Tab Grammar
  getChatHistory: (tab: string) => requestJson<ChatMessageRecord[]>(`/api/tabs/${tab}/chat`),

  sendChat: (
    tab: string,
    payload: {
      message: string;
      preferred_model_id?: string | null;
      agent_id?: string | null;
      use_hermes_swarm: boolean;
      isolation_mode?: IsolationMode | null;
    }
  ) =>
    requestJson<ChatTurnResponse>(`/api/tabs/${tab}/chat`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getTabAgents: (tab: string) => requestJson<AgentRecord[]>(`/api/tabs/${tab}/agents`),

  runTabAgent: (tab: string, agent_id: string, objective: string) =>
    requestJson<AgentRunResponse>(`/api/tabs/${tab}/agents`, {
      method: "POST",
      body: JSON.stringify({ agent_id, tab, objective }),
    }),

  getOpenTasks: (tab: string) => requestJson<TaskRecord[]>(`/api/tabs/${tab}/open-tasks`),

  createOpenTask: (tab: string, title: string, prompt: string, state: TaskState = "queued") =>
    requestJson<TaskRecord>(`/api/tabs/${tab}/open-tasks`, {
      method: "POST",
      body: JSON.stringify({ title, prompt, tab, state }),
    }),

  updateTaskState: (tab: string, taskId: string, state: TaskState, result_summary?: string) =>
    requestJson<TaskRecord>(`/api/tabs/${tab}/open-tasks/${taskId}`, {
      method: "PATCH",
      body: JSON.stringify({ state, result_summary }),
    }),

  getCompletedTasks: (tab: string) => requestJson<TaskRecord[]>(`/api/tabs/${tab}/completed-tasks`),

  getTrainingDocs: (tab: string) => requestJson<TrainingDocumentRecord[]>(`/api/tabs/${tab}/training`),

  ingestTrainingDoc: (tab: string, title: string, content: string, source_uri: string) =>
    requestJson<TrainingDocumentRecord>(`/api/tabs/${tab}/training`, {
      method: "POST",
      body: JSON.stringify({ title, content, source_uri }),
    }),

  queryKnowledge: (tab: string, query: string) =>
    requestJson<KnowledgeQueryResponse>(`/api/tabs/${tab}/knowledge`, {
      method: "POST",
      body: JSON.stringify({ query, limit: 8 }),
    }),

  getTabFiles: (tab: string) => requestJson<FileRecord[]>(`/api/tabs/${tab}/files`),

  uploadTabFile: (tab: string, filename: string, content: string, bucket_kind: "requests" | "finished") =>
    requestJson<FileRecord>(`/api/tabs/${tab}/files`, {
      method: "POST",
      body: JSON.stringify({ filename, content, bucket_kind }),
    }),

  getTabTools: (tab: string) => requestJson<ToolRecord[]>(`/api/tabs/${tab}/tools`),

  executeTabTool: (tab: string, tool_id: string, action = "run") =>
    requestJson<ToolExecuteResponse>(`/api/tabs/${tab}/tools`, {
      method: "POST",
      body: JSON.stringify({ tool_id, tab, action, params: {} }),
    }),

  getTabOutputs: (tab: string) => requestJson<OutputDeliverableRecord[]>(`/api/tabs/${tab}/outputs`),

  getTabSettings: (tab: string) => requestJson<TabSettingsModel>(`/api/tabs/${tab}/settings`),

  saveTabSettings: (
    tab: string,
    payload: {
      default_model_id?: string;
      guardrail_filter?: string;
      equip_sandbox_all?: boolean;
      hermes_enabled?: boolean;
      auto_notarize_ipfs?: boolean;
      flags?: Record<string, boolean>;
    }
  ) =>
    requestJson<TabSettingsModel>(`/api/tabs/${tab}/settings`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),

  // Sandboxes: Quick Requests & Finished Folder
  listRequests: () => requestJson<SandboxBundleDetail[]>("/api/requests"),
  submitQuickRequest: (prompt: string, tab: string) =>
    requestJson<SandboxBundleDetail>("/api/requests", {
      method: "POST",
      body: JSON.stringify({ prompt, tab, task_type: "quick" }),
    }),
  listFinished: () => requestJson<SandboxBundleDetail[]>("/api/finished"),
  getFinishedById: (sandboxId: string) => requestJson<SandboxBundleDetail>(`/api/finished/${sandboxId}`),

  // Specialized Domain Studios
  analyzeGhidra: (binary_name: string, hex_sample: string) =>
    requestJson<GhidraAnalyzeResponse>("/api/engineering/ghidra/analyze", {
      method: "POST",
      body: JSON.stringify({ binary_name, hex_sample }),
    }),
  generateFreeCadScrew: (thread_spec: string, material: string, boss_count: number) =>
    requestJson<FreeCadScrewResponse>("/api/engineering/freecad/screw", {
      method: "POST",
      body: JSON.stringify({ thread_spec, material, boss_count }),
    }),
  simulatePropulsion: (mode: string, drive_freq_khz: number) =>
    requestJson<PropulsionSimResponse>("/api/engineering/anti-gravity", {
      method: "POST",
      body: JSON.stringify({ mode, drive_freq_khz }),
    }),
  runImageConsistency: (payload: {
    prompt: string;
    isolation_mode: IsolationMode;
    stone_filter: "all" | "diamonds_only" | "rubies_only" | "emeralds_only";
    batch_count: number;
  }) =>
    requestJson<ImageConsistencyResponse>("/api/images/consistency", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  runVideoStitch: (payload: {
    prompt: string;
    target_duration_seconds: number;
    clip_duration_seconds: number;
    parallel_workers: number;
    primary_video_model: string;
  }) =>
    requestJson<VideoPipelineResponse>("/api/video/stitch", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  runVocalTuning: (payload: {
    track_title: string;
    key_scale: string;
    retune_speed_ms: number;
    stems: 2 | 4 | 5;
    include_808_kit: boolean;
  }) =>
    requestJson<VocalTuningResponse>("/api/music/vocal-tune", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getSecurityAttempts: () => requestJson<SecurityAttemptsResponse>("/api/security/attempts"),
  optInBiometric: (consent: boolean, subject_id: string) =>
    requestJson<BiometricOptInResponse>("/api/security/biometric/opt-in", {
      method: "POST",
      body: JSON.stringify({ consent, bipa_gdpr_acknowledged: consent, subject_id }),
    }),
  issuePassport: (holder: string, scope: string) =>
    requestJson<PassportIssueResponse>("/api/passport/issue", {
      method: "POST",
      body: JSON.stringify({ holder, scope }),
    }),
  getVaultKeyStatus: () => requestJson<VaultKeyStatusResponse>("/api/vault/llm-keys"),
  sealVaultKeys: (payload: {
    openrouter_key_1: string;
    openrouter_key_2: string;
    obliteratus_api_key: string;
    composio_api_key: string;
  }) =>
    requestJson<VaultKeyStatusResponse>("/api/vault/llm-keys", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
