import { create } from "zustand";

export const GRAMMAR = [
  "Chat",
  "Agents",
  "Open Tasks",
  "Completed Tasks",
  "Training",
  "Knowledge",
  "Files",
  "Tools",
  "Outputs",
  "Settings",
] as const;

export type TabSlug =
  | "home"
  | "llm"
  | "research"
  | "legal"
  | "osint"
  | "finance"
  | "investments"
  | "real_estate"
  | "business"
  | "leads"
  | "urban_planning"
  | "engineering_ghidra"
  | "coding"
  | "web_scraping"
  | "news"
  | "social_marketing"
  | "fashion"
  | "images_visual"
  | "video_ugc"
  | "music_audio"
  | "agents_comms"
  | "tasks"
  | "open_source"
  | "security_admin";

interface KingdomState {
  activeTab: TabSlug;
  setActiveTab: (tab: TabSlug) => void;
  copiedCode: string;
  setCopiedCode: (code: string) => void;
  turnoffFlags: Record<string, boolean>;
  setTurnoffFlag: (service: string, enabled: boolean) => void;
}

const DEFAULT_TURNOFF_FLAGS: Record<string, boolean> = {
  sandbox: false,
  agents: false,
  gpu: false,
  image: false,
  video: false,
  security: false,
};

export const useKingdomStore = create<KingdomState>()((set) => ({
  activeTab: "home",
  setActiveTab: (tab) => set({ activeTab: tab }),
  copiedCode: "",
  setCopiedCode: (code) => set({ copiedCode: code }),
  turnoffFlags: { ...DEFAULT_TURNOFF_FLAGS },
  setTurnoffFlag: (service, enabled) =>
    set((state) => ({
      turnoffFlags: { ...state.turnoffFlags, [service]: enabled },
    })),
}));
