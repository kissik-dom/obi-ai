import type { TabSpecRecord } from "../types/api";
import { useKingdomStore } from "../store/useKingdomStore";

interface TabSidebarProps {
  tabs: TabSpecRecord[];
}

export function TabSidebar({ tabs }: TabSidebarProps) {
  const { activeTab, setActiveTab, showExtendedTabs, setShowExtendedTabs } = useKingdomStore();

  const coreTabs = tabs.filter((t) => t.core);
  const extendedTabs = tabs.filter((t) => !t.core);

  const accentBadge = (accent: TabSpecRecord["accent"], selected: boolean) => {
    if (selected) {
      return "bg-black text-white border-black";
    }
    if (accent === "magenta") {
      return "bg-fuchsia-50 text-fuchsia-700 border-fuchsia-300";
    }
    if (accent === "turquoise") {
      return "bg-teal-50 text-teal-700 border-teal-300";
    }
    return "bg-orange-50 text-orange-700 border-orange-300";
  };

  return (
    <aside className="w-72 shrink-0 border-r border-neutral-300 bg-white">
      <div className="border-b border-neutral-200 px-4 py-3">
        <div className="flex items-center justify-between">
          <span className="font-mono text-[11px] font-bold uppercase tracking-wider text-fuchsia-600">
            24 Core Tabs ({coreTabs.length})
          </span>
          <label className="flex cursor-pointer items-center gap-1.5 font-mono text-[11px] text-neutral-700">
            <input
              type="checkbox"
              checked={showExtendedTabs}
              onChange={(e) => setShowExtendedTabs(e.target.checked)}
              className="rounded border-neutral-400"
            />
            Show 25-28+
          </label>
        </div>
      </div>

      <nav className="max-h-[calc(100vh-120px)] space-y-1 overflow-y-auto p-2.5">
        {coreTabs.map((tab) => {
          const selected = tab.slug === activeTab;
          return (
            <button
              key={tab.slug}
              type="button"
              onClick={() => setActiveTab(tab.slug)}
              className={`flex w-full items-center justify-between rounded border px-2.5 py-2 text-left transition ${
                selected
                  ? "border-black bg-neutral-900 font-bold text-white"
                  : "border-neutral-200 bg-white text-black hover:border-neutral-400 hover:bg-neutral-50"
              }`}
            >
              <div className="min-w-0 pr-2">
                <div className="truncate text-xs font-semibold">{tab.title}</div>
                <div
                  className={`truncate font-mono text-[10px] ${
                    selected ? "text-amber-300" : "text-neutral-600"
                  }`}
                >
                  {tab.best_llm}
                </div>
              </div>
              <span
                className={`rounded border px-1.5 py-0.5 font-mono text-[10px] font-bold ${accentBadge(
                  tab.accent,
                  selected
                )}`}
              >
                {String(tab.index).padStart(2, "0")}
              </span>
            </button>
          );
        })}

        {showExtendedTabs && extendedTabs.length > 0 && (
          <div className="pt-3">
            <div className="mb-1.5 border-t border-neutral-200 px-1 pt-2 font-mono text-[11px] font-bold uppercase tracking-wider text-teal-600">
              Extensible Tabs (25-{24 + extendedTabs.length})
            </div>
            <div className="space-y-1">
              {extendedTabs.map((tab) => {
                const selected = tab.slug === activeTab;
                return (
                  <button
                    key={tab.slug}
                    type="button"
                    onClick={() => setActiveTab(tab.slug)}
                    className={`flex w-full items-center justify-between rounded border px-2.5 py-2 text-left transition ${
                      selected
                        ? "border-black bg-neutral-900 font-bold text-white"
                        : "border-teal-200 bg-white text-black hover:border-teal-500 hover:bg-teal-50/30"
                    }`}
                  >
                    <div className="min-w-0 pr-2">
                      <div className="truncate text-xs font-semibold">{tab.title}</div>
                      <div
                        className={`truncate font-mono text-[10px] ${
                          selected ? "text-amber-300" : "text-neutral-600"
                        }`}
                      >
                        {tab.best_llm}
                      </div>
                    </div>
                    <span
                      className={`rounded border px-1.5 py-0.5 font-mono text-[10px] font-bold ${accentBadge(
                        tab.accent,
                        selected
                      )}`}
                    >
                      {String(tab.index).padStart(2, "0")}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </nav>
    </aside>
  );
}
