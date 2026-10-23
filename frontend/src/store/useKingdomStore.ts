import { create } from "zustand";
import type { GrammarSection } from "../types/api";

interface KingdomUiState {
  activeTab: string;
  activeSection: GrammarSection;
  showExtendedTabs: boolean;
  sandboxDrawerMode: "closed" | "requests" | "finished";
  selectedSandboxId: string | null;
  showAddTabModal: boolean;
  setActiveTab: (slug: string) => void;
  setActiveSection: (section: GrammarSection) => void;
  setShowExtendedTabs: (show: boolean) => void;
  openSandboxDrawer: (mode: "requests" | "finished", sandboxId?: string | null) => void;
  closeSandboxDrawer: () => void;
  setShowAddTabModal: (open: boolean) => void;
}

export const useKingdomStore = create<KingdomUiState>((set) => ({
  activeTab: "home",
  activeSection: "chat",
  showExtendedTabs: true,
  sandboxDrawerMode: "closed",
  selectedSandboxId: null,
  showAddTabModal: false,
  setActiveTab: (slug) => set({ activeTab: slug }),
  setActiveSection: (section) => set({ activeSection: section }),
  setShowExtendedTabs: (show) => set({ showExtendedTabs: show }),
  openSandboxDrawer: (mode, sandboxId = null) =>
    set({ sandboxDrawerMode: mode, selectedSandboxId: sandboxId }),
  closeSandboxDrawer: () => set({ sandboxDrawerMode: "closed", selectedSandboxId: null }),
  setShowAddTabModal: (open) => set({ showAddTabModal: open }),
}));
