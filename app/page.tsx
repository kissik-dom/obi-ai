"use client";
import { upload } from "@vercel/blob/client";
import { useEffect, useRef, useState } from "react";
type Att = { name: string; type: string; size: number; preview?: string; text?: string; file?: File; url?: string };
type Msg = { role: "user" | "assistant"; content: string; label?: string; atts?: Att[] };

const TEXTy = (t: string, n: string) =>
  /^text\//.test(t) || /(json|csv|xml|yaml|markdown|javascript|typescript|x-python|x-sh)/.test(t) ||
  /\.(txt|md|csv|json|js|ts|tsx|jsx|py|sh|css|html|yml|yaml|sql|java|go|rs|c|cpp|rb|php)$/i.test(n);

export default function Home() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [recording, setRecording] = useState(false);
  const [voiceOk, setVoiceOk] = useState(false);
  const [deep, setDeep] = useState(false);
  const [atts, setAtts] = useState<Att[]>([]);
  const [drag, setDrag] = useState(false);
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
    setAtts((p) => [...p, ...read]); // no limit on count
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
    let payload = content;
    const fileText = myAtts.filter((a) => a.text).map((a) => `FILE: ${a.name}\n${a.text}`).join("\n\n");
    const fileList = myAtts.map((a) => `${a.name} (${a.type}, ${(a.size / 1024).toFixed(0)} KB${a.url ? ", url: " + a.url : ""})`).join(", ");
    if (myAtts.length) payload += `\n\n[Attached ${myAtts.length} file(s): ${fileList}]` + (fileText ? `\n\n${fileText}` : "");
    const next = [...messages, { role: "user" as const, content: content || "(files attached)", atts: myAtts }];
    setMessages(next); setInput(""); setAtts([]); setBusy(true);
    await uploadAtts(myAtts);
    try {
      if (deep) {
        const res = await fetch("/api/agent/research", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ query: payload }) });
        const data = await res.json();
        const who = (data.contributors || []).filter((c: any) => c.ok).map((c: any) => c.label).join(", ");
        const head = data.stacked ? `Stacked ${data.stacked} model(s)${who ? " — " + who : ""}${data.academicSources ? ` + ${data.academicSources} source(s)` : ""}.\n\n` : "";
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
  const prompts = ["Draft a consulting proposal", "Research the EV battery market", "Forecast next quarter sales", "Write a Python web scraper"];

  return (
    <div className="wrap"
      onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
      onDragLeave={() => setDrag(false)}
      onDrop={(e) => { e.preventDefault(); setDrag(false); if (e.dataTransfer.files?.length) addFiles(e.dataTransfer.files); }}>
      <div className="header">
        <div className="logo">Oi</div>
        <div><div className="title">Obi AI</div><div className="sub">Hermes swarm · deep research · voice · files</div></div>
        <div className="badge">Powered by Obliteratus</div>
      </div>
      <div className="chat" ref={chatRef}>
        {messages.length === 0 && (
          <div className="empty">Ask anything, attach any files (drag and drop too), or toggle Deep Research.
            <div className="chips">{prompts.map((p) => (<button key={p} className="chip" onClick={() => send(p)}>{p}</button>))}</div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <div className="av">{m.role === "user" ? "You" : "Oi"}</div>
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
        {busy && (<div className="msg assistant"><div className="av">Oi</div><div className="bubble">{deep ? "Stacking research models…" : "Routing through the swarm…"}</div></div>)}
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
      <div className="composer">
        <button className="mic" title="Attach files (unlimited)" onClick={() => fileRef.current?.click()}>＋</button>
        <input ref={fileRef} type="file" multiple style={{ display: "none" }} onChange={(e) => { if (e.target.files) addFiles(e.target.files); e.currentTarget.value = ""; }} />
        <button className={`mic ${recording ? "rec" : ""}`} title={voiceOk ? "Voice to text" : "Voice not supported"} onClick={toggleMic} disabled={!voiceOk}>{recording ? "■" : "🎤"}</button>
        <textarea value={input} placeholder={recording ? "Listening…" : deep ? "Deep research query…" : "Message Obi AI…"} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }} rows={1} />
        <button className={`deep ${deep ? "on" : ""}`} title="Toggle deep research" onClick={() => setDeep((d) => !d)}>{deep ? "Deep ✓" : "Deep"}</button>
        <button className="send" onClick={() => send()} disabled={busy}>Send</button>
      </div>
      <div className="hint">Attach unlimited images, videos, and files (＋ or drag-drop). Text docs are read by the assistant. Enter to send.</div>
      {drag && <div className="dropzone">Drop files to attach</div>}
    </div>
  );
}
