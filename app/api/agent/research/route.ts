import { NextRequest, NextResponse } from "next/server";
import { deepResearch } from "@/lib/research-ensemble";
export const runtime = "nodejs";
export const maxDuration = 60;
// Deep research ensemble: stacks all configured research-grade models + scholarly sources.
export async function POST(req: NextRequest) {
  try {
    const { query } = await req.json();
    if (!query) return NextResponse.json({ error: "query required" }, { status: 400 });
    const out = await deepResearch(query);
    return NextResponse.json(out);
  } catch (err: any) { return NextResponse.json({ error: err?.message || "error" }, { status: 500 }); }
}
