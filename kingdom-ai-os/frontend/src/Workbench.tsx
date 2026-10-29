import { useState } from 'react';
import { FileText, ScanSearch, Cpu, GitPullRequest, ShieldAlert } from 'lucide-react';

const sample = JSON.stringify({
  title: 'The Kisi People: Research Monograph',
  subtitle: 'A source-led research volume',
  author: 'Kingdom AI OS Research Studio',
  font: 'Times-Roman', page_size: 'A4', margin_inches: 0.85,
  footer_quote: 'History deserves care, evidence, and dignity.', include_contents: true,
  sections: [
    { title: 'Chapter 1 — Scope and Method', body: 'Replace this sample with the chapter text generated and checked by your research workflow.\n\nKeep each chapter as its own section so it can be revised without rebuilding the whole manuscript.' },
    { title: 'Chapter 2 — Sources and Evidence', body: 'Separate primary sources, secondary research, and claims that still need verification. Add citations before publication.' }
  ],
  glossary: [{ term: 'Primary source', definition: 'A source created during the period or by a participant or direct observer.' }]
}, null, 2);

type Props = { mode: 'documents' | 'models' | 'registry' };
export default function Workbench({ mode }: Props) {
  const [json, setJson] = useState(sample);
  const [templateOptions, setTemplateOptions] = useState<{id:string;name:string;description:string}[]>([]);
  const [templateId, setTemplateId] = useState('royal-gold-book');
  const [status, setStatus] = useState('');
  const [profile, setProfile] = useState('');
  const [provider, setProvider] = useState('openrouter');
  const [modelId, setModelId] = useState('');
  const [modelCatalog, setModelCatalog] = useState<{id:string;name?:string;context_length?:number}[]>([]);
  const [confirmCost, setConfirmCost] = useState(false);
  const [registry, setRegistry] = useState('open_source_projects');
  const [operation, setOperation] = useState('propose_add');
  const [record, setRecord] = useState('{\n  "name_as_written": "Example tool",\n  "official_website_url": "https://example.org"\n}');
  const [reason, setReason] = useState('Add a reviewed candidate to the appropriate workspace.');
  async function loadTemplates() { try { const response=await fetch('/api/v1/documents/templates'); if(response.ok){ const rows=await response.json(); setTemplateOptions(rows); } } catch {} }
  async function chooseTemplate(id:string) { setTemplateId(id); try { const value=JSON.parse(json); value.template_id=id; for(const key of ['font','page_size','margin_inches','include_contents','footer_quote']) delete value[key]; setJson(JSON.stringify(value,null,2)); } catch {} }
  async function renderPDF() {
    setStatus('Rendering PDF…');
    try {
      const payload = JSON.parse(json); payload.template_id = templateId;
      const response = await fetch('/api/v1/documents/render-pdf', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
      if (!response.ok) throw new Error((await response.json()).detail || `HTTP ${response.status}`);
      const blob = await response.blob(); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'kingdom-ai-document.pdf'; a.click(); URL.revokeObjectURL(url); setStatus('PDF created. Check page breaks, citations, font rendering, and long-document output before publication.');
    } catch (e) { setStatus(e instanceof Error ? e.message : 'Could not render PDF.'); }
  }
  async function renderDOCX() {
    setStatus('Rendering editable DOCX…');
    try { const payload=JSON.parse(json); payload.template_id=templateId; const response=await fetch('/api/v1/documents/render-docx',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); if(!response.ok) throw new Error((await response.json()).detail || `HTTP ${response.status}`); const blob=await response.blob(); const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='kingdom-ai-document.docx'; a.click(); URL.revokeObjectURL(url); setStatus('Editable DOCX created. Review page fields and layout in Word or LibreOffice.'); } catch(e) { setStatus(e instanceof Error?e.message:'Could not render DOCX.'); }
  }
  async function analyzeTemplate(file?: File) {
    if (!file) return;
    if (file.size > 20 * 1024 * 1024) { setStatus('Template file exceeds 20 MB.'); return; }
    setStatus('Analyzing reference file…');
    try {
      const bytes = new Uint8Array(await file.arrayBuffer()); let binary = ''; for (let i=0;i<bytes.length;i+=0x8000) binary += String.fromCharCode(...bytes.subarray(i, i+0x8000));
      const response = await fetch('/api/v1/documents/template-profile', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({filename:file.name,content_base64:btoa(binary)})});
      const body = await response.json(); if (!response.ok) throw new Error(body.detail || `HTTP ${response.status}`); setProfile(JSON.stringify(body,null,2)); setStatus('Reference profile extracted; this is a style/layout analysis, not a guarantee of pixel-perfect reproduction.');
    } catch(e) { setStatus(e instanceof Error ? e.message : 'Could not analyze reference file.'); }
  }
  async function loadCatalog() {
    setStatus('Loading live provider catalog…');
    try { const response=await fetch(`/api/v1/system/provider-models?provider=${encodeURIComponent(provider)}`); const body=await response.json(); if(!response.ok) throw new Error(body.detail || `HTTP ${response.status}`); if(body.status!=='passed') throw new Error(body.reason || 'Provider catalog unavailable'); setModelCatalog(body.models || []); setStatus(`Loaded ${body.count_returned || 0} model IDs. Listing a model does not mean it has passed a live response test.`); } catch(e) { setStatus(e instanceof Error ? e.message : 'Could not load provider catalog.'); }
  }
  async function probe() {
    setStatus('Sending one live test request. This may incur provider charges…');
    try { const response = await fetch('/api/v1/system/model-probe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({provider,model_id:modelId,confirm_provider_cost:confirmCost})}); const body=await response.json(); setProfile(JSON.stringify(body,null,2)); if(!response.ok) throw new Error(body.detail || `HTTP ${response.status}`); setStatus(`Model probe status: ${body.status}. A single successful reply does not establish full capability, safety, or reliability.`); }
    catch(e) { setStatus(e instanceof Error ? e.message : 'Probe failed.'); }
  }
  async function validateChange() {
    setStatus('Validating proposed registry change…');
    try { const response=await fetch('/api/v1/registry/changes/validate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({registry,operation,record:JSON.parse(record),reason})}); const body=await response.json(); setProfile(JSON.stringify(body,null,2)); if(!response.ok) throw new Error(body.detail || `HTTP ${response.status}`); setStatus('Proposal validated but not applied. Approval, authentication, and an audit-backed apply workflow are still required.'); }
    catch(e) { setStatus(e instanceof Error ? e.message : 'Could not validate change.'); }
  }
  return <section className="workbench">
    {mode==='documents' && <>
      <div className="workbench-heading"><FileText size={20}/><div><h2>Document & Book Studio</h2><p>Render provided chapter text into a consistent, styled PDF.</p></div></div>
      <div className="notice"><ShieldAlert size={17}/> Template matching is currently a profile-and-review workflow. Exact recreation of arbitrary layouts, embedded art, complex tables, or fonts needs visual QA and may require manual adjustment.</div>
      <label className="field-label">Document template</label><select className="text-input" value={templateId} onFocus={loadTemplates} onChange={e=>chooseTemplate(e.target.value)}><option value="royal-gold-book">Royal Gold Book (default)</option>{templateOptions.filter(t=>t.id!=='royal-gold-book').map(t=><option key={t.id} value={t.id}>{t.name}</option>)}</select>
      <label className="field-label">Manuscript specification (JSON)</label><textarea className="code-editor" value={json} onChange={e=>setJson(e.target.value)} spellCheck={false}/>
      <div className="workbench-actions"><button className="primary-action" onClick={renderPDF}>Render and download PDF</button><button className="secondary-action" onClick={renderDOCX}>Render editable DOCX</button><label className="secondary-action">Analyze template reference<input type="file" accept=".docx,.pdf,.png,.jpg,.jpeg,.webp" onChange={e=>analyzeTemplate(e.target.files?.[0])}/></label></div>
      <p className="help-text">Included renderer features: title page, contents list, A4/Letter/Legal, standard fonts, section headings, page numbering, gold rule with centered diamond, optional footer quote, and optional glossary. The renderer formats content; an LLM must first write and fact-check the actual chapters.</p>
    </>}
    {mode==='models' && <>
      <div className="workbench-heading"><Cpu size={20}/><div><h2>Live Model Verification</h2><p>Test one exact model ID through a configured provider.</p></div></div>
      <div className="notice"><ShieldAlert size={17}/> A live probe sends a request to the provider and may use paid credits. Do not run tests you have not authorized.</div>
      <label className="field-label">Provider</label><select className="text-input" value={provider} onChange={e=>setProvider(e.target.value)}><option value="openrouter">OpenRouter</option><option value="fireworks">Fireworks</option></select>
      <button className="secondary-action" onClick={loadCatalog}>Load live provider catalog</button>
      {modelCatalog.length>0 && <><label className="field-label">Select an exact model ID ({modelCatalog.length} returned)</label><select className="text-input" value={modelId} onChange={e=>setModelId(e.target.value)}><option value="">Choose a model…</option>{modelCatalog.map(m=><option key={m.id} value={m.id}>{m.id}{m.context_length?` · context ${m.context_length}`:''}</option>)}</select></>}
      <label className="field-label">Exact provider model ID</label><input className="text-input" value={modelId} onChange={e=>setModelId(e.target.value)} placeholder="Choose from the live catalog or paste exact ID"/>
      <label className="check-row"><input type="checkbox" checked={confirmCost} onChange={e=>setConfirmCost(e.target.checked)}/> I authorize one live provider request, which may incur charges.</label>
      <button className="primary-action" disabled={!modelId.trim()||!confirmCost} onClick={probe}>Run one live probe</button>
      <p className="help-text">A passing probe only verifies that one short response worked at this moment. Separate tests are needed for tool use, long context, structured output, vision/audio, safety, rate limits, latency, and cost.</p>
    </>}
    {mode==='registry' && <>
      <div className="workbench-heading"><GitPullRequest size={20}/><div><h2>Safe Registry Change</h2><p>Prepare a reviewable change without mutating production data.</p></div></div>
      <label className="field-label">Registry</label><select className="text-input" value={registry} onChange={e=>setRegistry(e.target.value)}><option value="open_source_projects">Open-source / tool candidates</option><option value="models">LLM model candidates</option><option value="tabs">Workspace tabs</option></select>
      <label className="field-label">Change type</label><select className="text-input" value={operation} onChange={e=>setOperation(e.target.value)}><option value="propose_add">Propose add</option><option value="propose_update">Propose update</option></select>
      <label className="field-label">Record JSON</label><textarea className="code-editor short" value={record} onChange={e=>setRecord(e.target.value)} spellCheck={false}/>
      <label className="field-label">Reason / target workspace</label><input className="text-input" value={reason} onChange={e=>setReason(e.target.value)}/>
      <button className="primary-action" onClick={validateChange}>Validate proposal</button>
      <p className="help-text">This currently validates and previews only. It deliberately does not change live registries until authenticated approval, version control, audit logging, tests, and rollback are implemented.</p>
    </>}
    {status && <div className="status-message" role="status">{status}</div>}
    {profile && <><label className="field-label">Result / review profile</label><pre className="result-panel">{profile}</pre></>}
  </section>;
}
