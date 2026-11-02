# Kingdom AI OS — Tab Specification

## 24-tab surface (extensible to 28)

| # | Slug | Title | Accent | Focus |
| --- | --- | --- | --- | --- |
| 1 | home | Home/Command Center | magenta | global status, queues, dispatch |
| 2 | llm | LLM/Models | turquoise | model registry/routing, fallback |
| 3 | research | Research | turquoise | deep research, citation graph |
| 4 | legal | Legal | magenta | contracts, jurisdiction packs |
| 5 | osint | OSINT | orange | collection, evidence custody |
| 6 | finance | Finance | orange | ledger, markets, vault |
| 7 | investments | Investments | orange | deal scoring, due diligence |
| 8 | real_estate | Real Estate | orange | underwriting, parcels, zoning |
| 9 | business | Business/CRM | turquoise | pipeline, clients, deal rooms |
| 10 | leads | Leads | magenta | lead scoring/routing/cadence |
| 11 | urban_planning | City/Urban Planning | turquoise | zoning, census, infrastructure |
| 12 | engineering_ghidra | Engineering GHIDRA Anti-Gravity | orange | GHIDRA, FreeCAD, OpenSCAD, KiCad |
| 13 | coding | Coding/Dev | turquoise | code, tests, deploys |
| 14 | web_scraping | Web/Scraping | orange | Apify/Scrapy/Playwright/Selenium |
| 15 | news | News/Magazines | magenta | news, credibility, archives |
| 16 | social_marketing | Social/Marketing | orange | social, campaigns, calendar |
| 17 | fashion | Fashion | magenta | lookbooks, trends, consistency |
| 18 | images_visual | Images/Visual AI | turquoise | FLUX.1, SAM2, ControlNet |
| 19 | video_ugc | Video/UGC/TV/Movies | magenta | MiniMax Hailuo-02, Wan, LTX, Kling |
| 20 | music_audio | Music/Audio Vocal Tuning | orange | GSnap, MAutoPitch, Spleeter, RVC |
| 21 | agents_comms | Agents/Communications | turquoise | CUA, WAHA/Baileys/Evolution |
| 22 | tasks | Tasks | magenta | sandbox intake/finished folders |
| 23 | open_source | Open Source/Apps | turquoise | app catalog, runtime |
| 24 | security_admin | Security/Admin | orange | SIEM/IDP/admin controls |

Reserved extension tabs 25-28: Health/Medical, Education, Supply Chain, Custom Lab.
Extension policy: add `TAB_SLUGS`, `docs/TAB_SPEC.md`, backend router, frontend
component, tool category mapping, and test entry in the same PR.

## One grammar for every tab

```
Chat | Agents | Open Tasks | Completed Tasks | Training | Knowledge | Files | Tools | Outputs | Settings
```

Every tab has the identical API prefix and endpoints:

- `GET  /api/<slug>` — grammar
- `GET  /api/<slug>/chat`
- `POST /api/<slug>/chat`
- `GET  /api/<slug>/agents`
- `GET  /api/<slug>/tasks/open`
- `GET  /api/<slug>/tasks/completed`
- `GET  /api/<slug>/training`
- `GET  /api/<slug>/knowledge`
- `GET  /api/<slug>/files`
- `GET  /api/<slug>/tools`
- `GET  /api/<slug>/outputs`
- `GET  /api/<slug>/settings`
- `PUT  /api/<slug>/settings`

## Rules

1. No tab-specific bespoke backend route names; only the slug changes.
2. Frontend components share the same `GRAMMAR` order and section behavior.
3. Every mutation accepts `x-idempotency-key`; duplicate keys return the previous receipt.
4. Every tab has a `turnoff_flags` block. Default all services on; operators can turn off sandbox/agents/GPU/image/video per tab.
