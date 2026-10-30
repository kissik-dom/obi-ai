import { useState } from "react";
import { GRAMMAR, useKingdomStore } from "../store/useKingdomStore";

type SectionName = (typeof GRAMMAR)[number];
type Accent = "magenta" | "turquoise" | "orange";

function Section({ name, accent }: { name: SectionName; accent: Accent }) {
  const sample: Record<SectionName, string> = {
    Chat: `Chat surface for Engineering GHIDRA Anti-Gravity`,
    Agents: `BugFix, Testing, External Scout, Internal Optimizer, CUA Fleet`,
    "Open Tasks": `GET /api/engineering_ghidra/tasks/open`,
    "Completed Tasks": `GET /api/engineering_ghidra/tasks/completed`,
    Training: `knowledge/engineering_ghidra/training`,
    Knowledge: `qdrant:engineering_ghidra`,
    Files: `kingdom-sandboxes-engineering_ghidra`,
    Tools: `docs/TOOL_REGISTRY.md`,
    Outputs: `finished/engineering_ghidra`,
    Settings: `PUT /api/engineering_ghidra/settings`,
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

export default function EngineeringGhidraAntiGravity() {
  const turnoffFlags = useKingdomStore((state) => state.turnoffFlags);
  const setTurnoffFlag = useKingdomStore((state) => state.setTurnoffFlag);

  return (
    <div className="tab-surface">
      <header className="tab-header header-orange">
        <h1>Engineering GHIDRA Anti-Gravity</h1>
        <p>GHIDRA, FreeCAD, OpenSCAD, Blender, KiCad engineering sandbox.</p>
      </header>

      <div className="grammar-grid">
        {GRAMMAR.map((name) => (
          <Section key={name} name={name} accent="orange" />
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
