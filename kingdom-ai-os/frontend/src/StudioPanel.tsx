import { useEffect, useMemo, useState } from 'react';
import { Clapperboard, Film, Brain, Search, Download, Loader2, AlertTriangle, Plus, Trash2, Clock3, Sparkles, ShieldCheck, Globe } from 'lucide-react';

type ClockAct = { act: number; label: string; start: number; end: number; beat?: string; written?: boolean };
type Line = { character: string; line: string };
type Scene = { minute_start: number; minute_end: number; int_ext: string; location: string; time_of_day: string; action: string; dialogue: Line[]; camera: string; color: string; music: string; act?: number };
type Act = { act: number; label: string; start: number; end: number; act_summary: string; scenes: Scene[]; model_id?: string };
type Movie = { id: string; title: string; minutes: number; premise: string; clock: ClockAct[]; acts: Record<string, Act>; memory: Record<string, string>; archive_items: number };
type Row = { id: string; title: string; minutes: number; acts_written: number; acts_total: number };
type Model = { id: string; name: string };

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch('/api/v1/studio' + path, { headers: { 'Content-Type': 'application/json' }, ...init });
  if (!r.ok) { let d = `HTTP ${r.status}`; try { d = (await r.json()).detail || d } catch {} throw new Error(d) }
  return r.json();
}
const mmss = (m: number) => `${Math.floor(m / 60)}:${String(Math.floor(m % 60)).padStart(2, '0')}:${String(Math.round((m % 1) * 60) % 60).padStart(2, '0')}`;
const PERSONAS = ['Visionary auteur: slow-burn, striking images, few words', 'Blockbuster showrunner: big set pieces, fast pace, humor', 'Prestige TV writer: deep characters, sharp dialogue, cliffhangers', 'Animated family film director: warm, funny, colorful'];

export default function StudioPanel() {
  const [list, setList] = useState<Row[]>([]); const [movie, setMovie] = useState<Movie | null>(null);
  const [title, setTitle] = useState(''); const [minutes, setMinutes] = useState(90); const [premise, setPremise] = useState(''); const [persona, setPersona] = useState(PERSONAS[0]);
  const [models, setModels] = useState<Model[]>([]); const [model, setModel] = useState('');
  const [busy, setBusy] = useState(''); const [error, setError] = useState('');
  const [view, setView] = useState<'script' | 'memory'>('script'); const [from, setFrom] = useState(0); const [to, setTo] = useState(5); const [found, setFound] = useState<Scene[] | null>(null);
  const [notes, setNotes] = useState(''); const [question, setQuestion] = useState(''); const [preview, setPreview] = useState<ClockAct[]>([]);

  useEffect(() => { refresh(); fetch('/api/v1/catalog/models?limit=80&free=true').then(r => r.json()).then(r => setModels(r.items || [])).catch(() => setModels([])) }, []);
  useEffect(() => { const t = setTimeout(() => { if (minutes >= 1 && minutes <= 600) api<ClockAct[]>(`/clock?minutes=${minutes}`).then(setPreview).catch(() => setPreview([])) }, 150); return () => clearTimeout(t) }, [minutes]);
  function refresh() { api<Row[]>('/projects').then(setList).catch(() => setList([])) }
  async function run(label: string, fn: () => Promise<void>) { setBusy(label); setError(''); try { await fn() } catch (e) { setError((e as Error).message) } finally { setBusy('') } }
  const open = (id: string) => run('Opening…', async () => { setMovie(await api<Movie>(`/projects/${id}`)); setFound(null) });
  const create = () => run('Building the movie bible…', async () => {
    const m = await api<Movie>('/projects', { method: 'POST', body: JSON.stringify({ title, minutes, premise, persona: `You are a film director. Style: ${persona}.`, model_id: model || null }) });
    setMovie(m); refresh() });
  const nextAct = movie?.clock.find(a => !a.written);
  const write = (act: number) => run(`Writing ${movie!.clock.find(a => a.act === act)?.label}…`, async () => {
    await api(`/projects/${movie!.id}/acts/${act}`, { method: 'POST', body: JSON.stringify({ model_id: model || null, notes }) });
    setNotes(''); setMovie(await api<Movie>(`/projects/${movie!.id}`)); refresh() });
  const jump = () => run('Finding scenes…', async () => setFound(await api<Scene[]>(`/projects/${movie!.id}/minutes?start=${from}&end=${to}`)));
  const research = () => run('Researching the web…', async () => { await api(`/projects/${movie!.id}/research`, { method: 'POST', body: JSON.stringify({ question }) }); setQuestion(''); setMovie(await api<Movie>(`/projects/${movie!.id}`)) });
  const remove = (id: string) => run('', async () => { await api(`/projects/${id}`, { method: 'DELETE' }); if (movie?.id === id) setMovie(null); refresh() });
  const acts = useMemo(() => movie ? Object.values(movie.acts).sort((a, b) => a.act - b.act) : [], [movie]);
  const bible = useMemo(() => { try { return JSON.parse(movie?.memory.movie_bible || '{}') } catch { return {} } }, [movie]);
  const style = useMemo(() => { try { return JSON.parse(movie?.memory.style_bible || '{}') } catch { return {} } }, [movie]);
  const done = movie ? movie.clock.filter(a => a.written).length : 0;

  const picker = <select className="studio-input" value={model} onChange={e => setModel(e.target.value)} aria-label="Model"><option value="">Recommended free model</option>{models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}</select>;
  const status = <>{busy && <div className="notice"><Loader2 size={16} className="spin" /> {busy} <small>Free models on your own server can take a few minutes per act.</small></div>}{error && <div className="notice err"><AlertTriangle size={16} /> {error}</div>}</>;

  if (!movie) return <section className="welcome studio">
    <div className="eyebrow"><span className="eyebrow-icon"><Clapperboard size={14} /></span> TV / MOVIE STUDIO <span className="line" /></div>
    <h1>Any length. <em>One mind.</em></h1>
    <p>Pick the minutes, and the studio builds a clock of acts, writes each one in a locked screenplay template, and remembers every character, color and choice.</p>
    <div className="studio-card">
      <input className="studio-input" placeholder="Title, e.g. The Last Lighthouse" value={title} onChange={e => setTitle(e.target.value)} />
      <textarea className="studio-input" rows={4} placeholder="Premise: who, where, what goes wrong, how it should feel…" value={premise} onChange={e => setPremise(e.target.value)} />
      <div className="studio-row"><label><Clock3 size={14} /> Minutes <input type="number" min={1} max={600} value={minutes} onChange={e => setMinutes(Number(e.target.value))} className="studio-input small" /></label>
        <select className="studio-input" value={persona} onChange={e => setPersona(e.target.value)} aria-label="Director style">{PERSONAS.map(p => <option key={p}>{p}</option>)}</select>{picker}</div>
      {preview.length > 0 && <div className="clock">{preview.map(a => <span key={a.act} style={{ flex: a.end - a.start }} title={`${a.label}: ${a.start}-${a.end} min`}>{a.label}<small>{a.start}–{a.end}</small></span>)}</div>}
      <button className="studio-primary" disabled={!!busy || !title.trim() || premise.trim().length < 3} onClick={create}><Sparkles size={15} /> Create movie bible</button>
    </div>
    {status}
    {list.length > 0 && <div className="studio-list"><b>Your movies</b>{list.map(r => <div key={r.id} className="history-row"><button onClick={() => open(r.id)}>{r.title}<small>{r.minutes} min · {r.acts_written}/{r.acts_total} acts written</small></button><button aria-label="Delete movie" onClick={() => remove(r.id)}><Trash2 size={13} /></button></div>)}</div>}
    <div className="bottom-note"><ShieldCheck size={15} /> Runs on free open-source models. Everything is saved on your server.</div>
  </section>;

  return <section className="welcome studio has-movie">
    <div className="chat-bar"><button className="text-btn" onClick={() => { setMovie(null); refresh() }}><Plus size={14} /> All movies</button>
      <a className="text-btn" href={`/api/v1/studio/projects/${movie.id}/screenplay.fountain`} download={`${movie.title}.fountain`}><Download size={14} /> Screenplay</a>
      <a className="text-btn" href={`/api/v1/studio/projects/${movie.id}/shots`} download={`${movie.title}-shots.json`}><Film size={14} /> Shot list for video</a></div>
    <h2 className="studio-title">{movie.title} <small>{movie.minutes} min · {done}/{movie.clock.length} acts · {movie.archive_items} memories</small></h2>
    {bible.logline && <p className="studio-logline">{bible.logline}</p>}
    <div className="clock">{movie.clock.map(a => <button key={a.act} className={a.written ? 'written' : ''} style={{ flex: a.end - a.start }} onClick={() => a.written ? document.getElementById(`act-${a.act}`)?.scrollIntoView({ behavior: 'smooth' }) : write(a.act)} disabled={!!busy} title={a.beat}>{a.label}<small>{a.start}–{a.end}</small></button>)}</div>
    <div className="studio-card">
      {nextAct ? <><div className="studio-row"><b>Next: {nextAct.label} ({nextAct.start}–{nextAct.end} min)</b>{picker}</div>
        {nextAct.beat && <small className="muted">Beat: {nextAct.beat}</small>}
        <input className="studio-input" placeholder="Optional notes for this act (a twist, a song, a location…)" value={notes} onChange={e => setNotes(e.target.value)} />
        <button className="studio-primary" disabled={!!busy} onClick={() => write(nextAct.act)}><Clapperboard size={15} /> Write {nextAct.label}</button></>
        : <b>All {movie.clock.length} acts are written. Download the screenplay or the shot list above.</b>}
    </div>
    {status}
    <div className="studio-tabs"><button className={view === 'script' ? 'on' : ''} onClick={() => setView('script')}><Film size={14} /> Script</button><button className={view === 'memory' ? 'on' : ''} onClick={() => setView('memory')}><Brain size={14} /> Memory & research</button></div>
    {view === 'script' ? <>
      {acts.length > 0 && <div className="studio-row jump"><Clock3 size={14} /> Jump to minute <input type="number" min={0} value={from} onChange={e => setFrom(Number(e.target.value))} className="studio-input small" /> to <input type="number" min={0} value={to} onChange={e => setTo(Number(e.target.value))} className="studio-input small" /><button className="text-btn" onClick={jump}>Show</button>{found && <button className="text-btn" onClick={() => setFound(null)}>Clear</button>}</div>}
      {(found ? [{ act: 0, label: `Minutes ${from}–${to}`, start: from, end: to, act_summary: `${found.length} scene(s)`, scenes: found }] : acts).map(a => <div key={a.act} id={`act-${a.act}`} className="act">
        <h3>{a.label} <small>{a.start}–{a.end} min{a.model_id ? ` · ${a.model_id}` : ''}</small></h3><p className="muted">{a.act_summary}</p>
        {a.scenes.map((s, i) => <div key={i} className="scene"><div className="slug"><span className="tc">{mmss(s.minute_start)}</span>{s.int_ext} {s.location.toUpperCase()} – {s.time_of_day.toUpperCase()}</div>
          <p>{s.action}</p>{s.dialogue.map((d, j) => <div key={j} className="dlg"><b>{d.character.toUpperCase()}</b><span>{d.line}</span></div>)}
          <div className="chips"><span className="chip">🎥 {s.camera}</span><span className="chip">🎨 {s.color}</span><span className="chip">🎵 {s.music}</span></div></div>)}
      </div>)}
      {acts.length === 0 && <p className="muted">No acts yet. Click an act on the clock, or "Write Act 1" above.</p>}
    </> : <div className="memory">
      <div className="studio-card"><b><Globe size={14} /> Deep research (free web search, saved to memory)</b><div className="studio-row"><input className="studio-input" placeholder="e.g. 1920s lighthouse keeper daily life" value={question} onChange={e => setQuestion(e.target.value)} /><button className="studio-primary" disabled={!!busy || question.trim().length < 3} onClick={research}><Search size={14} /> Research</button></div></div>
      {bible.characters?.length > 0 && <div className="studio-card"><b>Characters</b>{bible.characters.map((c: any) => <p key={c.name}><b>{c.name}</b> · {c.role}<br /><small className="muted">{c.look} — wants: {c.want}</small></p>)}</div>}
      {Object.keys(style).length > 0 && <div className="studio-card"><b>Style bible</b>{Object.entries(style).map(([k, v]) => <p key={k}><small className="muted">{k.replace(/_/g, ' ')}</small><br />{String(v)}</p>)}</div>}
      <div className="studio-card"><b>Core memory blocks</b><small className="muted">Always loaded for every act. Older acts, scenes and research live in long-term memory ({movie.archive_items} items) and are recalled when relevant.</small>
        {['human', 'persona', 'current_act'].map(k => <p key={k}><small className="muted">{k.replace('_', ' ')}</small><br />{movie.memory[k] || '—'}</p>)}</div>
    </div>}
  </section>;
}
