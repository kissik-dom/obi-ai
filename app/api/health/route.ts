import { NextResponse } from "next/server";
import { cascadeProviders } from "@/lib/cascade";

export const runtime = "nodejs";

export async function GET() {
  const providers = cascadeProviders();
  return NextResponse.json({
    status: "ok",
    service: "obi-ai",
    providersConfigured: providers.length,
    providers,
    timestamp: new Date().toISOString(),
  });
}
