import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "../lib/apiClient";
import { useKingdomStore } from "../store/useKingdomStore";
import type {
  ChatTurnResponse,
  GrammarSection,
  ModelRecord,
  TabSpecRecord,
  TaskState,
} from "../types/api";
import { CopyButton } from "./CopyButton";
import {
  EngineeringStudio,
  ImageDirectorStudio,
  SecurityKycStudio,
  VideoStitchStudio,
  VocalTuningStudio,
} from "./DomainStudios";

const GRAMMAR_SECTIONS: Array<{ id: GrammarSection; label: string }> = [
  { id: "chat", label: "1. Chat" },
  { id: "agents", label: "2. Agents" },
  { id: "open-tasks", label: "3. Open Tasks" },
  { id: "completed-tasks", label: "4. Completed Tasks" },
  { id: "training", label: "5. Training" },
  { id: "knowledge", label: "6. Knowledge" },
  { id: "files", label: "7. Files" },
  { id: "tools", label: "8. Tools" },
  { id: "outputs", label: "9. Outputs" },
  { id: "settings", label: "10. Settings" },
];

const ALL_TASK_STATES: TaskState[] = [
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
];

interface TabWorkspaceProps {
  tabSpec: TabSpecRecord;
  models: ModelRecord[];
}

export function TabWorkspace({ tabSpec, models }: TabWorkspaceProps) {
  const queryClient = useQueryClient();
  const { activeSection, setActiveSection, openSandboxDrawer } = useKingdomStore();

  const [chatInput, setChatInput] = useState("");
  const [preferredModel, setPreferredModel] = useState<string>("");
  const [useHermes, setUseHermes] = useState(true);
  const [lastTurn, setLastTurn] = useState<ChatTurnResponse | null>(null);

  const [agentObj, setAgentObj] = useState("Execute sovereign synthesis and verify sandbox deliverables");
  const [taskTitle, setTaskTitle] = useState("");
  const [taskPrompt, setTaskPrompt] = useState("");
  const [trainTitle, setTrainTitle] = useState("");
  const [trainContent, setTrainContent] = useState("");
  const [knowledgeQuery, setKnowledgeQuery] = useState("Sovereign Architecture");
  const [fileName, setFileName] = useState("deliverable_notes.md");
  const [fileContent, setFileContent] = useState("# Sovereign Note\nVerified inside atomic MinIO bucket.");
  const [toolFilter, setToolFilter] = useState("");
  const [orKey1, setOrKey1] = useState("");
  const [orKey2, setOrKey2] = useState("");
  const [oblitKey, setOblitKey] = useState("");
  const [compKey, setCompKey] = useState("");

  const slug = tabSpec.slug;

  const chatHistoryQuery = useQuery({
    queryKey: ["tab-chat", slug],
    queryFn: () => apiClient.getChatHistory(slug),
  });

  const agentsQuery = useQuery({
    queryKey: ["tab-agents", slug],
    queryFn: () => apiClient.getTabAgents(slug),
  });

  const openTasksQuery = useQuery({
    queryKey: ["tab-open-tasks", slug],
    queryFn: () => apiClient.getOpenTasks(slug),
  });

  const completedTasksQuery = useQuery({
    queryKey: ["tab-completed-tasks", slug],
    queryFn: () => apiClient.getCompletedTasks(slug),
  });

  const trainingQuery = useQuery({
    queryKey: ["tab-training", slug],
    queryFn: () => apiClient.getTrainingDocs(slug),
  });

  const knowledgeMut = useMutation({
    mutationFn: (q: string) => apiClient.queryKnowledge(slug, q),
  });

  const filesQuery = useQuery({
    queryKey: ["tab-files", slug],
    queryFn: () => apiClient.getTabFiles(slug),
  });

  const toolsQuery = useQuery({
    queryKey: ["tab-tools", slug],
    queryFn: () => apiClient.getTabTools(slug),
  });

  const outputsQuery = useQuery({
    queryKey: ["tab-outputs", slug],
    queryFn: () => apiClient.getTabOutputs(slug),
  });

  const settingsQuery = useQuery({
    queryKey: ["tab-settings", slug],
    queryFn: () => apiClient.getTabSettings(slug),
  });

  const vaultKeysQuery = useQuery({
    queryKey: ["vault-llm-keys"],
    queryFn: apiClient.getVaultKeyStatus,
  });

  const sealVaultKeysMut = useMutation({
    mutationFn: () =>
      apiClient.sealVaultKeys({
        openrouter_key_1: orKey1,
        openrouter_key_2: orKey2,
        obliteratus_api_key: oblitKey,
        composio_api_key: compKey,
      }),
    onSuccess: () => {
      setOrKey1("");
      setOrKey2("");
      setOblitKey("");
      setCompKey("");
      void queryClient.invalidateQueries({ queryKey: ["vault-llm-keys"] });
    },
  });

  const sendChatMut = useMutation({
    mutationFn: () =>
      apiClient.sendChat(slug, {
        message: chatInput,
        preferred_model_id: preferredModel || null,
        use_hermes_swarm: useHermes,
      }),
    onSuccess: (res) => {
      setChatInput("");
      setLastTurn(res);
      void queryClient.invalidateQueries({ queryKey: ["tab-chat", slug] });
      void queryClient.invalidateQueries({ queryKey: ["tab-completed-tasks", slug] });
      void queryClient.invalidateQueries({ queryKey: ["tab-outputs", slug] });
      void queryClient.invalidateQueries({ queryKey: ["finished"] });
    },
  });

  const runAgentMut = useMutation({
    mutationFn: (agentId: string) => apiClient.runTabAgent(slug, agentId, agentObj),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["tab-completed-tasks", slug] });
      void queryClient.invalidateQueries({ queryKey: ["finished"] });
    },
  });

  const createTaskMut = useMutation({
    mutationFn: () => apiClient.createOpenTask(slug, taskTitle, taskPrompt, "queued"),
    onSuccess: () => {
      setTaskTitle("");
      setTaskPrompt("");
      void queryClient.invalidateQueries({ queryKey: ["tab-open-tasks", slug] });
    },
  });

  const patchTaskMut = useMutation({
    mutationFn: ({ id, state }: { id: string; state: TaskState }) =>
      apiClient.updateTaskState(slug, id, state),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["tab-open-tasks", slug] });
      void queryClient.invalidateQueries({ queryKey: ["tab-completed-tasks", slug] });
      void queryClient.invalidateQueries({ queryKey: ["tab-outputs", slug] });
    },
  });

  const ingestTrainMut = useMutation({
    mutationFn: () => apiClient.ingestTrainingDoc(slug, trainTitle, trainContent, `tab://${slug}/training`),
    onSuccess: () => {
      setTrainTitle("");
      setTrainContent("");
      void queryClient.invalidateQueries({ queryKey: ["tab-training", slug] });
    },
  });

  const uploadFileMut = useMutation({
    mutationFn: () => apiClient.uploadTabFile(slug, fileName, fileContent, "finished"),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["tab-files", slug] });
    },
  });

  const execToolMut = useMutation({
    mutationFn: (toolId: string) => apiClient.executeTabTool(slug, toolId, "run"),
  });

  const saveSettingsMut = useMutation({
    mutationFn: (patch: {
      equip_sandbox_all?: boolean;
      hermes_enabled?: boolean;
      flags?: Record<string, boolean>;
    }) => apiClient.saveTabSettings(slug, patch),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["tab-settings", slug] });
      void queryClient.invalidateQueries({ queryKey: ["healthz"] });
    },
  });

  const headerAccentClass =
    tabSpec.accent === "magenta"
      ? "border-fuchsia-600 text-fuchsia-600"
      : tabSpec.accent === "turquoise"
      ? "border-teal-600 text-teal-600"
      : "border-orange-600 text-orange-600";

  return (
    <main className="min-w-0 flex-1 bg-white p-5">
      {/* Editorial Chapter Banner */}
      <div className={`mb-4 border-l-4 pl-4 ${headerAccentClass}`}>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="font-mono text-[11px] font-bold uppercase tracking-widest">
            {tabSpec.chapter}
          </span>
          <div className="flex items-center gap-2">
            <span className="rounded border border-neutral-300 bg-neutral-50 px-2 py-0.5 font-mono text-[11px] text-black">
              Best LLM: <strong>{tabSpec.best_llm}</strong>
            </span>
            <CopyButton value={tabSpec.router_logic} label="COPY ROUTER RULE" />
          </div>
        </div>
        <h2 className="mt-1 text-xl font-extrabold text-black">{tabSpec.title}</h2>
        <p className="mt-0.5 text-xs text-neutral-800">{tabSpec.purpose}</p>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {tabSpec.top_tools.map((tool) => (
            <span
              key={tool}
              className="rounded border border-neutral-300 bg-white px-2 py-0.5 font-mono text-[10px] font-semibold text-neutral-800"
            >
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* Specialized Domain Power Studios */}
      {slug === "engineering" && <EngineeringStudio />}
      {(slug === "images" || slug === "fashion") && <ImageDirectorStudio />}
      {slug === "video" && <VideoStitchStudio />}
      {slug === "music" && <VocalTuningStudio />}
      {(slug === "security" || slug === "passport") && <SecurityKycStudio />}

      {/* Uniform 10-Section Grammar Navigation */}
      <div className="mb-4 flex flex-wrap gap-1.5 border-b-2 border-neutral-900 pb-3">
        {GRAMMAR_SECTIONS.map((sec) => {
          const active = activeSection === sec.id;
          return (
            <button
              key={sec.id}
              type="button"
              onClick={() => setActiveSection(sec.id)}
              className={`rounded border px-3 py-1.5 font-mono text-[11px] font-bold transition ${
                active
                  ? "border-black bg-black text-white"
                  : "border-neutral-300 bg-white text-black hover:border-neutral-900"
              }`}
            >
              {sec.label}
            </button>
          );
        })}
      </div>

      {/* SECTION 1: CHAT */}
      {activeSection === "chat" && (
        <div className="space-y-4">
          <div className="flex flex-wrap items-center gap-3 rounded border border-neutral-300 bg-neutral-50 p-3">
            <div className="flex items-center gap-2">
              <span className="font-mono text-[11px] font-bold text-fuchsia-600">LLM Override (205+):</span>
              <select
                value={preferredModel}
                onChange={(e) => setPreferredModel(e.target.value)}
                className="max-w-xs rounded border border-neutral-300 bg-white px-2.5 py-1 font-mono text-[11px]"
              >
                <option value="">Auto Priority Router ({tabSpec.best_llm})</option>
                {models.slice(0, 65).map((m) => (
                  <option key={m.id} value={m.id}>
                    [{m.tierCode} | {m.guardrail}] {m.canonicalName}
                  </option>
                ))}
              </select>
            </div>
            <label className="flex items-center gap-1.5 font-mono text-[11px] font-semibold text-black">
              <input
                type="checkbox"
                checked={useHermes}
                onChange={(e) => setUseHermes(e.target.checked)}
              />
              Hermes Swarm Specialist
            </label>
          </div>

          {lastTurn && (
            <div className="rounded border-2 border-teal-600 bg-white p-3 font-mono text-[11px]">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="font-bold text-teal-700">
                  Selected: {lastTurn.router_decision.selected_model.canonicalName} (Score:{" "}
                  {lastTurn.router_decision.score}) | Sandbox: {lastTurn.sandbox.sandbox_id}
                </span>
                <button
                  type="button"
                  onClick={() => openSandboxDrawer("finished", lastTurn.sandbox.sandbox_id)}
                  className="rounded border border-fuchsia-600 bg-fuchsia-600 px-2.5 py-0.5 text-white"
                >
                  Inspect Finished Sandbox
                </button>
              </div>
              <div className="mt-1 text-neutral-700">{lastTurn.router_decision.reasoning}</div>
            </div>
          )}

          <div className="max-h-[420px] space-y-3 overflow-y-auto rounded border border-neutral-300 bg-white p-4">
            {(chatHistoryQuery.data ?? []).length === 0 ? (
              <div className="font-mono text-[11px] text-neutral-600">
                Ready in [{tabSpec.title}]. Every turn creates an isolated sandbox equipped with Qdrant 768d, MinIO
                atomic S3, Vault HSM, and Postgres task audit.
              </div>
            ) : (
              chatHistoryQuery.data?.map((msg) => (
                <div
                  key={msg.id}
                  className={`rounded border p-3 ${
                    msg.role === "user"
                      ? "border-neutral-300 bg-neutral-50"
                      : "border-neutral-900 bg-white"
                  }`}
                >
                  <div className="mb-1.5 flex items-center justify-between">
                    <span className="font-mono text-[11px] font-bold uppercase text-fuchsia-600">
                      {msg.role} | {msg.model_id} | {msg.sandbox_id}
                    </span>
                    <CopyButton value={msg.content} />
                  </div>
                  <pre className="whitespace-pre-wrap font-mono text-[11px] text-black">{msg.content}</pre>
                </div>
              ))
            )}
          </div>

          <form
            className="flex gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              if (chatInput.trim()) {
                sendChatMut.mutate();
              }
            }}
          >
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder={`Send directive to ${tabSpec.title} (delivered in one unified batch)...`}
              className="flex-1 rounded border-2 border-neutral-900 px-3 py-2 text-xs text-black focus:border-fuchsia-600 focus:outline-none"
            />
            <button
              type="submit"
              disabled={sendChatMut.isPending || !chatInput.trim()}
              className="rounded border-2 border-black bg-black px-5 py-2 text-xs font-extrabold uppercase tracking-wider text-white hover:bg-neutral-800 disabled:opacity-50"
            >
              {sendChatMut.isPending ? "Executing..." : "Execute Batch"}
            </button>
          </form>
        </div>
      )}

      {/* SECTION 2: AGENTS */}
      {activeSection === "agents" && (
        <div className="space-y-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={agentObj}
              onChange={(e) => setAgentObj(e.target.value)}
              className="flex-1 rounded border border-neutral-300 px-3 py-1.5 text-xs"
              placeholder="Objective for agent execution..."
            />
          </div>
          {runAgentMut.data && (
            <div className="flex items-center justify-between rounded border-2 border-teal-600 bg-neutral-50 p-3 font-mono text-[11px]">
              <span>
                [{runAgentMut.data.agent_name}] Completed in {runAgentMut.data.sandbox_id} -&gt;{" "}
                {runAgentMut.data.finished_path}
              </span>
              <CopyButton value={runAgentMut.data.output} />
            </div>
          )}
          <div className="grid gap-3 md:grid-cols-2">
            {(agentsQuery.data ?? []).map((a) => (
              <div key={a.id} className="rounded border border-neutral-300 bg-white p-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-extrabold text-black">{a.name}</span>
                  <span
                    className={`rounded px-2 py-0.5 font-mono text-[10px] font-bold ${
                      a.enabled ? "bg-teal-100 text-teal-800" : "bg-neutral-200 text-neutral-700"
                    }`}
                  >
                    {a.status.toUpperCase()} ({a.cadence})
                  </span>
                </div>
                <div className="mt-1 font-mono text-[11px] text-fuchsia-700">
                  Primary LLM: {a.primary_llm} | Flag: {a.turn_off_flag}
                </div>
                <p className="mt-1 text-xs text-neutral-700">{a.description}</p>
                <div className="mt-2 flex justify-end">
                  <button
                    type="button"
                    onClick={() => runAgentMut.mutate(a.id)}
                    className="rounded border border-black bg-black px-3 py-1 font-mono text-[11px] font-bold text-white hover:bg-neutral-800"
                  >
                    Run in Sandbox
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SECTION 3: OPEN TASKS */}
      {activeSection === "open-tasks" && (
        <div className="space-y-4">
          <form
            className="grid gap-2 rounded border border-neutral-300 bg-neutral-50 p-3 md:grid-cols-3"
            onSubmit={(e) => {
              e.preventDefault();
              if (taskTitle.trim()) {
                createTaskMut.mutate();
              }
            }}
          >
            <input
              type="text"
              value={taskTitle}
              onChange={(e) => setTaskTitle(e.target.value)}
              placeholder="New task title..."
              className="rounded border border-neutral-300 bg-white px-3 py-1.5 text-xs"
            />
            <input
              type="text"
              value={taskPrompt}
              onChange={(e) => setTaskPrompt(e.target.value)}
              placeholder="Detailed sandbox specification..."
              className="rounded border border-neutral-300 bg-white px-3 py-1.5 text-xs"
            />
            <button
              type="submit"
              className="rounded bg-orange-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-orange-700"
            >
              Queue Sandbox Task
            </button>
          </form>

          <div className="space-y-2">
            {(openTasksQuery.data ?? []).map((t) => (
              <div
                key={t.id}
                className="flex flex-wrap items-center justify-between gap-2 rounded border border-neutral-300 p-3"
              >
                <div>
                  <div className="text-xs font-bold text-black">{t.title}</div>
                  <div className="font-mono text-[11px] text-neutral-700">
                    {t.id} | Sandbox: {t.sandbox_id} | State: <strong>{t.state}</strong> | Model: {t.model_used}
                  </div>
                </div>
                <select
                  value={t.state}
                  onChange={(e) => patchTaskMut.mutate({ id: t.id, state: e.target.value as TaskState })}
                  className="rounded border border-neutral-400 bg-white px-2.5 py-1 font-mono text-[11px]"
                >
                  {ALL_TASK_STATES.map((st) => (
                    <option key={st} value={st}>
                      {st}
                    </option>
                  ))}
                </select>
              </div>
            ))}
            {(openTasksQuery.data ?? []).length === 0 && (
              <div className="font-mono text-[11px] text-neutral-600">No open tasks queued in this tab.</div>
            )}
          </div>
        </div>
      )}

      {/* SECTION 4: COMPLETED TASKS */}
      {activeSection === "completed-tasks" && (
        <div className="space-y-2">
          {(completedTasksQuery.data ?? []).map((t) => (
            <div key={t.id} className="rounded border border-neutral-300 bg-white p-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <div className="text-xs font-bold text-black">{t.title}</div>
                  <div className="font-mono text-[11px] text-teal-700">
                    {t.finished_uri} | OTS: {t.opentimestamps_proof} | IPFS: {t.ipfs_cid}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => openSandboxDrawer("finished", t.sandbox_id)}
                    className="rounded bg-fuchsia-600 px-2.5 py-1 font-mono text-[11px] font-bold text-white"
                  >
                    Open Dossier
                  </button>
                  <CopyButton value={t.ipfs_cid} label="COPY CID" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* SECTION 5: TRAINING */}
      {activeSection === "training" && (
        <div className="space-y-4">
          <form
            className="space-y-2 rounded border border-neutral-300 bg-neutral-50 p-3"
            onSubmit={(e) => {
              e.preventDefault();
              if (trainTitle.trim() && trainContent.trim()) {
                ingestTrainMut.mutate();
              }
            }}
          >
            <div className="font-mono text-[11px] font-bold text-fuchsia-600">
              INGEST CORPUS INTO QDRANT 768D COSINE + MINIO ATOMIC S3
            </div>
            <input
              type="text"
              value={trainTitle}
              onChange={(e) => setTrainTitle(e.target.value)}
              placeholder="Corpus Document Title"
              className="w-full rounded border border-neutral-300 bg-white px-3 py-1.5 text-xs"
            />
            <textarea
              value={trainContent}
              onChange={(e) => setTrainContent(e.target.value)}
              placeholder="Paste legal statute, CAD spec, research paper, or domain SOP..."
              rows={3}
              className="w-full rounded border border-neutral-300 bg-white px-3 py-1.5 text-xs"
            />
            <button
              type="submit"
              className="rounded bg-fuchsia-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-fuchsia-700"
            >
              Embed 768d Cosine & Archive
            </button>
          </form>

          <div className="space-y-2">
            {(trainingQuery.data ?? []).map((doc) => (
              <div key={doc.doc_id} className="rounded border border-neutral-200 p-2.5 font-mono text-[11px]">
                <strong>{doc.title}</strong> | dim={doc.vector_dim} | collection={doc.qdrant_collection} |{" "}
                {doc.minio_uri}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SECTION 6: KNOWLEDGE */}
      {activeSection === "knowledge" && (
        <div className="space-y-4">
          <form
            className="flex gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              knowledgeMut.mutate(knowledgeQuery);
            }}
          >
            <input
              type="text"
              value={knowledgeQuery}
              onChange={(e) => setKnowledgeQuery(e.target.value)}
              className="flex-1 rounded border border-neutral-300 px-3 py-1.5 text-xs"
              placeholder="Semantic Cosine query across 768d Qdrant vectors..."
            />
            <button
              type="submit"
              className="rounded bg-teal-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-teal-700"
            >
              Search Qdrant 768d
            </button>
          </form>

          <div className="space-y-2">
            {(knowledgeMut.data?.hits ?? []).map((hit) => (
              <div key={hit.doc_id} className="rounded border border-neutral-300 p-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-black">{hit.title}</span>
                  <span className="font-mono text-[11px] font-bold text-teal-700">
                    Cosine Score: {hit.cosine_score}
                  </span>
                </div>
                <p className="mt-1 text-xs text-neutral-700">{hit.excerpt}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SECTION 7: FILES */}
      {activeSection === "files" && (
        <div className="space-y-4">
          <form
            className="grid gap-2 rounded border border-neutral-300 bg-neutral-50 p-3 md:grid-cols-3"
            onSubmit={(e) => {
              e.preventDefault();
              uploadFileMut.mutate();
            }}
          >
            <input
              type="text"
              value={fileName}
              onChange={(e) => setFileName(e.target.value)}
              className="rounded border border-neutral-300 bg-white px-3 py-1.5 font-mono text-xs"
            />
            <input
              type="text"
              value={fileContent}
              onChange={(e) => setFileContent(e.target.value)}
              className="rounded border border-neutral-300 bg-white px-3 py-1.5 text-xs"
            />
            <button
              type="submit"
              className="rounded bg-black px-4 py-1.5 text-xs font-bold text-white hover:bg-neutral-800"
            >
              Atomic MinIO Write (Temp -&gt; Rename)
            </button>
          </form>

          <div className="space-y-1.5">
            {(filesQuery.data ?? []).map((f) => (
              <div
                key={`${f.bucket}:${f.object_key}`}
                className="flex flex-wrap items-center justify-between gap-2 rounded border border-neutral-200 p-2 font-mono text-[11px]"
              >
                <span>
                  s3://{f.bucket}/{f.object_key} ({f.size_bytes} B | sha256:{f.sha256.slice(0, 12)})
                </span>
                <CopyButton value={`s3://${f.bucket}/${f.object_key}`} />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SECTION 8: TOOLS */}
      {activeSection === "tools" && (
        <div className="space-y-3">
          <input
            type="text"
            value={toolFilter}
            onChange={(e) => setToolFilter(e.target.value)}
            placeholder="Filter lazy-loaded tools by name or category..."
            className="w-full rounded border border-neutral-300 px-3 py-1.5 text-xs"
          />
          {execToolMut.data && (
            <div className="flex items-center justify-between rounded border-2 border-orange-600 bg-neutral-50 p-2.5 font-mono text-[11px]">
              <span>
                {execToolMut.data.summary} -&gt; {execToolMut.data.artifact_path}
              </span>
              <CopyButton value={execToolMut.data.artifact_path} />
            </div>
          )}
          <div className="grid gap-2 md:grid-cols-2 lg:grid-cols-3">
            {(toolsQuery.data ?? [])
              .filter(
                (t) =>
                  !toolFilter ||
                  t.name.toLowerCase().includes(toolFilter.toLowerCase()) ||
                  t.category.toLowerCase().includes(toolFilter.toLowerCase())
              )
              .map((t) => (
                <div key={t.id} className="flex items-center justify-between rounded border border-neutral-200 p-2.5">
                  <div className="min-w-0 pr-2">
                    <div className="truncate text-xs font-bold text-black">{t.name}</div>
                    <div className="font-mono text-[10px] text-neutral-600">
                      [{t.category}] stage:{t.docker_stage} | lazy:{String(t.lazy_loaded)}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => execToolMut.mutate(t.id)}
                    className="rounded border border-amber-600 bg-amber-400 px-2.5 py-1 font-mono text-[10px] font-bold text-black hover:bg-amber-500"
                  >
                    RUN
                  </button>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* SECTION 9: OUTPUTS */}
      {activeSection === "outputs" && (
        <div className="space-y-2">
          {(outputsQuery.data ?? []).map((o) => (
            <div
              key={o.output_id}
              className="flex flex-wrap items-center justify-between gap-2 rounded border border-neutral-300 p-3"
            >
              <div>
                <div className="text-xs font-bold text-black">{o.title}</div>
                <div className="font-mono text-[11px] text-neutral-700">
                  {o.batch_format} | {o.uri} | {o.opentimestamps_proof}
                </div>
              </div>
              <CopyButton value={o.uri} label="COPY S3 URI" />
            </div>
          ))}
          {(outputsQuery.data ?? []).length === 0 && (
            <div className="font-mono text-[11px] text-neutral-600">
              Completed unified single-batch outputs appear here automatically.
            </div>
          )}
        </div>
      )}

      {/* SECTION 10: SETTINGS & GRANULAR TURN-OFF FLAGS */}
      {activeSection === "settings" && settingsQuery.data && (
        <div className="space-y-4">
          <div className="rounded border-2 border-orange-600 bg-white p-4">
            <h4 className="mb-1 font-mono text-xs font-bold uppercase text-orange-600">
              Browser Secret Vault (Zero SSH / Zero Terminal Needed)
            </h4>
            <p className="mb-3 text-xs text-neutral-700">
              Paste your OpenRouter key(s) right here in your browser. Keys are encrypted immediately inside HashiCorp
              Vault HSM transit seal and never shown again in plaintext. Active OpenRouter keys:{" "}
              <strong>{vaultKeysQuery.data?.configured_openrouter_keys ?? 0}</strong>
              {vaultKeysQuery.data && vaultKeysQuery.data.masked_slots.length > 0
                ? ` (${vaultKeysQuery.data.masked_slots.join(", ")})`
                : ""}
            </p>
            <form
              className="grid gap-2 md:grid-cols-2"
              onSubmit={(e) => {
                e.preventDefault();
                sealVaultKeysMut.mutate();
              }}
            >
              <input
                type="password"
                value={orKey1}
                onChange={(e) => setOrKey1(e.target.value)}
                placeholder="OPENROUTER_API_KEY_1 (sk-or-v1-...)"
                className="rounded border border-neutral-300 px-3 py-1.5 font-mono text-xs"
              />
              <input
                type="password"
                value={orKey2}
                onChange={(e) => setOrKey2(e.target.value)}
                placeholder="OPENROUTER_API_KEY_2 (optional failover slot)"
                className="rounded border border-neutral-300 px-3 py-1.5 font-mono text-xs"
              />
              <input
                type="password"
                value={oblitKey}
                onChange={(e) => setOblitKey(e.target.value)}
                placeholder="OBLITERATUS_API_KEY (optional)"
                className="rounded border border-neutral-300 px-3 py-1.5 font-mono text-xs"
              />
              <input
                type="password"
                value={compKey}
                onChange={(e) => setCompKey(e.target.value)}
                placeholder="COMPOSIO_API_KEY (optional SaaS connectors)"
                className="rounded border border-neutral-300 px-3 py-1.5 font-mono text-xs"
              />
              <div className="md:col-span-2">
                <button
                  type="submit"
                  disabled={sealVaultKeysMut.isPending}
                  className="rounded border border-amber-600 bg-amber-400 px-4 py-1.5 font-mono text-[11px] font-bold text-black hover:bg-amber-500"
                >
                  {sealVaultKeysMut.isPending ? "Sealing in Vault HSM..." : "SEAL KEYS IN VAULT HSM"}
                </button>
              </div>
            </form>
          </div>

          <div className="rounded border border-neutral-300 p-4">
            <h4 className="mb-3 font-mono text-xs font-bold uppercase text-fuchsia-600">
              Per-Tab Sandbox & Hermes Configuration ({slug})
            </h4>
            <div className="flex flex-wrap gap-6 text-xs">
              <label className="flex items-center gap-2 font-semibold">
                <input
                  type="checkbox"
                  checked={settingsQuery.data.equip_sandbox_all}
                  onChange={(e) => saveSettingsMut.mutate({ equip_sandbox_all: e.target.checked })}
                />
                Equip Sandbox With Everything (Qdrant + MinIO + Vault + Tools)
              </label>
              <label className="flex items-center gap-2 font-semibold">
                <input
                  type="checkbox"
                  checked={settingsQuery.data.hermes_enabled}
                  onChange={(e) => saveSettingsMut.mutate({ hermes_enabled: e.target.checked })}
                />
                Enable Hermes Extensions on Tab
              </label>
            </div>
          </div>

          <div className="rounded border border-neutral-300 p-4">
            <h4 className="mb-3 font-mono text-xs font-bold uppercase text-teal-600">
              Global Sovereign Turn-Off Switches (Default True, Toggleable Live Without Crash)
            </h4>
            <div className="grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
              {Object.entries(settingsQuery.data.flags).map(([flagKey, enabled]) => (
                <label
                  key={flagKey}
                  className="flex cursor-pointer items-center justify-between rounded border border-neutral-200 px-3 py-2 font-mono text-[11px]"
                >
                  <span className="truncate pr-2 font-semibold text-black">{flagKey}</span>
                  <input
                    type="checkbox"
                    checked={enabled}
                    onChange={(e) =>
                      saveSettingsMut.mutate({
                        flags: { [flagKey]: e.target.checked },
                      })
                    }
                  />
                </label>
              ))}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
