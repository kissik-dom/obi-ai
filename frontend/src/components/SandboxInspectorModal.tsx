import { useQuery } from "@tanstack/react-query";
import { X } from "lucide-react";
import { apiClient } from "../lib/apiClient";
import { useKingdomStore } from "../store/useKingdomStore";
import { CopyButton } from "./CopyButton";

export function SandboxInspectorModal() {
  const { sandboxDrawerMode, selectedSandboxId, openSandboxDrawer, closeSandboxDrawer } = useKingdomStore();

  const listQuery = useQuery({
    queryKey: [sandboxDrawerMode],
    queryFn: () => (sandboxDrawerMode === "requests" ? apiClient.listRequests() : apiClient.listFinished()),
    enabled: sandboxDrawerMode !== "closed",
  });

  if (sandboxDrawerMode === "closed") {
    return null;
  }

  const bundles = listQuery.data ?? [];
  const activeBundle =
    bundles.find((b) => b.sandbox_id === selectedSandboxId) ?? (bundles.length > 0 ? bundles[0] : null);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="flex max-h-[88vh] w-full max-w-5xl flex-col overflow-hidden rounded border-2 border-black bg-white shadow-2xl">
        <div className="flex items-center justify-between border-b-2 border-neutral-900 bg-white px-5 py-3">
          <div>
            <h2 className="text-sm font-extrabold uppercase tracking-wider text-fuchsia-600">
              {sandboxDrawerMode === "requests"
                ? "Requests Folder Inspector: s3://kingdom-requests/"
                : "Finished Folder Inspector: s3://kingdom-finished/"}
            </h2>
            <p className="font-mono text-[11px] text-neutral-700">
              Atomic MinIO temp-then-rename bundles with OpenTimestamps & IPFS Kubo audit evidence
            </p>
          </div>
          <button
            type="button"
            onClick={closeSandboxDrawer}
            className="rounded border border-neutral-400 p-1.5 text-black hover:bg-neutral-100"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="grid flex-1 overflow-hidden md:grid-cols-3">
          <div className="overflow-y-auto border-r border-neutral-200 p-3">
            <div className="mb-2 font-mono text-[11px] font-bold text-teal-700">
              SANDBOX BUNDLES ({bundles.length})
            </div>
            <div className="space-y-1.5">
              {bundles.map((b) => {
                const isSel = activeBundle?.sandbox_id === b.sandbox_id;
                return (
                  <button
                    key={b.sandbox_id}
                    type="button"
                    onClick={() => openSandboxDrawer(sandboxDrawerMode, b.sandbox_id)}
                    className={`w-full rounded border p-2.5 text-left transition ${
                      isSel ? "border-black bg-neutral-900 text-white" : "border-neutral-200 bg-white hover:bg-neutral-50"
                    }`}
                  >
                    <div className="truncate text-xs font-bold">{b.title}</div>
                    <div className={`font-mono text-[10px] ${isSel ? "text-amber-300" : "text-neutral-600"}`}>
                      {b.sandbox_id} | {b.tab} | {b.state}
                    </div>
                  </button>
                );
              })}
              {bundles.length === 0 && (
                <div className="font-mono text-[11px] text-neutral-600">
                  No sandbox bundles yet. Submit a Quick Request or chat turn to populate this bucket.
                </div>
              )}
            </div>
          </div>

          <div className="overflow-y-auto p-4 md:col-span-2">
            {activeBundle ? (
              <div className="space-y-4">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-neutral-200 pb-2">
                  <div>
                    <div className="text-sm font-bold text-black">{activeBundle.title}</div>
                    <div className="font-mono text-[11px] text-neutral-700">
                      s3://{activeBundle.bucket}/{activeBundle.sandbox_id}/ | Model: {activeBundle.model_used}
                    </div>
                  </div>
                  <CopyButton value={activeBundle.summary_md} label="COPY DOSSIER" />
                </div>

                <div>
                  <div className="mb-1 font-mono text-[11px] font-bold uppercase text-fuchsia-600">
                    Equip Manifest (ENABLE_SANDBOX_EQUIP_ALL={String(activeBundle.equip_status.equipped_all)})
                  </div>
                  <pre className="overflow-x-auto rounded border border-neutral-200 bg-neutral-50 p-3 text-black">
                    {JSON.stringify(activeBundle.equip_status, null, 2)}
                  </pre>
                </div>

                <div>
                  <div className="mb-1 font-mono text-[11px] font-bold uppercase text-teal-600">
                    Summary / Unified Output
                  </div>
                  <pre className="whitespace-pre-wrap rounded border border-neutral-200 bg-neutral-50 p-3 text-black">
                    {activeBundle.summary_md}
                  </pre>
                </div>

                <div className="grid gap-3 md:grid-cols-2">
                  <div>
                    <div className="mb-1 font-mono text-[11px] font-bold uppercase text-orange-600">audit.json</div>
                    <pre className="overflow-x-auto rounded border border-neutral-200 bg-neutral-50 p-2.5 text-black">
                      {JSON.stringify(activeBundle.audit_json, null, 2)}
                    </pre>
                  </div>
                  <div>
                    <div className="mb-1 font-mono text-[11px] font-bold uppercase text-orange-600">
                      Artifacts & Evidence
                    </div>
                    <pre className="overflow-x-auto rounded border border-neutral-200 bg-neutral-50 p-2.5 text-black">
                      {JSON.stringify(
                        {
                          artifacts: activeBundle.artifacts,
                          evidence: activeBundle.evidence,
                          logs: activeBundle.logs,
                        },
                        null,
                        2
                      )}
                    </pre>
                  </div>
                </div>
              </div>
            ) : (
              <div className="font-mono text-[11px] text-neutral-600">Select a sandbox bundle to inspect.</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
