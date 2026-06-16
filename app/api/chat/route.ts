import { NextRequest, NextResponse } from "next/server";
import { swarm } from "@/lib/swarm";
import { ChatMessage } from "@/lib/llm";
export const runtime = "nodejs";
export const maxDuration = 60;
export async function POST(req: NextRequest) {
  try {
    const { messages } = (await req.json()) as { messages: ChatMessage[] };
    if (!Array.isArray(messages) || messages.length === 0) return NextResponse.json({ error: "messages[] required" }, { status: 400 });
    const result = await swarm(messages);
    return NextResponse.json({ text: result.text, agent: result.agent, label: result.label, provider: result.provider, model: result.model });
  } catch (err: any) { return NextResponse.json({ error: err?.message || "error" }, { status: 500 }); }
}
