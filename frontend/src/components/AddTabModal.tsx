import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { X } from "lucide-react";
import { apiClient } from "../lib/apiClient";
import { useKingdomStore } from "../store/useKingdomStore";
import type { ToolCategory } from "../types/api";

export function AddTabModal() {
  const queryClient = useQueryClient();
  const { showAddTabModal, setShowAddTabModal, setActiveTab, setShowExtendedTabs } = useKingdomStore();
  const [slug, setSlug] = useState("aerospace_lab");
  const [title, setTitle] = useState("Aerospace Lab");
  const [purpose, setPurpose] = useState("Orbital trajectory optimization, CAD structures, and telemetry verification.");
  const [bestLlm, setBestLlm] = useState("qwen3-coder-next-80b");
  const [accent, setAccent] = useState<"magenta" | "turquoise" | "orange">("turquoise");
  const [cat, setCat] = useState<ToolCategory>("H");

  const addMut = useMutation({
    mutationFn: () =>
      apiClient.addTab({
        slug,
        title,
        purpose,
        best_llm: bestLlm,
        tool_categories: [cat, "L"],
        accent,
      }),
    onSuccess: (res) => {
      void queryClient.invalidateQueries({ queryKey: ["tabs"] });
      void queryClient.invalidateQueries({ queryKey: ["healthz"] });
      setShowExtendedTabs(true);
      setActiveTab(res.tab.slug);
      setShowAddTabModal(false);
    },
  });

  if (!showAddTabModal) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="w-full max-w-lg rounded border-2 border-black bg-white p-5 shadow-2xl">
        <div className="mb-4 flex items-center justify-between border-b border-neutral-200 pb-2">
          <h2 className="text-sm font-extrabold uppercase tracking-wider text-fuchsia-600">
            Add New Sovereign Tab (new_tab_skill.py)
          </h2>
          <button
            type="button"
            onClick={() => setShowAddTabModal(false)}
            className="rounded border border-neutral-300 p-1 hover:bg-neutral-100"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <form
          className="space-y-3"
          onSubmit={(e) => {
            e.preventDefault();
            addMut.mutate();
          }}
        >
          <div>
            <label className="mb-1 block font-mono text-[11px] font-bold">Slug (lowercase_snake)</label>
            <input
              type="text"
              value={slug}
              onChange={(e) => setSlug(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, "_"))}
              className="w-full rounded border border-neutral-300 px-3 py-1.5 font-mono text-xs"
              required
            />
          </div>
          <div>
            <label className="mb-1 block font-mono text-[11px] font-bold">Tab Display Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full rounded border border-neutral-300 px-3 py-1.5 text-xs"
              required
            />
          </div>
          <div>
            <label className="mb-1 block font-mono text-[11px] font-bold">Domain Purpose</label>
            <textarea
              value={purpose}
              onChange={(e) => setPurpose(e.target.value)}
              rows={2}
              className="w-full rounded border border-neutral-300 px-3 py-1.5 text-xs"
              required
            />
          </div>
          <div className="grid grid-cols-3 gap-2">
            <div>
              <label className="mb-1 block font-mono text-[11px] font-bold">Best LLM</label>
              <select
                value={bestLlm}
                onChange={(e) => setBestLlm(e.target.value)}
                className="w-full rounded border border-neutral-300 bg-white px-2 py-1.5 text-xs"
              >
                <option value="qwen3.8-27b-2.19m">Qwen3.8-27B</option>
                <option value="ling-3.1-flash-1m">Ling-3.1-Flash-1M</option>
                <option value="qwen3-coder-next-80b">Qwen3-Coder-80B</option>
                <option value="gemma-4-it-qat-12b">Gemma-4-IT-12B</option>
                <option value="cyberstrike-offsec-35b">CyberStrike-35B</option>
              </select>
            </div>
            <div>
              <label className="mb-1 block font-mono text-[11px] font-bold">Tool Pack</label>
              <select
                value={cat}
                onChange={(e) => setCat(e.target.value as ToolCategory)}
                className="w-full rounded border border-neutral-300 bg-white px-2 py-1.5 text-xs"
              >
                <option value="H">H: Engineering</option>
                <option value="F">F: Research</option>
                <option value="D">D: OSINT</option>
                <option value="G">G: Security</option>
                <option value="J">J: Images</option>
                <option value="K">K: Video</option>
              </select>
            </div>
            <div>
              <label className="mb-1 block font-mono text-[11px] font-bold">Header Accent</label>
              <select
                value={accent}
                onChange={(e) => setAccent(e.target.value as "magenta" | "turquoise" | "orange")}
                className="w-full rounded border border-neutral-300 bg-white px-2 py-1.5 text-xs"
              >
                <option value="magenta">Magenta</option>
                <option value="turquoise">Turquoise</option>
                <option value="orange">Orange</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={() => setShowAddTabModal(false)}
              className="rounded border border-neutral-300 px-3 py-1.5 text-xs font-semibold"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={addMut.isPending}
              className="rounded border border-amber-600 bg-amber-400 px-4 py-1.5 font-mono text-[11px] font-bold text-black hover:bg-amber-500"
            >
              {addMut.isPending ? "Creating..." : "CREATE & MOUNT TAB"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
