import { webContext } from "./websearch";
// Deep Research Ensemble — OPEN SOURCE edition.
// Stacks multiple open-weight research models in parallel via free OpenAI-compatible
// hosts, adds keyless scholarly sources (arXiv, Semantic Scholar), then synthesizes
// one merged report. No paid subscription required.
//
// Hosts (any subset; a single free key unlocks several models):
//   GROQ_API_KEY         -> Llama 3.3 70B, DeepSeek-R1-Distill 70B, Qwen (free tier)
//   OPENROUTER_API_KEY   -> Llama / DeepSeek / Qwen ":free" models
//   HF_TOKEN             -> Hugging Face open models
//   OBLITERATUS_GATEWAY_URL -> self-hosted Hermes (fully open, no third party)
// Scholarly sources (arXiv, Semantic Scholar) always run, keyless.
type ProviderOut = { id: string; label: string; text: string; ok: boolean };
const E = process.env;

async function openAICompatible(base: string, key: string, model: string, prompt: string, extraHeaders: Record<string, string> = {}) {
  const r = await fetch(base.replace(/\/$/, "") + "/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${key}`, ...extraHeaders },
    body: JSON.stringify({ model, messages: [
      { role: "system", content: "You are an elite deep-research analyst. Produce a rigorous, well-sourced briefing." },
      { role: "user", content: prompt }], temperature: 0.3 }),
  });
  if (!r.ok) throw new Error(`${r.status} ${(await r.text()).slice(0, 160)}`);
  return (await r.json())?.choices?.[0]?.message?.content ?? "";
}

type Spec = { id: string; label: string; run: (q: string) => Promise<string> };

function csv(v: string | undefined, fallback: string[]) {
  return (v ? v.split(",").map((s) => s.trim()).filter(Boolean) : fallback);
}

function specs(): Spec[] {
  const list: Spec[] = [];
  // Groq free tier — open-weight models, one key stacks several.
  if (E.GROQ_API_KEY) {
    for (const m of csv(E.GROQ_MODELS, ["llama-3.3-70b-versatile", "deepseek-r1-distill-llama-70b", "qwen-2.5-32b"])) {
      list.push({ id: `groq:${m}`, label: `Groq · ${m}`, run: (q) => openAICompatible("https://api.groq.com/openai/v1", E.GROQ_API_KEY!, m, q) });
    }
  }
  // OpenRouter free ":free" open models.
  if (E.OPENROUTER_API_KEY) {
    for (const m of csv(E.OPENROUTER_MODELS, ["meta-llama/llama-3.3-70b-instruct:free", "deepseek/deepseek-r1:free", "qwen/qwen-2.5-72b-instruct:free"])) {
      list.push({ id: `or:${m}`, label: `OpenRouter · ${m}`, run: (q) => openAICompatible("https://openrouter.ai/api/v1", E.OPENROUTER_API_KEY!, m, q, { "HTTP-Referer": "https://obi-ai-delta.vercel.app", "X-Title": "Obi AI" }) });
    }
  }
  // Hugging Face router (open models).
  if (E.HF_TOKEN) {
    for (const m of csv(E.HF_MODELS, ["meta-llama/Llama-3.3-70B-Instruct"])) {
      list.push({ id: `hf:${m}`, label: `HuggingFace · ${m}`, run: (q) => openAICompatible("https://router.huggingface.co/v1", E.HF_TOKEN!, m, q) });
    }
  }
  // Self-hosted open Hermes gateway.
  if (E.OBLITERATUS_GATEWAY_URL) {
    list.push({ id: "obliteratus", label: "Obliteratus Hermes (self-hosted)", run: (q) => openAICompatible((E.OBLITERATUS_GATEWAY_URL || "") + "/v1", E.OBLITERATUS_API_KEY || "x", E.OBLITERATUS_MODEL || "obliteratus-hermes-3-70b", q) });
  }
  return list;
}

async function academic(query: string): Promise<string> {
  const out: string[] = [];
  try {
    const r = await fetch(`https://api.semanticscholar.org/graph/v1/paper/search?query=${encodeURIComponent(query)}&limit=5&fields=title,abstract,year,url`);
    if (r.ok) for (const p of (await r.json()).data || []) out.push(`[Semantic Scholar ${p.year || ""}] ${p.title}: ${(p.abstract || "").slice(0, 240)} (${p.url || ""})`);
  } catch {}
  try {
    const r = await fetch(`http://export.arxiv.org/api/query?search_query=all:${encodeURIComponent(query)}&max_results=4`);
    if (r.ok) {
      const xml = await r.text();
      const titles = [...xml.matchAll(/<title>([\s\S]*?)<\/title>/g)].slice(1).map((m) => m[1].trim());
      const sums = [...xml.matchAll(/<summary>([\s\S]*?)<\/summary>/g)].map((m) => m[1].trim());
      titles.forEach((t, i) => out.push(`[arXiv] ${t}: ${(sums[i] || "").slice(0, 240)}`));
    }
  } catch {}
  return out.length ? out.join("\n") : "";
}

export async function deepResearch(query: string) {
  const enabled = specs();
  const [academicCtx, webCtx, results] = await Promise.all([
    academic(query),
    webContext(query, 3).catch(() => ""),
    Promise.all(enabled.map(async (s): Promise<ProviderOut> => {
      try { return { id: s.id, label: s.label, text: await s.run(query), ok: true }; }
      catch (e: any) { return { id: s.id, label: s.label, text: `(failed: ${e?.message || e})`, ok: false }; }
    })),
  ]);
  const good = results.filter((r) => r.ok && r.text.trim());
  const findings = good.map((r) => `### Source model: ${r.label}\n${r.text}`).join("\n\n");
  const synth = enabled[0];
  const synthPrompt = `You are the lead synthesizer. Merge the independent open-source model outputs below into ONE authoritative briefing on:\n"${query}"\n\nRules: integrate agreements, explicitly flag disagreements/uncertainty, dedupe, and cite which model or scholarly source supports each major claim. End with "Confidence" and "Open questions" sections.\n\n` + (webCtx ? `## Live web\n${webCtx}\n\n` : "") + (academicCtx ? `## Scholarly sources\n${academicCtx}\n\n` : "") + `## Model findings\n${findings || "(no model findings available)"}`;
  let report = "";
  if (synth && good.length) { try { report = await synth.run(synthPrompt); } catch (e: any) { report = `Synthesis failed (${e?.message || e}). Raw findings below:\n\n${findings}`; } }
  else if (academicCtx) report = `No open-source model host is configured yet, but here are keyless scholarly sources:\n\n${academicCtx}\n\nAdd a free GROQ_API_KEY (or OPENROUTER_API_KEY / HF_TOKEN) to stack open models.`;
  else report = "No research sources available. Add a free open-source model key (GROQ_API_KEY recommended).";
  return { report, contributors: results.map((r) => ({ id: r.id, label: r.label, ok: r.ok })), academicSources: academicCtx ? academicCtx.split("\n").length : 0, stacked: enabled.length };
}
