import { NextRequest, NextResponse } from "next/server";
import { presignPut, storageConfigured } from "@/lib/storage";
export const runtime = "nodejs";
export async function POST(req: NextRequest) {
  if (!storageConfigured()) return NextResponse.json({ configured: false });
  try {
    const { name, type } = await req.json();
    if (!name) return NextResponse.json({ error: "name required" }, { status: 400 });
    const r = await presignPut(name, type || "application/octet-stream");
    return NextResponse.json({ configured: true, ...r });
  } catch (e: any) { return NextResponse.json({ error: e?.message || "error" }, { status: 500 }); }
}
export async function GET() { return NextResponse.json({ configured: storageConfigured() }); }
