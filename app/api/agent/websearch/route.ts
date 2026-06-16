import { NextRequest, NextResponse } from "next/server";
import { webSearch, webContext } from "@/lib/websearch";
export const runtime = "nodejs";
export const maxDuration = 60;
export async function POST(req: NextRequest) {
  try {
    const { query, read } = await req.json();
    if (!query) return NextResponse.json({ error: "query required" }, { status: 400 });
    if (read) return NextResponse.json({ context: await webContext(query, 3) });
    return NextResponse.json({ results: await webSearch(query, 8) });
  } catch (e: any) { return NextResponse.json({ error: e?.message || "error" }, { status: 500 }); }
}
