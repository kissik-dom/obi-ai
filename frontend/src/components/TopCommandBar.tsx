import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { FolderCheck, FolderInput, PlusCircle, ShieldCheck, Zap } from "lucide-react";
import { apiClient } from "../lib/apiClient";
import { useKingdomStore } from "../store/useKingdomStore";

export function TopCommandBar() {
  const queryClient = useQueryClient();
  const { activeTab, openSandboxDrawer, setShowAddTabModal } = useKingdomStore();
  const [quickPrompt, setQuickPrompt] = useState("");

  const healthQuery = useQuery({
    queryKey: ["healthz"],
    queryFn: apiClient.getHealthz,
    refetchInterval: 10000,
  });

  const quickRequestMutation = useMutation({
    mutationFn: (prompt: string) => apiClient.submitQuickRequest(prompt, activeTab),
    onSuccess: (bundle) => {
      setQuickPrompt("");
      void queryClient.invalidateQueries({ queryKey: ["requests"] });
      void queryClient.invalidateQueries({ queryKey: ["finished"] });
      openSandboxDrawer("requests", bundle.sandbox_id);
    },
  });

  const h = healthQuery.data;

  return (
    <header className="sticky top-0 z-30 border-b-2 border-neutral-900 bg-white px-4 py-3">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="rounded bg-fuchsia-600 px-2.5 py-1 font-mono text-[11px] font-bold uppercase tracking-widest text-white">
            KINGDOM AI OS
          </div>
          <div>
            <h1 className="text-sm font-extrabold tracking-tight text-black">
              Sovereign Multi-Agent Operating System, 24 to 28+ Tabs
            </h1>
            <p className="font-mono text-[11px] text-neutral-700">
              {h
                ? `Status: ${h.status.toUpperCase()} | Tabs: ${h.tabs_registered} | Models: ${h.models_registered} | Open-Source Tools: ${h.open_source_tools} | Total Tools: ${h.total_tools}`
                : "Connecting to Sovereign Control Plane..."}
            </p>
          </div>
        </div>

        <div className="flex flex-1 items-center justify-end gap-2">
          <form
            className="flex min-w-[260px] max-w-md flex-1 items-center gap-1.5"
            onSubmit={(e) => {
              e.preventDefault();
              if (quickPrompt.trim()) {
                quickRequestMutation.mutate(quickPrompt.trim());
              }
            }}
          >
            <input
              type="text"
              value={quickPrompt}
              onChange={(e) => setQuickPrompt(e.target.value)}
              placeholder={`Quick Request in [${activeTab}] -> s3://kingdom-requests/`}
              className="w-full rounded border border-neutral-300 bg-white px-3 py-1.5 text-xs text-black placeholder:text-neutral-500 focus:border-teal-600 focus:outline-none"
            />
            <button
              type="submit"
              disabled={quickRequestMutation.isPending || !quickPrompt.trim()}
              className="inline-flex items-center gap-1 whitespace-nowrap rounded border border-orange-700 bg-orange-600 px-3 py-1.5 text-xs font-bold text-white transition hover:bg-orange-700 disabled:opacity-50"
            >
              <Zap className="h-3.5 w-3.5" />
              {quickRequestMutation.isPending ? "Running..." : "Quick Request"}
            </button>
          </form>

          <button
            type="button"
            onClick={() => openSandboxDrawer("requests")}
            className="inline-flex items-center gap-1 rounded border border-teal-700 bg-teal-600 px-2.5 py-1.5 text-xs font-bold text-white hover:bg-teal-700"
          >
            <FolderInput className="h-3.5 w-3.5" />
            Requests Folder
          </button>

          <button
            type="button"
            onClick={() => openSandboxDrawer("finished")}
            className="inline-flex items-center gap-1 rounded border border-fuchsia-700 bg-fuchsia-600 px-2.5 py-1.5 text-xs font-bold text-white hover:bg-fuchsia-700"
          >
            <FolderCheck className="h-3.5 w-3.5" />
            Finished Folder
          </button>

          <button
            type="button"
            onClick={() => setShowAddTabModal(true)}
            className="inline-flex items-center gap-1 rounded border border-amber-600 bg-amber-400 px-2.5 py-1.5 font-mono text-[11px] font-bold text-black hover:bg-amber-500"
          >
            <PlusCircle className="h-3.5 w-3.5" />
            ADD TAB
          </button>

          <a
            href="/docs"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 rounded border border-neutral-900 bg-white px-2.5 py-1.5 font-mono text-[11px] font-bold text-black hover:bg-neutral-100"
          >
            <ShieldCheck className="h-3.5 w-3.5 text-teal-600" />
            API /docs
          </a>
        </div>
      </div>
    </header>
  );
}
