// Keyless web search + page reading that works from Vercel datacenter IPs.
// Strategy: route through r.jina.ai (free reader proxy) which fetches from Jina's
// own servers, bypassing IP blocks. Search = proxied DuckDuckGo HTML; read = reader.
export type WebResult = { title: string; url: string; snippet: string };

const JINA = "https://r.jina.ai/";

function decodeDDG(href: string): string {
  try {
    const u = new URL(href);
    const uddg = u.searchParams.get("uddg");
    return uddg ? decodeURIComponent(uddg) : href;
  } catch { return href; }
}

async function jget(target: string, ms = 15000): Promise<string> {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), ms);
  try {
    const r = await fetch(JINA + target, { headers: { "User-Agent": "Mozilla/5.0", "X-Return-Format": "markdown" }, signal: c.signal });
    return r.ok ? await r.text() : "";
  } catch { return ""; } finally { clearTimeout(t); }
}

export async function webSearch(query: string, limit = 6): Promise<WebResult[]> {
  const md = await jget("https://html.duckduckgo.com/html/?q=" + encodeURIComponent(query));
  if (!md) return [];
  const out: WebResult[] = [];
  const seen = new Set<string>();
  const re = /\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g;
  let m;
  while ((m = re.exec(md)) && out.length < limit) {
    const title = m[1].trim();
    let url = m[2];
    if (url.includes("duckduckgo.com/l/?uddg=")) url = decodeDDG(url);
    if (!/^https?:\/\//.test(url)) continue;
    if (/duckduckgo\.com|jina\.ai|w3\.org|gstatic|improving\.duckduckgo/.test(url)) continue;
    if (!title || title.length < 3) continue;
    if (seen.has(url)) continue;
    seen.add(url);
    out.push({ title, url, snippet: "" });
  }
  return out;
}

export async function fetchPage(url: string, maxChars = 4000): Promise<string> {
  const md = await jget(url, 12000);
  return md.replace(/\n{3,}/g, "\n\n").slice(0, maxChars);
}

export async function webContext(query: string, depth = 3): Promise<string> {
  const results = await webSearch(query, 6);
  if (!results.length) return "";
  const top = results.slice(0, depth);
  const pages = await Promise.all(top.map((r) => fetchPage(r.url, 1200)));
  const lines = results.map((r, i) => `- ${r.title} (${r.url})${pages[i] ? "\n  " + pages[i].replace(/\n/g, " ").slice(0, 600) : ""}`);
  return "Live web results:\n" + lines.join("\n");
}
