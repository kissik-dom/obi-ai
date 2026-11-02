import { useState, type ComponentType } from "react";
import { useKingdomStore, type TabSlug } from "./store/useKingdomStore";
import HomeCommandCenter from "./tabs/HomeCommandCenter";
import LlmModels from "./tabs/LlmModels";
import Research from "./tabs/Research";
import Legal from "./tabs/Legal";
import Osint from "./tabs/Osint";
import Finance from "./tabs/Finance";
import Investments from "./tabs/Investments";
import RealEstate from "./tabs/RealEstate";
import BusinessCrm from "./tabs/BusinessCrm";
import Leads from "./tabs/Leads";
import CityUrbanPlanning from "./tabs/CityUrbanPlanning";
import EngineeringGhidraAntiGravity from "./tabs/EngineeringGhidraAntiGravity";
import CodingDev from "./tabs/CodingDev";
import WebScraping from "./tabs/WebScraping";
import NewsMagazines from "./tabs/NewsMagazines";
import SocialMarketing from "./tabs/SocialMarketing";
import Fashion from "./tabs/Fashion";
import ImagesVisualAi from "./tabs/ImagesVisualAi";
import VideoUgcTvMovies from "./tabs/VideoUgcTvMovies";
import MusicAudioVocalTuning from "./tabs/MusicAudioVocalTuning";
import AgentsCommunications from "./tabs/AgentsCommunications";
import Tasks from "./tabs/Tasks";
import OpenSourceApps from "./tabs/OpenSourceApps";
import SecurityAdmin from "./tabs/SecurityAdmin";

interface TabDefinition {
  slug: TabSlug;
  title: string;
  accent: "magenta" | "turquoise" | "orange";
  Component: ComponentType<Record<string, never>>;
}

const TAB_DEFINITIONS: TabDefinition[] = [
  { slug: "home", title: "Home/Command Center", accent: "magenta", Component: HomeCommandCenter },
  { slug: "llm", title: "LLM/Models", accent: "turquoise", Component: LlmModels },
  { slug: "research", title: "Research", accent: "turquoise", Component: Research },
  { slug: "legal", title: "Legal", accent: "magenta", Component: Legal },
  { slug: "osint", title: "OSINT", accent: "orange", Component: Osint },
  { slug: "finance", title: "Finance", accent: "orange", Component: Finance },
  { slug: "investments", title: "Investments", accent: "orange", Component: Investments },
  { slug: "real_estate", title: "Real Estate", accent: "orange", Component: RealEstate },
  { slug: "business", title: "Business/CRM", accent: "turquoise", Component: BusinessCrm },
  { slug: "leads", title: "Leads", accent: "magenta", Component: Leads },
  { slug: "urban_planning", title: "City/Urban Planning", accent: "turquoise", Component: CityUrbanPlanning },
  { slug: "engineering_ghidra", title: "Engineering GHIDRA Anti-Gravity", accent: "orange", Component: EngineeringGhidraAntiGravity },
  { slug: "coding", title: "Coding/Dev", accent: "turquoise", Component: CodingDev },
  { slug: "web_scraping", title: "Web/Scraping", accent: "orange", Component: WebScraping },
  { slug: "news", title: "News/Magazines", accent: "magenta", Component: NewsMagazines },
  { slug: "social_marketing", title: "Social/Marketing", accent: "orange", Component: SocialMarketing },
  { slug: "fashion", title: "Fashion", accent: "magenta", Component: Fashion },
  { slug: "images_visual", title: "Images/Visual AI", accent: "turquoise", Component: ImagesVisualAi },
  { slug: "video_ugc", title: "Video/UGC/TV/Movies", accent: "magenta", Component: VideoUgcTvMovies },
  { slug: "music_audio", title: "Music/Audio Vocal Tuning", accent: "orange", Component: MusicAudioVocalTuning },
  { slug: "agents_comms", title: "Agents/Communications", accent: "turquoise", Component: AgentsCommunications },
  { slug: "tasks", title: "Tasks", accent: "magenta", Component: Tasks },
  { slug: "open_source", title: "Open Source/Apps", accent: "turquoise", Component: OpenSourceApps },
  { slug: "security_admin", title: "Security/Admin", accent: "orange", Component: SecurityAdmin },
];

export default function App() {
  const activeTab = useKingdomStore((state) => state.activeTab);
  const setActiveTab = useKingdomStore((state) => state.setActiveTab);
  const [search, setSearch] = useState("");
  const ActiveComponent =
    TAB_DEFINITIONS.find((tab) => tab.slug === activeTab)?.Component ??
    HomeCommandCenter;
  const filteredTabs = TAB_DEFINITIONS.filter((tab) =>
    tab.title.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div className="kingdom-shell">
      <nav className="kingdom-nav" aria-label="Kingdom AI OS tabs">
        <div className="brand">Kingdom AI OS</div>
        <input
          className="tab-search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Filter 24 tabs"
          aria-label="Filter tabs"
        />
        <div className="tab-list" role="tablist" aria-label="Kingdom AI OS tabs">
          {filteredTabs.map((tab) => (
            <button
              key={tab.slug}
              type="button"
              role="tab"
              aria-selected={activeTab === tab.slug}
              className={`tab-pill accent-${tab.accent} ${activeTab === tab.slug ? "tab-pill-active" : ""}`}
              onClick={() => setActiveTab(tab.slug)}
            >
              {tab.title}
            </button>
          ))}
        </div>
      </nav>
      <main className="content">
        <ActiveComponent />
      </main>
    </div>
  );
}
