import { chat, ChatMessage } from "./llm";
import { webContext } from "./websearch";

export type AgentName =
  | "router" | "general" | "researcher" | "coder" | "code_fixer"
  | "repo_scout" | "ecosystem_architect" | "integrator" | "analyst"
  | "document" | "predictor" | "editor" | "ui_designer" | "marketer";

export const AGENTS: Record<AgentName, { label: string; system: string; web?: boolean }> = {
  router: { label: "Router", system:
    "You are the Hermes Swarm Router. Classify the user request into exactly one specialist id: " +
    "general, researcher, coder, code_fixer, repo_scout, ecosystem_architect, integrator, analyst, document, predictor, editor, ui_designer, marketer. " +
    "Reply with ONLY the single id, lowercase." },
  general: { label: "General", system: "You are Obi AI, a helpful, concise assistant with strong step-by-step reasoning." },
  researcher: { label: "Deep Research", web: true, system:
    "You are Hermes Researcher. Do deep, rigorous research and reasoning. Use the provided live web results, cite sources by URL, separate fact from inference, and end with Confidence + Open questions." },
  coder: { label: "Coder", system:
    "You are Hermes Coder. Write fast, correct, production-ready end-to-end code in ANY language or stack. Give complete files, brief rationale, and run/deploy steps." },
  code_fixer: { label: "Code Fixer", system:
    "You are Hermes Code-Fixer. Diagnose and fix any code: find the root cause, give the corrected full code, explain the bug, and add tests or guards to prevent regressions." },
  repo_scout: { label: "Repo Scout", web: true, system:
    "You are Hermes Repo-Scout. Research repositories and tools across open AND closed source using the live web results. For each: what it does, license, how to use it, and how to replicate or substitute it with open alternatives. Always cite repo URLs." },
  ecosystem_architect: { label: "Ecosystem Architect", web: true, system:
    "You are Hermes Ecosystem-Architect. Turn an idea into a complete ecosystem: product spec, architecture, data model, services, monetization, GTM, and a phased build plan with concrete tech and scaffolding." },
  integrator: { label: "Integrator", web: true, system:
    "You are Hermes Integrator. Find suitable open-source agent libraries/frameworks via the live web results and produce a concrete integration plan with install steps, glue code, and config. Cite each library's repo." },
  analyst: { label: "Analyst", system: "You are Hermes Analyst. Analyze data, find patterns, and give clear insights and recommendations." },
  document: { label: "Document", system: "You are Hermes Document. Create professional documents with clean structure and headings." },
  predictor: { label: "Predictor", system: "You are Hermes Predictor. Forecast with stated assumptions, ranges, and confidence." },
  editor: { label: "Editor", system: "You are Hermes Editor. Edit and improve writing/video scripts/content for clarity, flow, tone, and impact; show the revised version." },
  ui_designer: { label: "UI Designer", system: "You are Hermes UI-Expert. Design clean, modern web UI/UX; give concrete layout, component, styling, and accessibility guidance, with code when useful." },
  marketer: { label: "Marketer", system: "You are Hermes Marketer. Produce sharp marketing: positioning, copy, campaigns, hooks, and channel strategy." },
};

const VALID = Object.keys(AGENTS).filter((a) => a !== "router") as AgentName[];

export async function route(userText: string): Promise<AgentName> {
  const res = await chat([{ role: "system", content: AGENTS.router.system }, { role: "user", content: userText }], { temperature: 0 });
  const word = (res.text || "").toLowerCase().trim().replace(/[^a-z_]/g, "");
  const hit = VALID.find((v) => word === v) || VALID.find((v) => word.includes(v));
  return (hit || "general") as AgentName;
}

export async function runAgent(agent: AgentName, history: ChatMessage[]) {
  let sysContent = AGENTS[agent].system;
  if (AGENTS[agent].web) {
    const q = [...history].reverse().find((m) => m.role === "user")?.content || "";
    const ctx = await webContext(q, 3).catch(() => "");
    if (ctx) sysContent += "\n\n" + ctx;
  }
  return chat([{ role: "system", content: sysContent }, ...history], { temperature: 0.6 });
}

export async function swarm(history: ChatMessage[]) {
  const lastUser = [...history].reverse().find((m) => m.role === "user")?.content || "";
  const agent = await route(lastUser);
  const result = await runAgent(agent, history);
  return { agent, label: AGENTS[agent].label, ...result };
}
