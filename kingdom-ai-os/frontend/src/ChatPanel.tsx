import { useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { Sparkles, Paperclip, ArrowUp, ChevronDown, Search, WandSparkles, Command, CheckCircle2, ImagePlus, Cpu, Boxes, ShieldCheck, Globe, History, Plus, Trash2, X, Loader2, AlertTriangle } from 'lucide-react';

type Msg = { id: string; role: 'user' | 'assistant'; content: string; model_id?: string; citations?: { url: string; title: string }[]; attachments?: string[] };
type Conv = { id: string; tab_id: string; title: string; updated_at: number };
type Model = { id: string; name: string; context?: number; price_in?: number | null; price_out?: number | null; free: boolean; vision: boolean; check: string };
type Status = { chat_ready: boolean; default_model: string; catalog_count: number; database: string };
type Props = { tabId: string; tabName: string; webDefault: boolean; status: Status | null; onNavigate: (id: string) => void };

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch('/api/v1' + path, { headers: { 'Content-Type': 'application/json' }, ...init });
  if (!r.ok) { let d = `HTTP ${r.status}`; try { d = (await r.json()).detail || d } catch {} throw new Error(d) }
  return r.json();
}

/* Small, safe markdown renderer: headings, bullets, numbered lists, bold, italics, code, links. No raw HTML. */
function inline(text: string, key: string) {
  const parts: (string | ReactNode)[] = []; const re = /(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\(https?:\/\/[^)\s]+\)|\*[^*\s][^*]*\*)/g; let last = 0; let m: RegExpExecArray | null; let i = 0;
  while ((m = re.exec(text))) { if (m.index > last) parts.push(text.slice(last, m.index)); const t = m[0];
    if (t.startsWith('**')) parts.push(<strong key={key + i++}>{t.slice(2, -2)}</strong>);
    else if (t.startsWith('`')) parts.push(<code key={key + i++}>{t.slice(1, -1)}</code>);
    else if (t.startsWith('[')) { const mm = /\[([^\]]+)\]\(([^)]+)\)/.exec(t)!; parts.push(<a key={key + i++} href={mm[2]} target="_blank" rel="noreferrer">{mm[1]}</a>) }
    else parts.push(<em key={key + i++}>{t.slice(1, -1)}</em>);
    last = m.index + t.length }
  if (last < text.length) parts.push(text.slice(last)); return parts;
}
function Markdown({ text }: { text: string }) {
  const blocks: ReactNode[] = []; const lines = text.split('\n'); let i = 0; let k = 0;
  while (i < lines.length) { const line = lines[i];
    if (line.startsWith('```')) { const buf: string[] = []; i++; while (i < lines.length && !lines[i].startsWith('```')) buf.push(lines[i++]); i++; blocks.push(<pre key={k++}><code>{buf.join('\n')}</code></pre>); continue }
    const h = /^(#{1,4})\s+(.*)/.exec(line); if (h) { blocks.push(<h4 key={k++}>{inline(h[2], 'h' + k)}</h4>); i++; continue }
    if (/^\s*([-*•]|\d+\.)\s+/.test(line)) { const ordered = /^\s*\d+\./.test(line); const items: string[] = []; while (i < lines.length && /^\s*([-*•]|\d+\.)\s+/.test(lines[i])) items.push(lines[i++].replace(/^\s*([-*•]|\d+\.)\s+/, ''));
      const li = items.map((t, j) => <li key={j}>{inline(t, `l${k}-${j}`)}</li>); blocks.push(ordered ? <ol key={k++}>{li}</ol> : <ul key={k++}>{li}</ul>); continue }
    if (!line.trim()) { i++; continue }
    const buf: string[] = []; while (i < lines.length && lines[i].trim() && !/^(#{1,4}\s|```|\s*([-*•]|\d+\.)\s+)/.test(lines[i])) buf.push(lines[i++]);
    blocks.push(<p key={k++}>{inline(buf.join(' '), 'p' + k)}</p>) }
  return <div className="md">{blocks}</div>;
}

export default function ChatPanel({ tabId, tabName, webDefault, status, onNavigate }: Props) {
  const [convs, setConvs] = useState<Conv[]>([]); const [convId, setConvId] = useState<string | null>(null); const [messages, setMessages] = useState<Msg[]>([]);
  const [text, setText] = useState(''); const [busy, setBusy] = useState(false); const [error, setError] = useState('');
  const [web, setWeb] = useState(webDefault); const [files, setFiles] = useState<{ name: string; text: string }[]>([]);
  const [model, setModel] = useState(localStorage.getItem('kaios-model') || ''); const [pickerOpen, setPickerOpen] = useState(false); const [historyOpen, setHistoryOpen] = useState(false);
  const [models, setModels] = useState<Model[]>([]); const [mq, setMq] = useState(''); const [freeOnly, setFreeOnly] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => { setWeb(webDefault); setConvId(null); setMessages([]); setError(''); refreshConvs() }, [tabId]);
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages, busy]);
  useEffect(() => { if (!pickerOpen) return; const t = setTimeout(() => api<{ items: Model[] }>(`/catalog/models?limit=80&free=${freeOnly}${mq ? '&q=' + encodeURIComponent(mq) : ''}`).then(r => setModels(r.items)).catch(() => setModels([])), 200); return () => clearTimeout(t) }, [pickerOpen, mq, freeOnly]);
  const modelLabel = useMemo(() => (model || status?.default_model || 'Auto').split('/').pop(), [model, status]);

  function refreshConvs() { api<Conv[]>(`/conversations?tab_id=${tabId}`).then(setConvs).catch(() => setConvs([])) }
  async function open(id: string) { setHistoryOpen(false); setError(''); const c = await api<{ messages: Msg[] }>(`/conversations/${id}`); setConvId(id); setMessages(c.messages) }
  async function remove(id: string) { await api(`/conversations/${id}`, { method: 'DELETE' }); if (id === convId) { setConvId(null); setMessages([]) } refreshConvs() }
  function fresh() { setConvId(null); setMessages([]); setError(''); setHistoryOpen(false) }
  function chooseModel(id: string) { setModel(id); localStorage.setItem('kaios-model', id); setPickerOpen(false) }

  async function attach(list: FileList | null) {
    if (!list) return; setError('');
    for (const f of Array.from(list).slice(0, 5)) {
      if (f.size > 20 * 1024 * 1024) { setError(`${f.name} is over 20 MB.`); continue }
      const b64 = await new Promise<string>((res, rej) => { const r = new FileReader(); r.onload = () => res(String(r.result).split(',')[1] || ''); r.onerror = rej; r.readAsDataURL(f) });
      try { const out = await api<{ name: string; text: string }>('/files/extract', { method: 'POST', body: JSON.stringify({ name: f.name, data_b64: b64 }) }); setFiles(x => [...x, { name: out.name, text: out.text }]) } catch (e) { setError(`${f.name}: ${(e as Error).message}`) }
    }
  }

  async function send(preset?: string) {
    const content = (preset ?? text).trim(); if (!content || busy) return;
    setBusy(true); setError(''); const sentFiles = files; setText(''); setFiles([]);
    setMessages(m => [...m, { id: 'pending', role: 'user', content, attachments: sentFiles.map(f => f.name) }]);
    try {
      let id = convId; if (!id) { const c = await api<Conv>('/conversations', { method: 'POST', body: JSON.stringify({ tab_id: tabId }) }); id = c.id; setConvId(id) }
      const r = await api<{ user: Msg; assistant: Msg }>(`/conversations/${id}/messages`, { method: 'POST', body: JSON.stringify({ content, model_id: model || null, web_search: web, attachments: sentFiles }) });
      setMessages(m => [...m.filter(x => x.id !== 'pending'), r.user, r.assistant]); refreshConvs();
    } catch (e) { setError((e as Error).message); setText(content); setFiles(sentFiles) } finally { setBusy(false) }
  }

  const empty = messages.length === 0;
  const composer = <div className="composer">
    {files.length > 0 && <div className="chips">{files.map((f, i) => <span className="chip" key={i}><Paperclip size={12} />{f.name}<button aria-label="Remove file" onClick={() => setFiles(x => x.filter((_, j) => j !== i))}><X size={12} /></button></span>)}</div>}
    <textarea value={text} onChange={e => setText(e.target.value)} placeholder={`Ask ${tabName.split(' /')[0]} anything…`} onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() } }} />
    <div className="composer-bottom"><div className="composer-tools">
      <label className="tool-btn" title="Attach PDF, Word, text or code files"><Paperclip size={17} /><span>Attach</span><input type="file" multiple hidden accept=".pdf,.docx,.txt,.md,.csv,.json,.html,.py,.ts,.tsx,.js" onChange={e => { attach(e.target.files); e.target.value = '' }} /></label>
      <button className={`tool-btn ${web ? 'on' : ''}`} title="Search the web and cite sources" onClick={() => setWeb(v => !v)}><Globe size={16} /><span>Web {web ? 'on' : 'off'}</span></button>
      <div className="picker-wrap"><button className="model-select" onClick={() => setPickerOpen(v => !v)}><span className="model-orb" /> {modelLabel} <ChevronDown size={13} /></button>
        {pickerOpen && <div className="model-picker"><div className="picker-search"><Search size={14} /><input autoFocus onKeyDown={e => { if (e.key === "Escape") setPickerOpen(false) }} value={mq} onChange={e => setMq(e.target.value)} placeholder={`Search ${status?.catalog_count || ''} live models`} /></div>
          <label className="picker-free"><input type="checkbox" checked={freeOnly} onChange={e => setFreeOnly(e.target.checked)} /> Free models only</label>
          <button className={`picker-row ${!model ? 'sel' : ''}`} onClick={() => chooseModel('')}><b>Recommended</b><small>{status?.default_model} · falls back automatically if it fails</small></button>
          {models.map(m => <button key={m.id} className={`picker-row ${model === m.id ? 'sel' : ''}`} onClick={() => chooseModel(m.id)}><b>{m.name}{m.check === 'passed' && <CheckCircle2 size={12} className="ok" />}</b><small>{m.id} · {m.free ? 'free' : m.price_in != null ? `$${m.price_in}/$${m.price_out} per 1M` : ''}{m.context ? ` · ${Math.round(m.context / 1000)}k ctx` : ''}{m.vision ? ' · vision' : ''}</small></button>)}
          {models.length === 0 && <small className="picker-empty">No models match.</small>}</div>}
      </div></div>
      <div className="composer-right"><span className="shortcut">Shift ↵ for new line</span><button className="send-btn" onClick={() => send()} disabled={busy} aria-label="Send">{busy ? <Loader2 size={18} className="spin" /> : <ArrowUp size={18} />}</button></div></div>
  </div>;

  return <section className={`welcome chat ${empty ? '' : 'has-messages'}`}>
    <div className="chat-bar"><button className="text-btn" onClick={() => setHistoryOpen(v => !v)}><History size={14} /> History ({convs.length})</button><button className="text-btn" onClick={fresh}><Plus size={14} /> New chat</button></div>
    {historyOpen && <div className="history">{convs.length === 0 && <small>No saved chats in this workspace yet.</small>}{convs.map(c => <div key={c.id} className={`history-row ${c.id === convId ? 'sel' : ''}`}><button onClick={() => open(c.id)}>{c.title}<small>{new Date(c.updated_at * 1000).toLocaleString()}</small></button><button aria-label="Delete chat" onClick={() => remove(c.id)}><Trash2 size={13} /></button></div>)}</div>}
    {status && !status.chat_ready && <div className="notice warn"><AlertTriangle size={16} /> Chat is almost ready. The server needs an OpenRouter API key (<code>OPENROUTER_API_KEY</code>) before models can answer. Everything else works.</div>}
    {empty ? <>
      <div className="eyebrow"><span className="eyebrow-icon"><Sparkles size={14} /></span> {tabId === 'home' ? 'YOUR AI WORKSPACE' : tabName.toUpperCase()} <span className="line" /></div>
      {tabId === 'home' ? <h1>What are we <em>building</em><br />today?</h1> : <h1>{tabName.split(' /')[0]} <em>assistant</em></h1>}
      <p>{tabId === 'home' ? 'One place to think, create, research, and bring your ideas to life.' : 'Ask a question, attach files, and keep every chat saved in this workspace.'}</p>
      {composer}
      {error && <div className="notice err"><AlertTriangle size={16} /> {error}</div>}
      {tabId === 'home' && <div className="quick-grid">
        <button onClick={() => { onNavigate('research') }}><span className="quick-icon purple"><Search size={17} /></span><span><b>Research & analyze</b><small>Cited answers from the web</small></span><span className="quick-arrow">↗</span></button>
        <button onClick={() => onNavigate('images-visual-ai')}><span className="quick-icon orange"><WandSparkles size={17} /></span><span><b>Create something</b><small>Images, video, and audio plans</small></span><span className="quick-arrow">↗</span></button>
        <button onClick={() => onNavigate('coding-dev')}><span className="quick-icon blue"><Command size={17} /></span><span><b>Build with code</b><small>Plan, implement, and test</small></span><span className="quick-arrow">↗</span></button>
        <button onClick={() => onNavigate('tasks')}><span className="quick-icon green"><CheckCircle2 size={17} /></span><span><b>Manage tasks</b><small>Turn goals into steps</small></span><span className="quick-arrow">↗</span></button>
        <button onClick={() => onNavigate('document-studio')}><span className="quick-icon orange"><ImagePlus size={17} /></span><span><b>Document Studio</b><small>Styled PDFs and editable DOCX</small></span><span className="quick-arrow">↗</span></button>
        <button onClick={() => onNavigate('model-verification')}><span className="quick-icon blue"><Cpu size={17} /></span><span><b>Verify a model</b><small>Live catalog and response test</small></span><span className="quick-arrow">↗</span></button>
        <button onClick={() => onNavigate('registry-change')}><span className="quick-icon purple"><Boxes size={17} /></span><span><b>Add tools or models</b><small>Validate a safe registry proposal</small></span><span className="quick-arrow">↗</span></button>
      </div>}
      <div className="bottom-note"><ShieldCheck size={15} /> Chats are saved on your server. Provider keys never reach the browser.</div>
    </> : <>
      <div className="thread">{messages.map(m => <div key={m.id} className={`msg ${m.role}`}>
        {m.role === 'assistant' && <div className="msg-avatar"><Sparkles size={14} /></div>}
        <div className="bubble">{m.role === 'assistant' ? <Markdown text={m.content} /> : <p>{m.content}</p>}
          {!!m.attachments?.length && <div className="chips">{m.attachments.map(a => <span className="chip" key={a}><Paperclip size={11} />{a}</span>)}</div>}
          {!!m.citations?.length && <div className="sources"><b>Sources</b>{m.citations.map((c, i) => <a key={c.url} href={c.url} target="_blank" rel="noreferrer">[{i + 1}] {c.title}</a>)}</div>}
          {m.model_id && <small className="msg-meta">{m.model_id}</small>}</div></div>)}
        {busy && <div className="msg assistant"><div className="msg-avatar"><Sparkles size={14} /></div><div className="bubble typing"><span /><span /><span /></div></div>}
        <div ref={endRef} /></div>
      {error && <div className="notice err"><AlertTriangle size={16} /> {error}</div>}
      <div className="composer-dock">{composer}</div>
    </>}
  </section>;
}
