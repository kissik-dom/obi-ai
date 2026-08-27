// Obliteratus Hermes Gateway — never-fail LLM cascade.
// Tries open-source inference providers in order; returns the first success.
// Each provider runs only if its API key env var is set. Groq is intentionally
// last (the team's Groq keys are dead). Add more keys to widen the cascade.
export type ChatMessage = { role: "system" | "user" | "assistant"; content: string };
export type CascadeResult = { text: string; provider: string; model: string };
const E = process.env;
const PER_TRY_MS = 13000;

async function withTimeout<T>(p: (signal: AbortSignal) => Promise<T>, ms = PER_TRY_MS): Promise<T> {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), ms);
  try { return await p(c.signal); } finally { clearTimeout(t); }
}

async function oai(base: string, key: string, model: string, messages: ChatMessage[], temperature: number, extra: Record<string, string> = {}) {
  return withTimeout(async (signal) => {
    const r = await fetch(base.replace(/\/$/, "") + "/chat/completions", {
      method: "POST", signal,
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${key}`, ...extra },
      body: JSON.stringify({ model, messages, temperature }),
    });
    if (!r.ok) throw new Error(`${r.status} ${(await r.text()).slice(0, 120)}`);
    const t = (await r.json())?.choices?.[0]?.message?.content ?? "";
    if (!t.trim()) throw new Error("empty");
    return t;
  });
}

async function gemini(key: string, model: string, messages: ChatMessage[], temperature: number) {
  return withTimeout(async (signal) => {
    const sys = messages.filter((m) => m.role === "system").map((m) => m.content).join("\n");
    const contents = messages.filter((m) => m.role !== "system").map((m) => ({ role: m.role === "assistant" ? "model" : "user", parts: [{ text: m.content }] }));
    const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`, {
      method: "POST", signal, headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ systemInstruction: sys ? { parts: [{ text: sys }] } : undefined, contents, generationConfig: { temperature } }),
    });
    if (!r.ok) throw new Error(`${r.status} ${(await r.text()).slice(0, 120)}`);
    const t = ((await r.json())?.candidates?.[0]?.content?.parts || []).map((p: any) => p.text || "").join("");
    if (!t.trim()) throw new Error("empty");
    return t;
  });
}

type Attempt = { provider: string; model: string; call: (m: ChatMessage[], t: number) => Promise<string> };

function keys(name: string): string[] {
  return [E[name], E[name + "_2"], E[name + "_3"]].filter(Boolean) as string[];
}

function plan(): Attempt[] {
  const a: Attempt[] = [];
  // Primary hosted Obliteratus gateway, when a valid deployment URL and server-side key are configured.
  if (E.OBLITERATUS_GATEWAY_URL && E.OBLITERATUS_API_KEY) {
    const gatewayBase = E.OBLITERATUS_GATEWAY_URL.replace(/\/$/, "");
    a.push({
      provider: "obliteratus",
      model: E.OBLITERATUS_MODEL || "obliteratus-hermes-3-70b",
      call: (m, t) => oai(`${gatewayBase}${gatewayBase.endsWith("/v1") ? "" : "/v1"}`, E.OBLITERATUS_API_KEY!, E.OBLITERATUS_MODEL || "obliteratus-hermes-3-70b", m, t),
    });
  }
  // Self-hosted Hermes (their GPU/vLLM) first if configured and not pointing back at us.
  if (E.HERMES_GPU_URL) a.push({ provider: "hermes-gpu", model: E.HERMES_GPU_MODEL || "hermes-3-70b", call: (m, t) => oai(E.HERMES_GPU_URL!.replace(/\/$/, "") + "/v1", E.HERMES_GPU_KEY || "x", E.HERMES_GPU_MODEL || "hermes-3-70b", m, t) });
  for (const k of keys("SAMBANOVA_API_KEY")) a.push({ provider: "sambanova", model: E.SAMBANOVA_MODEL || "Meta-Llama-3.3-70B-Instruct", call: (m, t) => oai("https://api.sambanova.ai/v1", k, E.SAMBANOVA_MODEL || "Meta-Llama-3.3-70B-Instruct", m, t) });
  for (const k of keys("OPENROUTER_API_KEY")) a.push({ provider: "openrouter", model: E.OPENROUTER_MODEL || "meta-llama/llama-3.3-70b-instruct:free", call: (m, t) => oai("https://openrouter.ai/api/v1", k, E.OPENROUTER_MODEL || "meta-llama/llama-3.3-70b-instruct:free", m, t, { "HTTP-Referer": "https://obi-ai-delta.vercel.app", "X-Title": "Obi AI" }) });
  for (const k of keys("CEREBRAS_API_KEY")) a.push({ provider: "cerebras", model: E.CEREBRAS_MODEL || "llama-3.3-70b", call: (m, t) => oai("https://api.cerebras.ai/v1", k, E.CEREBRAS_MODEL || "llama-3.3-70b", m, t) });
  for (const k of keys("TOGETHER_API_KEY")) a.push({ provider: "together", model: E.TOGETHER_MODEL || "meta-llama/Llama-3.3-70B-Instruct-Turbo", call: (m, t) => oai("https://api.together.xyz/v1", k, E.TOGETHER_MODEL || "meta-llama/Llama-3.3-70B-Instruct-Turbo", m, t) });
  for (const k of keys("DEEPINFRA_API_KEY")) a.push({ provider: "deepinfra", model: E.DEEPINFRA_MODEL || "meta-llama/Llama-3.3-70B-Instruct", call: (m, t) => oai("https://api.deepinfra.com/v1/openai", k, E.DEEPINFRA_MODEL || "meta-llama/Llama-3.3-70B-Instruct", m, t) });
  for (const k of keys("FIREWORKS_API_KEY")) a.push({ provider: "fireworks", model: E.FIREWORKS_MODEL || "accounts/fireworks/models/llama-v3p3-70b-instruct", call: (m, t) => oai("https://api.fireworks.ai/inference/v1", k, E.FIREWORKS_MODEL || "accounts/fireworks/models/llama-v3p3-70b-instruct", m, t) });
  for (const k of keys("FEATHERLESS_API_KEY")) a.push({ provider: "featherless", model: E.FEATHERLESS_MODEL || "meta-llama/Meta-Llama-3.1-8B-Instruct", call: (m, t) => oai("https://api.featherless.ai/v1", k, E.FEATHERLESS_MODEL || "meta-llama/Meta-Llama-3.1-8B-Instruct", m, t) });
  for (const k of keys("HF_TOKEN")) a.push({ provider: "huggingface", model: E.HF_MODEL || "meta-llama/Llama-3.3-70B-Instruct", call: (m, t) => oai("https://router.huggingface.co/v1", k, E.HF_MODEL || "meta-llama/Llama-3.3-70B-Instruct", m, t) });
  for (const k of keys("GEMINI_API_KEY")) a.push({ provider: "gemini", model: E.GEMINI_MODEL || "gemini-2.0-flash", call: (m, t) => gemini(k, E.GEMINI_MODEL || "gemini-2.0-flash", m, t) });
  for (const k of keys("GROQ_API_KEY")) a.push({ provider: "groq", model: E.GROQ_MODEL || "llama-3.3-70b-versatile", call: (m, t) => oai("https://api.groq.com/openai/v1", k, E.GROQ_MODEL || "llama-3.3-70b-versatile", m, t) });
  return a;
}

export function cascadeProviders(): string[] { return plan().map((a) => `${a.provider}:${a.model}`); }

export async function cascadeChat(messages: ChatMessage[], temperature = 0.7): Promise<CascadeResult> {
  const attempts = plan();
  const errors: string[] = [];
  for (const at of attempts) {
    try {
      const text = await at.call(messages, temperature);
      return { text, provider: at.provider, model: at.model };
    } catch (e: any) {
      errors.push(`${at.provider}: ${e?.message || e}`);
    }
  }
  const summary = attempts.length
    ? "All configured AI providers are currently unavailable."
    : "No AI provider is configured for this deployment.";
  console.error("Obi AI cascade unavailable", { attemptedProviders: attempts.map((attempt) => attempt.provider), errors });
  throw new Error(summary);
}
