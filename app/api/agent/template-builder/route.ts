import { NextRequest, NextResponse } from "next/server";
import { runAgent } from "@/lib/swarm";
export const runtime = "nodejs";
export const maxDuration = 60;
const templates = new Map<string, { name: string; body: string; createdAt: string }>();
export async function GET() { return NextResponse.json({ templates: Array.from(templates.values()) }); }
export async function POST(req: NextRequest) {
  try {
    const { name, instructions } = await req.json();
    if (!name || !instructions) return NextResponse.json({ error: "name and instructions required" }, { status: 400 });
    const res = await runAgent("document", [{ role: "user", content: `Build a reusable template named "${name}". Use {{placeholder}} tokens for variable fields. Instructions: ${instructions}` }]);
    const tpl = { name, body: res.text, createdAt: new Date().toISOString() };
    templates.set(name, tpl);
    return NextResponse.json({ template: tpl, provider: res.provider });
  } catch (err: any) { return NextResponse.json({ error: err?.message || "error" }, { status: 500 }); }
}
