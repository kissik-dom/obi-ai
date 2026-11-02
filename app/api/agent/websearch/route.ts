import { NextRequest, NextResponse } from "next/server";
import { webSearch } from "@/lib/websearch";

export const runtime = "nodejs";
export const maxDuration = 60;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const query = typeof body?.query === "string" ? body.query.trim() : "";
    if (!query) return NextResponse.json({ error: "query required" }, { status: 400 });

    const results = await webSearch(query, 8);
    return NextResponse.json({ results });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Web search failed.";
    console.error("Obi AI web search request failed", { message });
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
