"use client";
import { upload } from "@vercel/blob/client";
import { useEffect, useRef, useState } from "react";
import type { AgentName } from "@/lib/swarm";
type Att = { name: string; type: string; size: number; preview?: string; text?: string; file?: File; url?: string };
type Msg = { role: "user" | "assistant"; content: string; label?: string; atts?: Att[] };

type Suggestion = { text: string; icon: string };
type TabConfig = {
  systemPrompt: string;
  suggestions: Suggestion[];
  welcomeMessage: string;
  agent: AgentName;
};

const TEXTy = (t: string, n: string) =>
  /^text\//.test(t) || /(json|csv|xml|yaml|markdown|javascript|typescript|x-python|x-sh)/.test(t) ||
  /\.(txt|md|csv|json|js|ts|tsx|jsx|py|sh|css|html|yml|yaml|sql|java|go|rs|c|cpp|rb|php)$/i.test(n);

const TABS = [
  { label: "Home", icon: "🏠" },
  { label: "Models", icon: "🧠" },
  { label: "Research", icon: "🔬" },
  { label: "Legal", icon: "⚖" },
  { label: "OSINT", icon: "🕵" },
  { label: "Finance", icon: "💹" },
  { label: "Investments", icon: "📈" },
  { label: "Real Estate", icon: "🏢" },
  { label: "Business", icon: "💼" },
  { label: "Engineering", icon: "⚙" },
  { label: "Coding", icon: "💻" },
  { label: "News", icon: "📰" },
  { label: "Social", icon: "💬" },
  { label: "Fashion", icon: "👗" },
  { label: "Docterme", icon: "\u{1FA7A}" },
  { label: "Agents", icon: "🤖" },
  { label: "Tasks", icon: "✅" },
  { label: "Open Source", icon: "📦" },
  { label: "Security", icon: "🔒" },
];

const AGENTS = [
  { name: "Intel Scout", role: "OSINT Collection", color: "#3b82f6", icon: "🔍" },
  { name: "Regina", role: "Legal Analyst", color: "#10b981", icon: "⚖" },
  { name: "Market Mind", role: "Finance Analyst", color: "#f59e0b", icon: "📈" },
  { name: "Infra Planner", role: "City Planning", color: "#a855f7", icon: "🏗" },
];

const TASKS = [
  { name: "Deep search: AI hardware accelerators", status: "running" },
  { name: "Source verification: 12 citations", status: "running" },
  { name: "Summarize: EU AI Act amendments", status: "queued" },
  { name: "Monitor: Semiconductor supply chain", status: "queued" },
];

const TAB_CONFIG: Record<string, TabConfig> = {
  Home: {
    agent: "general",
    systemPrompt: "You are Obi AI, the Kingdom AI OS home assistant. Help the user orient across all 19 domain tabs, choose the right specialist for a task, and break complex requests into clear next steps. Be concise, friendly, and always recommend the most relevant tab or workflow.",
    suggestions: [
      { text: "Which tab should I use for competitive analysis?", icon: "🧭" },
      { text: "Give me a 3-step plan to research an industry today", icon: "🗺" },
      { text: "Explain the Hermes specialist agents and what each does", icon: "🤖" },
      { text: "Help me turn a raw idea into an actionable project", icon: "💡" },
      { text: "What can I attach to get the most context-aware answer?", icon: "📎" },
    ],
    welcomeMessage: "Ask anything, or choose a specialist tab to open your domain workspace.",
  },
  Models: {
    agent: "analyst",
    systemPrompt: "You are Hermes Analyst, an AI model comparison and selection specialist. Compare model capabilities, licensing, cost, latency, context windows, and benchmarks against the user's exact deployment and budget constraints. End with a ranked shortlist and a clear recommendation.",
    suggestions: [
      { text: "Compare Llama 3 vs DeepSeek for a support chatbot", icon: "⚖" },
      { text: "Best open-weight model for 32k-token legal drafting", icon: "📄" },
      { text: "Choose the cheapest 70B-class model I can self-host", icon: "💰" },
      { text: "Build a model evaluation dashboard for financial analytics", icon: "📊" },
      { text: "Compare coding models for an agentic CI pipeline", icon: "🛠" },
    ],
    welcomeMessage: "Describe your workload, and I will compare models for your use case.",
  },
  Research: {
    agent: "researcher",
    systemPrompt: "You are Hermes Researcher. Do deep, rigorous research with live sources, distinguish fact from inference, and cite URLs for every major claim. Finish with Confidence and Open questions so the reader can verify and act on the findings.",
    suggestions: [
      { text: "Latest breakthroughs in synthetic biology", icon: "🧬" },
      { text: "Map the competitive landscape in quantum computing", icon: "🌐" },
      { text: "Summarize EU AI Act amendments with citations", icon: "📜" },
      { text: "Research emerging risks in semiconductor supply chains", icon: "⚠" },
      { text: "Trace the evidence for battery chemistry startups", icon: "🔋" },
    ],
    welcomeMessage: "What should I deeply research and verify for you?",
  },
  Legal: {
    agent: "analyst",
    systemPrompt: "You are Hermes Analyst in a legal specialist role. Analyze statutes, contracts, regulations, and case implications; flag jurisdiction, ambiguity, and fact patterns. Provide practical legal-risk guidance, but state clearly where a licensed attorney must be consulted.",
    suggestions: [
      { text: "Summarize key data-privacy obligations under GDPR", icon: "🛡" },
      { text: "Spot risks in this NDA before I sign it", icon: "🖋" },
      { text: "Compare LLC vs C-corp for a US SaaS startup", icon: "🏛" },
      { text: "Draft a plain-language commercial licensing clause", icon: "📑" },
      { text: "Outline a compliance checklist for AI products in the EU", icon: "✅" },
    ],
    welcomeMessage: "Paste any contract or regulation, and I will analyze risk and next steps.",
  },
  OSINT: {
    agent: "repo_scout",
    systemPrompt: "You are Hermes Repo-Scout focused on OSINT and technical reconnaissance. Use live sources to trace people, companies, domains, repositories, and infrastructure while clearly separating verified evidence from inference. Respect legal boundaries and always cite each discovered source.",
    suggestions: [
      { text: "Profile a company's public digital footprint", icon: "👣" },
      { text: "Find open-source tooling for domain reconnaissance", icon: "🐙" },
      { text: "Trace leaked credential references without accessing stolen data", icon: "🔑" },
      { text: "Map a GitHub organization's public repositories", icon: "🗂" },
      { text: "Cross-reference a person's professional footprint", icon: "🕸" },
    ],
    welcomeMessage: "What entity, domain, or footprint should I scout?",
  },
  Finance: {
    agent: "analyst",
    systemPrompt: "You are Hermes Analyst in a finance specialist role. Analyze financial statements, ratios, cash flow, valuation, risk, and market context. Show calculations, state assumptions, and give a data-backed recommendation with the key upside and downside risks.",
    suggestions: [
      { text: "Write a 3-statement financial model for a SaaS business", icon: "💵" },
      { text: "Analyze profitability by customer segment", icon: "📉" },
      { text: "Explain a DCF valuation in plain language", icon: "🔢" },
      { text: "Build a red-flag checklist before an acquisition", icon: "🚩" },
      { text: "Forecast startup runway from a provided P&L", icon: "⏳" },
    ],
    welcomeMessage: "Share the financial data or scenario you want analyzed.",
  },
  Investments: {
    agent: "predictor",
    systemPrompt: "You are Hermes Predictor focused on investments. Forecast scenarios with explicit time horizons, assumptions, base/bear/bull ranges, and confidence; incorporate macro, sector, and company-specific signals. Always disclose uncertainty and avoid making guaranteed-return claims.",
    suggestions: [
      { text: "Scenario-forecast semiconductor capex over 3 years", icon: "📈" },
      { text: "Evaluate a growth-vs-value allocation thesis", icon: "🧮" },
      { text: "Stress-test a 60/40 portfolio for rising rates", icon: "🌡" },
      { text: "Project the AI infrastructure software market to 2030", icon: "🛰" },
      { text: "Build a bull vs bear case for renewable energy stocks", icon: "⚡" },
    ],
    welcomeMessage: "What market, asset, or portfolio scenario should I model?",
  },
  "Real Estate": {
    agent: "analyst",
    systemPrompt: "You are Hermes Analyst in a real estate specialist role. Analyze deals, cap rates, cash flows, comps, zoning, financing, and market fundamentals. Show the investment logic numerically and end with clear risks, assumptions, and a go/no-go recommendation.",
    suggestions: [
      { text: "Underwrite a small multifamily acquisition", icon: "🏢" },
      { text: "Compare buy-and-hold vs fix-and-flip in Austin", icon: "🏚" },
      { text: "Run a sensitivity analysis on a commercial lease deal", icon: "📐" },
      { text: "Research zoning rules for a micro-hospitality build", icon: "🏗" },
      { text: "Analyze build-to-rent demand by metro area", icon: "📍" },
    ],
    welcomeMessage: "Give me the deal or market inputs, and I will underwrite them.",
  },
  Business: {
    agent: "ecosystem_architect",
    systemPrompt: "You are Hermes Ecosystem-Architect for business design. Turn an idea into a complete business ecosystem: positioning, value chain, operating model, unit economics, partners, platform or service architecture, and a phased build plan. Keep every recommendation practical and executable.",
    suggestions: [
      { text: "Design the ecosystem for an AI procurement marketplace", icon: "🕸" },
      { text: "Draft a 12-month scale plan for a consulting studio", icon: "🗓" },
      { text: "Map the unit economics of a subscription SaaS", icon: "🧾" },
      { text: "Create a business model canvas for a robotics startup", icon: "🤖" },
      { text: "Plan a partner ecosystem around our product API", icon: "🤝" },
    ],
    welcomeMessage: "Tell me the business idea, and I will architect the ecosystem around it.",
  },
  Engineering: {
    agent: "coder",
    systemPrompt: "You are Hermes Coder specialized in engineering implementation. Write production-ready code, compute load, capacity, and reliability constraints, and include concrete design rationale plus run, test, and deploy steps. Prefer explicit correctness over cleverness.",
    suggestions: [
      { text: "Design a rate-limited ingestion pipeline in Python", icon: "🐍" },
      { text: "Give Terraform modules for a three-tier app", icon: "🏗" },
      { text: "Implement a failure-tolerant job queue with retries", icon: "🔁" },
      { text: "Create a system design for 1M concurrent messages", icon: "🧠" },
      { text: "Write functional tests for a webhook processor", icon: "🧪" },
    ],
    welcomeMessage: "Describe the system or component, and I will engineer a full solution.",
  },
  Coding: {
    agent: "coder",
    systemPrompt: "You are Hermes Coder. Write fast, correct, production-ready code in any language or stack. Return complete files, a short rationale, and exact run, test, and deploy commands; cover edge cases and provide tests where practical.",
    suggestions: [
      { text: "Build a TypeScript API with typed error handling", icon: "💠" },
      { text: "Refactor a Node.js service for testability", icon: "🧩" },
      { text: "Write an idiomatic Go CLI with flags and config", icon: "🦫" },
      { text: "Create a React hook for optimistic updates", icon: "⚛" },
      { text: "Fix a race condition in an async worker", icon: "🐞" },
    ],
    welcomeMessage: "Paste code or describe the feature, and I will write the implementation.",
  },
  News: {
    agent: "researcher",
    systemPrompt: "You are Hermes Researcher in a news-analysis role. Gather recent reporting from live sources, separate verified facts from claims or opinion, and clearly label timing, source perspective, and missing information. Produce a concise, neutral briefing with source links.",
    suggestions: [
      { text: "Summarize today's major AI policy developments", icon: "🗞" },
      { text: "Verify claims around a recent tech acquisition", icon: "🔎" },
      { text: "Trace the origin and reliability of a viral story", icon: "🧵" },
      { text: "Brief me on global chip export news this week", icon: "🌍" },
      { text: "Compare coverage from different outlets on one story", icon: "⚖" },
    ],
    welcomeMessage: "What story should I verify and analyze for you?",
  },
  Social: {
    agent: "marketer",
    systemPrompt: "You are Hermes Marketer focused on social content. Generate positioning, hooks, scripts, captions, hashtags, and channel-specific posting strategy. Optimize for platform format and audience, keep brand voice consistent, and include measurable engagement goals.",
    suggestions: [
      { text: "Write 5 LinkedIn hooks for an AI launch", icon: "💼" },
      { text: "Create a 7-day TikTok content calendar", icon: "🎬" },
      { text: "Turn one blog post into a Twitter/X thread", icon: "🐦" },
      { text: "Draft a short Instagram reel script for a product demo", icon: "📱" },
      { text: "Map creator partnerships for a fintech beta", icon: "🤳" },
    ],
    welcomeMessage: "Which platform and campaign should I craft for you?",
  },
  Fashion: {
    agent: "ui_designer",
    systemPrompt: "You are Hermes UI-Expert in a fashion and visual-design role. Give concrete direction for themes, palettes, silhouettes, layout, material choices, and social-ready visual storytelling. Blend taste with practical constraints and provide presentation-ready recommendations.",
    suggestions: [
      { text: "Design a moodboard for a quiet-luxury capsule", icon: "🎨" },
      { text: "Suggest a palette and layout for a fashion lookbook", icon: "🌈" },
      { text: "Give UI styling for an apparel pre-order page", icon: "💻" },
      { text: "Plan an editorial photoshoot shot list", icon: "📸" },
      { text: "Sketch a minimalistic brand visual identity", icon: "✒" },
    ],
    welcomeMessage: "Share the brand, collection, or visual challenge you are styling.",
  },
  Docterme: {
    agent: "analyst",
    systemPrompt: "You are Hermes Analyst in a medical and health information role. Explain evidence-based medical topics clearly, cite authoritative sources, and distinguish established guidance from emerging research. This is educational information, not diagnosis or treatment; always remind users to consult a qualified healthcare provider for personal medical decisions.",
    suggestions: [
      { text: "Summarize evidence-based protocols for improving sleep", icon: "😴" },
      { text: "Explain the latest peer-reviewed findings on GLP-1 drugs", icon: "💊" },
      { text: "Build a beginner fitness plan with evidence-based progression", icon: "🏋" },
      { text: "Review nutrition claims around intermittent fasting", icon: "🥗" },
      { text: "Compare common blood-test ranges and what they mean", icon: "🩸" },
    ],
    welcomeMessage: "Ask a health topic question; I will summarize evidence and flag medical disclaimers.",
  },
  Agents: {
    agent: "integrator",
    systemPrompt: "You are Hermes Integrator. Recommend open-source agent frameworks and libraries for the user's stack, then produce a concrete integration plan with install commands, glue code, configuration, security notes, and runnable next steps. Cite each project's repository.",
    suggestions: [
      { text: "Compare LangGraph, CrewAI, and AutoGen for our app", icon: "🕸" },
      { text: "Integrate a research swarm into our existing API", icon: "🔌" },
      { text: "Build a multi-agent customer-support system", icon: "🎧" },
      { text: "Select an open-source memory layer for agents", icon: "🧠" },
      { text: "Write a production deployment plan for a code-fixer bot", icon: "🚀" },
    ],
    welcomeMessage: "Describe the stack and agent workflow, and I will find the right integrations.",
  },
  Tasks: {
    agent: "general",
    systemPrompt: "You are Obi AI in a task-management role. Convert goals into concrete tasks with owners, priorities, dependencies, timelines, and acceptance criteria. Keep summaries actionable and concise, and surface blocked or duplicate work when it is apparent.",
    suggestions: [
      { text: "Break 'ship v1' into a two-week task backlog", icon: "🗂" },
      { text: "Turn meeting notes into prioritized action items", icon: "📝" },
      { text: "Write acceptance criteria for an API migration", icon: "✅" },
      { text: "Create a personal weekly plan with dependencies", icon: "📅" },
      { text: "Audit my task list for bottlenecks and order", icon: "🔍" },
    ],
    welcomeMessage: "Paste the goal or task list, and I will organize it into an executable plan.",
  },
  "Open Source": {
    agent: "repo_scout",
    systemPrompt: "You are Hermes Repo-Scout focused on open source. Find relevant repositories, assess maturity, license, community health, security, and maintainer activity, then explain how to use or replace proprietary tools with open alternatives. Always cite repo URLs.",
    suggestions: [
      { text: "Find self-hosted alternatives to Notion", icon: "📝" },
      { text: "Compare open-source vector databases for RAG", icon: "🧮" },
      { text: "Audit a GitHub repository for maturity and risk", icon: "🔎" },
      { text: "Build a data stack from open-source tools", icon: "🧰" },
      { text: "Source an open-source license that fits our product", icon: "📜" },
    ],
    welcomeMessage: "Name a tool or problem, and I will scout the best open-source options.",
  },
  Security: {
    agent: "code_fixer",
    systemPrompt: "You are Hermes Code-Fixer in a security-review role. Find vulnerabilities, trace the root cause, and return corrected full code with tests or guards. Prioritize OWASP and infrastructure hardening issues, then give a remediation checklist and verify the fixed path.",
    suggestions: [
      { text: "Review this auth flow for common vulnerabilities", icon: "🔐" },
      { text: "Harden a Node.js API against injection and SSRF", icon: "🧱" },
      { text: "Fix an exposed S3 bucket configuration", icon: "🪣" },
      { text: "Write a threat model for a payment integration", icon: "🧭" },
      { text: "Add dependency-scanning CI gates to a repo", icon: "🛡" },
    ],
    welcomeMessage: "Paste code or infrastructure config, and I will run a security-first fix.",
  },
};

const AGENT_DISPLAY: Record<AgentName, string> = {
  router: "Router",
  general: "General",
  researcher: "Researcher",
  coder: "Coder",
  code_fixer: "Code-Fixer",
  repo_scout: "Repo-Scout",
  ecosystem_architect: "Ecosystem-Architect",
  integrator: "Integrator",
  analyst: "Analyst",
  document: "Document",
  predictor: "Predictor",
  editor: "Editor",
  ui_designer: "UI-Designer",
  marketer: "Marketer",
};

export default function Home() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [recording, setRecording] = useState(false);
  const [voiceOk, setVoiceOk] = useState(false);
  const [deep, setDeep] = useState(false);
  const [atts, setAtts] = useState<Att[]>([]);
  const [drag, setDrag] = useState(false);
  const [activeTab, setActiveTab] = useState("Research");
  const recRef = useRef<any>(null);
  const chatRef = useRef<HTMLDivElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SR) { setVoiceOk(true); const r = new SR(); r.continuous = false; r.interimResults = true; r.lang = "en-US";
      r.onresult = (e: any) => { let t = ""; for (let i = e.resultIndex; i < e.results.length; i++) t += e.results[i][0].transcript; setInput(t); };
      r.onend = () => setRecording(false); r.onerror = () => setRecording(false); recRef.current = r; }
  }, []);
  useEffect(() => { setMessages([]); }, [activeTab]);
  useEffect(() => { chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: "smooth" }); }, [messages, busy, atts]);

  function toggleMic() { if (!recRef.current) return; if (recording) { recRef.current.stop(); setRecording(false); } else { setInput(""); recRef.current.start(); setRecording(true); } }

  async function readFile(f: File): Promise<Att> {
    const a: Att = { name: f.name, type: f.type || "application/octet-stream", size: f.size, file: f };
    if (f.type.startsWith("image/") || f.type.startsWith("video/")) {
      a.preview = await new Promise((res) => { const r = new FileReader(); r.onload = () => res(r.result as string); r.readAsDataURL(f); });
    }
    if (TEXTy(f.type, f.name) && f.size < 1_500_000) {
      a.text = (await f.text()).slice(0, 12000);
    }
    return a;
  }
  async function addFiles(list: FileList | File[]) {
    const arr = Array.from(list);
    const read = await Promise.all(arr.map(readFile));
    setAtts((p) => [...p, ...read]);
  }
  function removeAtt(i: number) { setAtts((p) => p.filter((_, idx) => idx !== i)); }

  async function uploadAtts(list: Att[]) {
    for (const a of list) {
      if (a.url || !a.file) continue;
      try {
        const blob = await upload(a.name, a.file, { access: "public", handleUploadUrl: "/api/upload/blob" });
        a.url = blob.url;
      } catch { /* fall back to inline if blob not configured */ }
    }
  }

  async function send(text?: string) {
    const content = (text ?? input).trim();
    if ((!content && atts.length === 0) || busy) return;
    if (recording) { recRef.current?.stop(); setRecording(false); }
    const myAtts = atts;
    setBusy(true);
    await uploadAtts(myAtts);
    let payload = content;
    const fileText = myAtts.filter((a) => a.text).map((a) => `FILE: ${a.name}\n${a.text}`).join("\n\n");
    const fileList = myAtts.map((a) => `${a.name} (${a.type}, ${(a.size / 1024).toFixed(0)} KB${a.url ? ", url: " + a.url : ""})`).join(", ");
    if (myAtts.length) payload += `\n\n[Attached ${myAtts.length} file(s): ${fileList}]` + (fileText ? `\n\n${fileText}` : "");
    const next = [...messages, { role: "user" as const, content: content || "(files attached)", atts: myAtts }];
    setMessages(next); setInput(""); setAtts([]);
    try {
      if (deep) {
        const res = await fetch("/api/agent/research", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ query: payload, tab: activeTab, agent: TAB_CONFIG[activeTab].agent }) });
        const data = await res.json();
        const who = (data.contributors || []).filter((c: any) => c.ok).map((c: any) => c.label).join(", ");
        const head = data.stacked ? `Stacked ${data.stacked} model(s)${who ? " \u2014 " + who : ""}${data.academicSources ? ` + ${data.academicSources} source(s)` : ""}.\n\n` : "";
        setMessages((m) => [...m, { role: "assistant", content: head + (data.report || data.error || "(no report)"), label: "Deep Research" }]);
      } else {
        const hist = next.map((m, i) => ({ role: m.role, content: i === next.length - 1 ? payload : m.content }));
        const res = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: hist, tab: activeTab, agent: TAB_CONFIG[activeTab].agent }) });
        const data = await res.json();
        setMessages((m) => [...m, { role: "assistant", content: data.text || data.error || "(no response)", label: data.label }]);
      }
    } catch (e: any) { setMessages((m) => [...m, { role: "assistant", content: "Network error: " + e.message }]); }
    finally { setBusy(false); }
  }

  return (
    <>
      <div className="topbar">
        <div className="topbar-logo">
          <span className="crown">👑</span>
          <span>Kingdom AI OS</span>
          <span className="dropdown">▾</span>
        </div>
      </div>
      <div className="tabnav">
        {TABS.map((t) => (
          <button key={t.label} className={`tab ${t.label === activeTab ? "active" : ""}`} onClick={() => setActiveTab(t.label)}>
            <span className="icon">{t.icon}</span>
            {t.label}
          </button>
        ))}
      </div>
        <div className="app"
          onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
          onDragLeave={() => setDrag(false)}
          onDrop={(e) => { e.preventDefault(); setDrag(false); if (e.dataTransfer.files?.length) addFiles(e.dataTransfer.files); }}>
        <div className="sidebar">
          <div className="sidebar-model">
            <div className="sidebar-model-name">Kingdom Core</div>
            <div className="sidebar-model-info">Multi-Provider Router</div>
            <div className="sidebar-model-info" style={{ marginTop: 2 }}><span className="dot"></span> OpenRouter + Fireworks</div>
          </div>
          <div className="sidebar-search">
            <div className="sidebar-search-wrap">
              <span className="search-icon">🔍</span>
              <input placeholder="Search anything..." disabled aria-label="Search anything" title="Search is currently disabled" style={{ opacity: 0.5, cursor: "not-allowed" }} />
              <span className="shortcut" aria-hidden="true">⌘ K</span>
            </div>
          </div>
          <div className="sidebar-nav">
            <button className="sidebar-nav-item active" onClick={() => setActiveTab("Home")} title="Go to Home"><span className="nav-icon">🏠</span> Home</button>
            <button className="sidebar-nav-item" disabled title="Chat view coming soon"><span className="nav-icon">💬</span> Chat</button>
            <button className="sidebar-nav-item" disabled title="Prompt Library coming soon"><span className="nav-icon">{"\u{1F4D6}"}</span> Prompt Library</button>
            <button className="sidebar-nav-item" disabled title="Integrations coming soon"><span className="nav-icon">{"\u{1F517}"}</span> Integrations</button>
          </div>
          <div className="sidebar-section-header"><span>Pinned</span><button className="plus" disabled aria-label="Add pinned item" title="Add pinned item">+</button></div>
          <div className="sidebar-pinned">
            <button className="pinned-chip" onClick={() => send("OSINT Dashboard")}><span className="picon">{"\u{1F4CA}"}</span> OSINT Dashboard</button>
            <button className="pinned-chip" onClick={() => send("Alpha Deals")}><span className="picon">{"\u{1F4B0}"}</span> Alpha Deals</button>
            <button className="pinned-chip" onClick={() => send("City Blueprint")}><span className="picon">{"\u{1F3D9}"}</span> City Blueprint</button>
            <button className="pinned-chip" onClick={() => send("Agent Swarm")}><span className="picon">🤖</span> Agent Swarm</button>
          </div>
          <div className="sidebar-section-header"><span>Today</span><button className="plus" disabled aria-label="Expand Today" title="Expand Today">{"\u{25B4}"}</button></div>
          <div className="sidebar-today">
            <div className="activity-item"><span>Competitor analysis: Horizon Dev.</span><span className="time">10:42 AM</span></div>
            <div className="activity-item"><span>Zoning laws in Austin metro</span><span className="time">9:15 AM</span></div>
            <div className="activity-item"><span>Material cost forecast Q3</span><span className="time">8:03 AM</span></div>
          </div>
          <div className="sidebar-section-header"><span>Yesterday</span><button className="plus" disabled aria-label="Expand Yesterday" title="Expand Yesterday">{"\u{25B4}"}</button></div>
          <div className="sidebar-yesterday">
            <div className="activity-item"><span>Biotech funding trends 2024</span><span className="time">Yesterday</span></div>
            <div className="activity-item"><span>Stealth startup teardown</span><span className="time">Yesterday</span></div>
          </div>
          <div className="sidebar-user">
            <div className="sidebar-user-avatar">S</div>
            <div className="sidebar-user-info">
              <div className="sidebar-user-name">Sovereign User</div>
              <div className="sidebar-user-plan">Pro Plan</div>
            </div>
            <span className="sidebar-user-crown">{"\u{1F451}"}</span>
          </div>
        </div>
        <div className="main">
          <div className="main-header">
            <div className="main-title"><span className="sparkle">✨</span> {activeTab}</div>
            <div className="main-subtitle">Powered by Hermes {AGENT_DISPLAY[TAB_CONFIG[activeTab].agent]} agent</div>
          </div>
          {messages.length === 0 && (
            <div className="prompt-suggestions">
              {TAB_CONFIG[activeTab].suggestions.map((p) => (
                <button key={p.text} className="prompt-chip" onClick={() => send(p.text)}>
                  <span className="picon">{p.icon}</span> {p.text}
                </button>
              ))}
            </div>
          )}
          <div className="chat-area" ref={chatRef}
            
            
            >
            {messages.length === 0 && <div className="empty">{TAB_CONFIG[activeTab].welcomeMessage}</div>}
            {messages.map((m, i) => (
              <div key={i} className={`msg ${m.role}`}>
                <div className="av">{m.role === "user" ? "You" : "✨"}</div>
                <div className="bubble">
                  {m.role === "assistant" && m.label && <div className="tag">{m.label} agent</div>}
                  {m.content}
                  {m.atts && m.atts.length > 0 && (
                    <div className="atts">{m.atts.map((a, j) => (
                      <span className="att" key={j}>{a.preview && a.type.startsWith("image/")
                        ? <img src={a.preview} alt={a.name} />
                        : a.preview && a.type.startsWith("video/")
                        ? <video src={a.preview} muted />
                        : <span className="fileic">FILE</span>}<span className="attn">{a.name}</span></span>))}</div>
                  )}
                </div>
              </div>
            ))}
            {busy && (<div className="msg assistant busy-msg"><div className="av">✨</div><div className="bubble">{deep ? "Stacking research models…" : "Routing through the swarm…"}</div></div>)}
          </div>
          {atts.length > 0 && (
            <div className="tray">{atts.map((a, i) => (
              <span className="att" key={i}>
                {a.preview && a.type.startsWith("image/") ? <img src={a.preview} alt={a.name} />
                  : a.preview && a.type.startsWith("video/") ? <video src={a.preview} muted />
                  : <span className="fileic">FILE</span>}
                <span className="attn">{a.name}</span>
                <button className="x" onClick={() => removeAtt(i)}>×</button>
              </span>))}
              <span className="trayinfo">{atts.length} file(s) attached</span>
            </div>
          )}
          <div className="composer-wrap">
            <div className="composer">
              <button className="composer-btn" title="Attach files" onClick={() => fileRef.current?.click()}>📎</button>
              <input ref={fileRef} type="file" multiple style={{ display: "none" }} onChange={(e) => { if (e.target.files) addFiles(e.target.files); e.currentTarget.value = ""; }} />
              <button className={`composer-btn ${recording ? "rec" : ""}`} title={voiceOk ? "Voice to text" : "Voice not supported"} onClick={toggleMic} disabled={!voiceOk}>{recording ? "■" : "🎤"}</button>
              <button className={`deep-toggle ${deep ? "on" : ""}`} title="Toggle deep research" onClick={() => setDeep((d) => !d)}>🌐 Deep Research ▾</button>
              <textarea value={input} placeholder={recording ? "Listening…" : deep ? "Deep research query…" : `Ask me anything in ${activeTab}...`} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }} rows={1} />
              <button className="composer-btn send-btn" onClick={() => send()} disabled={busy}>↑</button>
            </div>
            <div className="composer-hint">Press Enter to send, Shift+Enter for new line</div>
          </div>
          {drag && <div className="dropzone">Drop files to attach</div>}
        </div>
        <div className="right-panel">
          <div className="right-section">
            <div className="right-section-header">
              <div className="right-section-title"><span className="ricon">👥</span> Active Agents</div>
              <button className="plus-btn" disabled aria-label="Add agent" title="Add agent">+</button>
            </div>
            {AGENTS.map((a) => (
              <div className="agent-item" key={a.name}>
                <div className="agent-avatar" style={{ background: a.color }}>{a.icon}</div>
                <div className="agent-info">
                  <div className="agent-name">{a.name}</div>
                  <div className="agent-role">{a.role}</div>
                </div>
                <div className="agent-status"></div>
              </div>
            ))}
            <button className="view-all">View all agents →</button>
          </div>
          <div className="right-section">
            <div className="right-section-header">
              <div className="right-section-title"><span className="ricon">{"\u2705"}</span> Tasks</div>
              <span style={{ fontSize: 12, color: "var(--muted)", border: "1px solid var(--line)", padding: "2px 8px", borderRadius: 999 }}>{TASKS.filter(t => t.status === "running").length} Active</span>
            </div>
            {TASKS.map((t) => (
              <div className="task-item" key={t.name}>
                <div className="task-left">
                  <div className={`task-dot ${t.status}`}></div>
                  <span>{t.name}</span>
                </div>
                <span className={`task-status ${t.status}`}>{t.status === "running" ? "Running" : "Queued"}</span>
              </div>
            ))}
            <button className="view-all">View all tasks {"\u2192"}</button>
          </div>
        </div>
      </div>
    </>
  );
}
