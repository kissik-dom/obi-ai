# ADD_TAB.md - Extending Kingdom AI OS From 24 to 28+ Tabs

Kingdom AI OS allows both operators and autonomous agents (`backend/agents/skills/new_tab_skill.py`) to add new tabs at runtime or build time while preserving the strict 10-part tab grammar:

`Chat | Agents | Open Tasks | Completed Tasks | Training | Knowledge | Files | Tools | Outputs | Settings`

## Manual Protocol (8 Deterministic Steps)

1. **Frontend Page (`frontend/src/pages/<PascalName>Tab.tsx`)**: Create a typed React component rendering `<UnifiedTabWorkspace tabSlug="<slug>" />` with white background, black text, magenta/turquoise/orange headers, gold `COPY` buttons, 11px mono code, header chapter label, and footer page numbers (no em dashes).
2. **Backend Router (`backend/api/routers/<slug>.py`)**: Create a FastAPI `APIRouter` via `build_tab_router("<slug>")` exposing `/chat`, `/agents`, `/open-tasks`, `/completed-tasks`, `/training`, `/knowledge`, `/files`, `/tools`, `/outputs`, and `/settings` with Pydantic v2 `BaseModel` schemas.
3. **Specification (`TAB_SPEC.md`)**: Register the tab's purpose, single best LLM, top 5-10 priority LLMs, Category A-M open-source tools, assigned agents, and deterministic router rule.
4. **Compose Service (`docker-compose.yml`)**: Add an optional isolated worker container if the tab introduces a new native runtime stage.
5. **Frontend Router (`frontend/src/App.tsx`)**: Register the tab in the tab bar state and route table.
6. **Backend App (`backend/main.py`)**: Mount `include_router` under `/api/<slug>` and `/api/tabs/<slug>`.
7. **Registries (`LLM_REGISTRY.md` / `TOOL_REGISTRY.md`)**: Register any new `ModelRecord` (`new_llm_skill.py`) or `ToolRecord` (`new_tool_skill.py`).
8. **Git Commit**: Commit with `feat: add <slug> tab` and run `pytest tests/test_all.py`.

## Automated Agent Skill Execution (`+ ADD TAB` Button)

Clicking **`+ ADD TAB`** in the White UI calls `POST /api/agents/skills/new-tab` which invokes `backend/agents/skills/new_tab_skill.py`:
- Validates the slug, title, best LLM, tool categories, and assigned agents via Pydantic v2.
- Generates `backend/api/routers/<slug>.py` and `frontend/src/pages/<PascalName>Tab.tsx`.
- Registers the live tab immediately in FastAPI and persists the tab definition so it appears in the UI tab bar without downtime.
- Companion skills in `backend/agents/skills/`:
  - `new_tab_skill.py`
  - `new_llm_skill.py`
  - `new_tool_skill.py`
  - `new_agent_skill.py`
