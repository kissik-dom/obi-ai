"use client";
import { upload } from "@vercel/blob/client";
import { useEffect, useRef, useState } from "react";
type Att = { name: string; type: string; size: number; preview?: string; text?: string; file?: File; url?: string };
type Msg = { role: "user" | "assistant"; content: string; label?: string; atts?: Att[] };

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

const PROMPTS = [
  { text: "Latest breakthroughs in synthetic biology", icon: "\u{2795}" },
  { text: "Analyze regulatory shifts in AI governance", icon: "\u{1F4CB}" },
  { text: "Map competitive landscape in quantum computing", icon: "\u{1F30D}" },
  { text: "Evaluate patent filings in advanced materials", icon: "🔬" },
  { text: "Identify emerging risks in supply chains", icon: "\u{26A0}" },
];

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
        const res = await fetch("/api/agent/research", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ query: payload }) });
        const data = await res.json();
        const who = (data.contributors || []).filter((c: any) => c.ok).map((c: any) => c.label).join(", ");
        const head = data.stacked ? `Stacked ${data.stacked} model(s)${who ? " \u2014 " + who : ""}${data.academicSources ? ` + ${data.academicSources} source(s)` : ""}.\n\n` : "";
        setMessages((m) => [...m, { role: "assistant", content: head + (data.report || data.error || "(no report)"), label: "Deep Research" }]);
      } else {
        const hist = next.map((m, i) => ({ role: m.role, content: i === next.length - 1 ? payload : m.content }));
        const res = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: hist }) });
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
              <input placeholder="Search anything..." disabled style={{ opacity: 0.5, cursor: "not-allowed" }} />
              <span className="shortcut">⌘ K</span>
            </div>
          </div>
          <div className="sidebar-nav">
            <button className="sidebar-nav-item active"><span className="nav-icon">🏠</span> Home</button>
            <button className="sidebar-nav-item"><span className="nav-icon">💬</span> Chat</button>
            <button className="sidebar-nav-item"><span className="nav-icon">\u{1F4D6}</span> Prompt Library</button>
            <button className="sidebar-nav-item"><span className="nav-icon">\u{1F517}</span> Integrations</button>
          </div>
          <div className="sidebar-section-header"><span>Pinned</span><span className="plus">+</span></div>
          <div className="sidebar-pinned">
            <span className="pinned-chip"><span className="picon">\u{1F4CA}</span> OSINT Dashboard</span>
            <span className="pinned-chip"><span className="picon">\u{1F4B0}</span> Alpha Deals</span>
            <span className="pinned-chip"><span className="picon">\u{1F3D9}</span> City Blueprint</span>
            <span className="pinned-chip"><span className="picon">🤖</span> Agent Swarm</span>
          </div>
          <div className="sidebar-section-header"><span>Today</span><span className="plus">\u{25B4}</span></div>
          <div className="sidebar-today">
            <div className="activity-item"><span>Competitor analysis: Horizon Dev.</span><span className="time">10:42 AM</span></div>
            <div className="activity-item"><span>Zoning laws in Austin metro</span><span className="time">9:15 AM</span></div>
            <div className="activity-item"><span>Material cost forecast Q3</span><span className="time">8:03 AM</span></div>
          </div>
          <div className="sidebar-section-header"><span>Yesterday</span><span className="plus">\u{25B4}</span></div>
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
            <span className="sidebar-user-crown">\u{1F451}</span>
          </div>
        </div>
        <div className="main">
          <div className="main-header">
            <div className="main-title"><span className="sparkle">✨</span> {activeTab}</div>
            <div className="main-subtitle">Deep context. Verified sources. Strategic intelligence.<br />Ask anything in {activeTab}.</div>
          </div>
          {messages.length === 0 && (
            <div className="prompt-suggestions">
              {PROMPTS.map((p) => (
                <button key={p.text} className="prompt-chip" onClick={() => send(p.text)}>
                  <span className="picon">{p.icon}</span> {p.text}
                </button>
              ))}
            </div>
          )}
          <div className="chat-area" ref={chatRef}
            
            
            >
            {messages.length === 0 && <div className="empty">Ask anything, attach any files (drag and drop too), or toggle Deep Research.</div>}
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
              <button className="plus-btn">+</button>
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
              <div className="right-section-title"><span className="ricon">\u2705</span> Tasks</div>
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
            <button className="view-all">View all tasks \u2192</button>
          </div>
        </div>
      </div>
    </>
  );
}
