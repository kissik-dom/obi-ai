import { NextRequest, NextResponse } from "next/server";
import { deepResearch } from "@/lib/research-ensemble";
export const runtime = "nodejs";
export const maxDuration = 60;
// Deep research ensemble: stacks all configured research-grade models + scholarly sources.
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const query = typeof body?.query === "string" ? body.query.trim() : "";
    const tab = typeof body?.tab === "string" ? body.tab.trim() : "";
    if (!query) return NextResponse.json({ error: "query required" }, { status: 400 });
    const researchQuery = tab ? `Domain context: ${tab}\n\n${query}` : query;
    const out = await deepResearch(researchQuery);
    return NextResponse.json(out);
  } catch (err: any) { return NextResponse.json({ error: err?.message || "error" }, { status: 500 }); }
}
