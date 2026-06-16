import { NextRequest, NextResponse } from "next/server";
import { cascadeChat, ChatMessage } from "@/lib/cascade";
export const runtime = "nodejs";
export const maxDuration = 60;

// Obliteratus Hermes Gateway — OpenAI-compatible /v1/chat/completions.
// Point any client (including Obi AI's OBLITERATUS_GATEWAY_URL) at this endpoint.
export async function POST(req: NextRequest) {
  // Optional bearer auth: set OBLITERATUS_API_KEY to require it.
  const required = process.env.OBLITERATUS_API_KEY;
  if (required) {
    const auth = req.headers.get("authorization") || "";
    if (auth !== `Bearer ${required}`) return NextResponse.json({ error: { message: "unauthorized" } }, { status: 401 });
  }
  try {
    const body = await req.json();
    const messages = (body.messages || []) as ChatMessage[];
    if (!Array.isArray(messages) || !messages.length) return NextResponse.json({ error: { message: "messages[] required" } }, { status: 400 });
    const r = await cascadeChat(messages, body.temperature ?? 0.7);
    return NextResponse.json({
      id: "obli-" + Date.now(),
      object: "chat.completion",
      created: Math.floor(Date.now() / 1000),
      model: `obliteratus-hermes/${r.provider}/${r.model}`,
      choices: [{ index: 0, message: { role: "assistant", content: r.text }, finish_reason: "stop" }],
      usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 },
    });
  } catch (e: any) {
    return NextResponse.json({ error: { message: e?.message || "error" } }, { status: 500 });
  }
}

export async function GET() {
  const { cascadeProviders } = await import("@/lib/cascade");
  return NextResponse.json({ gateway: "obliteratus-hermes", status: "ok", cascade: cascadeProviders() });
}
