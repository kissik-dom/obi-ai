// Obi AI LLM entry point — delegates to the Obliteratus Hermes Gateway cascade.
import { cascadeChat, cascadeProviders, CascadeResult, ChatMessage as CM } from "./cascade";
export type ChatMessage = CM;
export type LLMResult = { text: string; provider: string; model: string };

export function activeProvider(): string {
  const p = cascadeProviders();
  return p.length ? p[0].split(":")[0] : "mock";
}

export async function chat(messages: ChatMessage[], opts: { temperature?: number } = {}): Promise<LLMResult> {
  const r: CascadeResult = await cascadeChat(messages, opts.temperature ?? 0.7);
  return { text: r.text, provider: r.provider, model: r.model };
}
