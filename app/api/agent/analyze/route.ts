import { NextRequest, NextResponse } from "next/server";
import { chat } from "@/lib/llm";
import { AGENTS } from "@/lib/swarm";

export const runtime = "nodejs";
export const maxDuration = 60;

function parseJsonObject(text: string): Record<string, unknown> | null {
  try {
    const cleaned = text.replace(/```(?:json)?/gi, "").trim();
    const start = cleaned.indexOf("{");
    const end = cleaned.lastIndexOf("}");
    if (start === -1 || end === -1 || end <= start) return null;
    const parsed: unknown = JSON.parse(cleaned.slice(start, end + 1));
    return parsed && typeof parsed === "object" && !Array.isArray(parsed)
      ? (parsed as Record<string, unknown>)
      : null;
  } catch {
    return null;
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const query = typeof body?.query === "string" ? body.query.trim() : "";
    const tab = typeof body?.tab === "string" ? body.tab.trim() : "";
    if (!query) return NextResponse.json({ error: "query required" }, { status: 400 });

    const prompt = `Analyze the following request${tab ? ` in the context of the "${tab}" tab` : ""}.\n\n${query}\n\nReturn ONLY a JSON object with these keys: "analysis" (string), "confidence" (one of low, medium, or high), and "sources" (array of strings).`;
    const res = await chat(
      [{ role: "system", content: AGENTS.analyst.system }, { role: "user", content: prompt }],
      { temperature: 0.3 },
    );

    const parsed = parseJsonObject(res.text);
    return NextResponse.json({
      analysis: typeof parsed?.analysis === "string" ? parsed.analysis : res.text,
      confidence: typeof parsed?.confidence === "string" ? parsed.confidence : "medium",
      sources: Array.isArray(parsed?.sources)
        ? parsed.sources.filter((source): source is string => typeof source === "string")
        : [],
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Analysis failed.";
    console.error("Obi AI analysis request failed", { message });
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
