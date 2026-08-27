import { NextRequest, NextResponse } from "next/server";
import { swarm } from "@/lib/swarm";
import { ChatMessage } from "@/lib/llm";

export const runtime = "nodejs";
export const maxDuration = 60;

const MAX_MESSAGES = 24;
const MAX_MESSAGE_CHARS = 12_000;
const MAX_TOTAL_CHARS = 48_000;
const VALID_ROLES = new Set<ChatMessage["role"]>(["system", "user", "assistant"]);

function parseMessages(value: unknown): ChatMessage[] | null {
  if (!Array.isArray(value) || value.length === 0 || value.length > MAX_MESSAGES) {
    return null;
  }

  const messages: ChatMessage[] = [];
  let totalChars = 0;
  for (const item of value) {
    if (
      !item ||
      typeof item !== "object" ||
      !("role" in item) ||
      !("content" in item) ||
      typeof item.role !== "string" ||
      typeof item.content !== "string" ||
      !VALID_ROLES.has(item.role as ChatMessage["role"])
    ) {
      return null;
    }
    const content = item.content.trim();
    if (!content || content.length > MAX_MESSAGE_CHARS) {
      return null;
    }
    totalChars += content.length;
    if (totalChars > MAX_TOTAL_CHARS) {
      return null;
    }
    messages.push({ role: item.role as ChatMessage["role"], content });
  }
  return messages;
}

export async function POST(req: NextRequest) {
  try {
    const body: unknown = await req.json();
    const messages = parseMessages(
      body && typeof body === "object" && "messages" in body ? body.messages : undefined,
    );
    if (!messages) {
      return NextResponse.json(
        { error: "Provide 1–24 non-empty chat messages within the request size limit." },
        { status: 400 },
      );
    }

    const result = await swarm(messages);
    return NextResponse.json({
      text: result.text,
      agent: result.agent,
      label: result.label,
      provider: result.provider,
      model: result.model,
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unexpected chat-service error.";
    const unavailable = message === "No AI provider is configured for this deployment." ||
      message === "All configured AI providers are currently unavailable.";
    console.error("Obi AI chat request failed", { unavailable, message });
    return NextResponse.json(
      { error: unavailable ? "The AI service is temporarily unavailable. Please try again later." : "The chat request could not be completed." },
      { status: unavailable ? 503 : 500 },
    );
  }
}
