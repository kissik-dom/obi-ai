import { useState } from "react";

interface CopyButtonProps {
  value: string;
  label?: string;
}

export function CopyButton({ value, label = "COPY" }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1400);
    } catch {
      setCopied(false);
    }
  };

  return (
    <button
      type="button"
      onClick={() => void handleCopy()}
      className="inline-flex items-center gap-1 rounded border border-amber-600 bg-amber-400 px-2.5 py-1 font-mono text-[11px] font-bold uppercase tracking-wider text-black transition hover:bg-amber-500 active:scale-95"
    >
      {copied ? "COPIED" : label}
    </button>
  );
}
