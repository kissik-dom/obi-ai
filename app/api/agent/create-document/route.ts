import { NextRequest, NextResponse } from "next/server";
import { chat } from "@/lib/llm";
import { AGENTS } from "@/lib/swarm";

export const runtime = "nodejs";
export const maxDuration = 60;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const title = typeof body?.title === "string" ? body.title.trim() : "";
    const outline = typeof body?.outline === "string" ? body.outline.trim() : "";
    const tab = typeof body?.tab === "string" ? body.tab.trim() : "";
    if (!title) return NextResponse.json({ error: "title required" }, { status: 400 });

    const prompt = `Create a professional document titled "${title}".${tab ? ` Domain context: ${tab}.` : ""}${outline ? `\n\nUse this outline:\n${outline}` : ""}\n\nUse markdown headings (#, ##) for structure.`;
    const res = await chat(
      [{ role: "system", content: AGENTS.document.system }, { role: "user", content: prompt }],
      { temperature: 0.6 },
    );

    return NextResponse.json({ document: res.text, title });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Document creation failed.";
    console.error("Obi AI document request failed", { message });
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
