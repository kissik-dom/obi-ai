import { NextRequest, NextResponse } from "next/server";
import { runAgent } from "@/lib/swarm";
export const runtime = "nodejs";
export const maxDuration = 60;
export async function POST(req: NextRequest) {
  try {
    const { series, horizon = 5, context } = await req.json();
    if (!series) return NextResponse.json({ error: "series required" }, { status: 400 });
    const sample = typeof series === "string" ? series.slice(0, 6000) : JSON.stringify(series).slice(0, 6000);
    const res = await runAgent("predictor", [{ role: "user", content: `Forecast the next ${horizon} periods. Give point estimates, ranges, assumptions, and confidence.${context ? ` Context: ${context}.` : ""}\n\nSeries:\n${sample}` }]);
    return NextResponse.json({ forecast: res.text, horizon, provider: res.provider });
  } catch (err: any) { return NextResponse.json({ error: err?.message || "error" }, { status: 500 }); }
}
