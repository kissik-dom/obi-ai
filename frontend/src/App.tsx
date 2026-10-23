import { useQuery } from "@tanstack/react-query";
import { apiClient } from "./lib/apiClient";
import { useKingdomStore } from "./store/useKingdomStore";
import { TopCommandBar } from "./components/TopCommandBar";
import { TabSidebar } from "./components/TabSidebar";
import { TabWorkspace } from "./components/TabWorkspace";
import { SandboxInspectorModal } from "./components/SandboxInspectorModal";
import { AddTabModal } from "./components/AddTabModal";

export function App() {
  const { activeTab } = useKingdomStore();

  const tabsQuery = useQuery({
    queryKey: ["tabs"],
    queryFn: () => apiClient.listTabs(true),
  });

  const modelsQuery = useQuery({
    queryKey: ["models"],
    queryFn: apiClient.listModels,
  });

  const tabs = tabsQuery.data ?? [];
  const currentTab = tabs.find((t) => t.slug === activeTab) ?? tabs[0];

  return (
    <div className="min-h-screen bg-white text-black">
      <TopCommandBar />
      <div className="flex">
        <TabSidebar tabs={tabs} />
        {currentTab ? (
          <TabWorkspace tabSpec={currentTab} models={modelsQuery.data ?? []} />
        ) : (
          <div className="p-8 font-mono text-xs text-neutral-700">
            Loading Sovereign 24 to 28 Tab Registry...
          </div>
        )}
      </div>
      <SandboxInspectorModal />
      <AddTabModal />
    </div>
  );
}
