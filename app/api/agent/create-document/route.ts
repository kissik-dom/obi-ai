import { NextRequest, NextResponse } from "next/server";
import { runAgent } from "@/lib/swarm";
import { generatePdf } from "@/lib/pdf";
export const runtime = "nodejs";
export const maxDuration = 60;
export async function POST(req: NextRequest) {
  try {
    const { prompt, type = "document", format = "text", pages = 1, title } = await req.json();
    if (!prompt) return NextResponse.json({ error: "prompt required" }, { status: 400 });
    const length = pages >= 50 ? "This must be a full-length, ~100 page document. Be exhaustive with sections, subsections and detail." : pages > 1 ? `Target roughly ${pages} pages of content.` : "Keep it appropriately concise.";
    const res = await runAgent("document", [{ role: "user", content: `Create a ${type}. ${length}\nUse markdown headings (#, ##) for structure.\n\nRequest: ${prompt}` }]);
    const docTitle = title || `${type[0].toUpperCase()}${type.slice(1)}`;
    if (format === "pdf") {
      const bytes = await generatePdf(docTitle, res.text);
      return new NextResponse(Buffer.from(bytes), { headers: { "Content-Type": "application/pdf", "Content-Disposition": `attachment; filename="${docTitle.replace(/\s+/g, "_")}.pdf"` } });
    }
    return NextResponse.json({ title: docTitle, content: res.text, provider: res.provider, model: res.model });
  } catch (err: any) { return NextResponse.json({ error: err?.message || "error" }, { status: 500 }); }
}
