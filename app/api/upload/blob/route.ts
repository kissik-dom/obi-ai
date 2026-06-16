import { handleUpload, type HandleUploadBody } from "@vercel/blob/client";
import { NextRequest, NextResponse } from "next/server";
export const runtime = "nodejs";
// Vercel Blob client-upload authorizer. Browser uploads directly to Blob storage,
// bypassing the serverless body limit — unlimited large images/videos/files.
export async function POST(req: NextRequest) {
  const body = (await req.json()) as HandleUploadBody;
  try {
    const json = await handleUpload({
      body,
      request: req,
      onBeforeGenerateToken: async () => ({
        addRandomSuffix: true,
        maximumSizeInBytes: 5 * 1024 * 1024 * 1024, // 5 GB per file
      }),
      onUploadCompleted: async () => {},
    });
    return NextResponse.json(json);
  } catch (e: any) {
    return NextResponse.json({ error: e?.message || "upload error" }, { status: 400 });
  }
}
