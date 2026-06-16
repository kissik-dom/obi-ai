import { NextRequest, NextResponse } from "next/server";
import { runAgent } from "@/lib/swarm";
export const runtime = "nodejs";
export const maxDuration = 60;
export async function POST(req: NextRequest) {
  try {
    const { data, question } = await req.json();
    if (!data) return NextResponse.json({ error: "data required" }, { status: 400 });
    const sample = typeof data === "string" ? data.slice(0, 8000) : JSON.stringify(data).slice(0, 8000);
    const res = await runAgent("analyst", [{ role: "user", content: `Analyze this dataset. Identify patterns, summary stats, anomalies, and insights.${question ? ` Focus question: ${question}.` : ""}\n\nData:\n${sample}` }]);
    return NextResponse.json({ analysis: res.text, provider: res.provider });
  } catch (err: any) { return NextResponse.json({ error: err?.message || "error" }, { status: 500 }); }
}
