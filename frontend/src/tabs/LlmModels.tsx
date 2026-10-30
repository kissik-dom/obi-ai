import { useState } from "react";
import { GRAMMAR, useKingdomStore } from "../store/useKingdomStore";

type SectionName = (typeof GRAMMAR)[number];
type Accent = "magenta" | "turquoise" | "orange";

function Section({ name, accent }: { name: SectionName; accent: Accent }) {
  const sample: Record<SectionName, string> = {
    Chat: `Chat surface for LLM/Models`,
    Agents: `BugFix, Testing, External Scout, Internal Optimizer, CUA Fleet`,
    "Open Tasks": `GET /api/llm/tasks/open`,
    "Completed Tasks": `GET /api/llm/tasks/completed`,
    Training: `knowledge/llm/training`,
    Knowledge: `qdrant:llm`,
    Files: `kingdom-sandboxes-llm`,
    Tools: `docs/TOOL_REGISTRY.md`,
    Outputs: `finished/llm`,
    Settings: `PUT /api/llm/settings`,
  };

  return (
    <section className="grammar-section">
      <h2 style={{ color: `var(--kingdom-${accent})` }}>{name}</h2>
      <code>{sample[name]}</code>
      <CopyButton text={sample[name]} />
    </section>
  );
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const setCopiedCode = useKingdomStore((state) => state.setCopiedCode);

  const copy = async () => {
    await navigator.clipboard.writeText(text);
    setCopiedCode(text);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 900);
  };

  return (
    <button type="button" className="copy-button" onClick={copy}>
      {copied ? "Copied" : "Copy"}
    </button>
  );
}

export default function LlmModels() {
  const turnoffFlags = useKingdomStore((state) => state.turnoffFlags);
  const setTurnoffFlag = useKingdomStore((state) => state.setTurnoffFlag);

  return (
    <div className="tab-surface">
      <header className="tab-header header-turquoise">
        <h1>LLM/Models</h1>
        <p>Model registry, Tier S/B/V routing, 10-key OpenRouter fallback, VRAM filters.</p>
      </header>

      <div className="grammar-grid">
        {GRAMMAR.map((name) => (
          <Section key={name} name={name} accent="turquoise" />
        ))}
      </div>

      <section className="grammar-section">
        <h2>Turn-off flags</h2>
        <div className="status-row">
          {Object.entries(turnoffFlags).map(([service, enabled]) => (
            <button
              key={service}
              type="button"
              className="flag-button"
              aria-pressed={enabled}
              onClick={() => setTurnoffFlag(service, !enabled)}
            >
              {service}: {enabled ? "on" : "off"}
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}
