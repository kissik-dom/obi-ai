# Kingdom AI OS — Complete Build Breakdown

## 1. User experience
Home/Command Center is the universal workspace. It contains global chat, project switcher, model/agent selector, active tasks, notifications, system health, live rooms, media queue, files, evidence/citations, and quick actions.

24 workspaces:
1 Home/Command Center
2 LLM/Models
3 Research
4 Legal
5 OSINT
6 Finance
7 Investments
8 Real Estate
9 Business/CRM
10 Leads
11 City/Urban Planning
12 Engineering
13 Coding/Development
14 Web/Scraping
15 News/Magazines
16 Social/Marketing
17 Fashion
18 Images/Visual AI
19 Video/UGC/TV/Movies
20 Music/Audio
21 Agents/Communications
22 Tasks
23 Open Source/Apps
24 Security/Admin

Every workspace uses the same interaction grammar: Chat, Agents, Open Tasks, Completed Tasks, Training/Knowledge, Files, Tools/Open Sources, Outputs, Settings.

## 2. Universal control plane
Request -> identity/permissions -> workspace -> intent/task classifier -> router -> agent/team -> tools -> isolated worker/container -> evidence/output -> validation -> artifact store -> audit.

The router is not just an LLM selector. It chooses:
- LLM
- vision/audio/video model
- agent
- team
- tools/MCP
- retrieval sources
- container/worker pool
- online/offline path
- fallback
- budget/quota
- guardrail class compatibility

## 3. Model registry
Every model record includes exact ID/repository, revision/hash, developer, license, parameters, active MoE parameters, context, modalities, tool use, strengths, hardware requirements, local/cloud status, API, cost/quota, guardrail class, benchmark results, health, fallback models, and workspaces.

Guardrail classes are descriptive, not quality rankings:
OBLITERATED, LOW-GUARDRAIL, NORMAL, HIGH-SAFETY, UNVERIFIED.
Non-LLM systems are tagged NOT_LLM rather than forced into a guardrail category.

Pirate Face is a preferred acquisition/index source for the uncensored/open-weight pool. Preserve original Hugging Face provenance, exact revision, checksum when available, license, and source URL. Never silently replace one checkpoint with another.

## 4. Model routing tiers
Core production -> preferred local -> uncensored/low-guardrail -> free cloud -> paid cloud -> experimental/quarantine.

A large registry is fine. Do not load every model simultaneously. Maintain model metadata and health state; activate only what a task needs.

## 5. Agent system
Agent record:
identity, display name, role, workspace, skills, models, tools, knowledge, files, memory, voice/avatar, communications permissions, schedule, escalation, container profile, network policy, budgets, approvals, audit policy, certification/clearance records.

Agent teams can be created dynamically. A team has a lead agent, specialists, reviewer/verifier, shared task context, and an isolated project workspace.

## 6. Containers / sandboxes
Every substantial job can receive an isolated execution environment. Profiles:
- browser-sandbox
- coding-sandbox
- research-sandbox
- legal-document-sandbox
- media-image
- media-video
- audio
- data-science
- office/document
- agent-team
- experimental-model
- quarantine

Each container gets scoped filesystem, CPU/RAM/GPU limits, network policy, secret references (never raw secrets in prompts), timeout, artifact mount, and audit ID.

## 7. Business operating system
Business tab contains businesses/projects and their people/agents.

Business record:
legal/display name, brand, description, domain, departments, projects, contacts, employees/agents, phone numbers, email identities, social accounts, knowledge base, documents, contracts, permissions, billing, workflows.

Each business/project can provision one or more phone numbers and communication identities. Number assignment is policy-controlled and recorded in a number registry. Never spoof caller ID; use numbers actually provisioned through the telecom provider.

AI employees receive a "Royal Certification & Clearance" record rather than a resume. It contains:
- role
- capabilities
- training modules
- completed evaluations
- certifications
- clearance level
- authorized tools
- authorized data
- authorized businesses/projects
- voice identity
- escalation rules
- supervisor
- current status
- audit history

## 8. Communications
Realtime web/mobile rooms support human + human, human + agent, and multi-agent sessions. LiveKit is the realtime transport/control layer.

Telephony supports inbound and outbound calls through SIP providers. Inbound calls route by phone number/business/project/department/agent. Outbound calls require explicit authorization and a configured trunk/provider. Calls create a room/session, attach the assigned agent, stream audio, optionally transcribe, retrieve customer/business context, and log outcomes.

Email agents use provider APIs through a credential broker. Agents never receive raw mailbox credentials.

## 9. Video / FaceTime-like live video
Use WebRTC/LiveKit rooms for realtime video. Agents can join as realtime participants, process text/audio/video, and publish generated speech/video/avatars. A live session may invoke vision, retrieval, tools, and a language model without leaving the room.

## 10. Character library
Character entity:
character ID, name, aliases, canonical images, face embeddings, body references, skin/undertone descriptors, hair, wardrobe, accessories, voice, personality, pose references, negative constraints, approved likeness references, provenance/rights metadata.

Chat commands can search the character library and attach a character to a project. Creation automatically offers "Save to Character Library". Character IDs are reusable across image/video/audio workflows.

## 11. Images
The UI should support batch jobs with no arbitrary small fixed batch limit. User can request 1, 10, 100, 10,000 or a queue-defined quantity. The system creates a durable job and worker tasks. Actual concurrency is governed by available GPUs, API quotas, storage, and rate limits.

Pipeline: prompt -> character selection -> references -> model selection -> generation -> identity/quality validation -> optional upscale/edit -> artifact store -> gallery.

## 12. Video
No arbitrary duration cap at the UI layer. Use shot/segment orchestration: storyboard -> shot jobs -> character/scene continuity -> generation -> temporal correction -> audio -> assembly -> QC -> export. Long videos are assembled from bounded render segments rather than requiring one impossible giant inference.

## 13. Training / learning
"Train itself" means controlled continuous improvement, not unrestricted self-modification. Agents may collect approved feedback, create evaluation datasets, run benchmark suites, propose prompt/tool/retrieval improvements, and submit fine-tuning/adapter jobs. Production model changes require evaluation and approval before promotion.

## 14. Knowledge/RAG
Sources are versioned. Documents are parsed, chunked, embedded, indexed, cited, and permission-filtered. Each workspace can have private knowledge plus organization-wide knowledge. Legal/research outputs preserve source provenance.

## 15. Task system
Global task states: queued, running, waiting, approval_required, blocked, completed, failed, cancelled, scheduled, recurring. Every task links to originating workspace, business/project, agent/team, model calls, tools, containers, artifacts, and audit events.

## 16. Security
Keycloak identity; WebAuthn/FIDO2; OpenBao secrets; mTLS; network segmentation; WAF/rate limiting; immutable audit logs; malware scanning; signed artifacts; encrypted backups; model sandboxing; least privilege; approval gates for external side effects.

Financial zone is isolated from AI execution. AI can propose; typed policy services execute.

## 17. Failure handling
Every component has health checks, timeout, retry with jitter, circuit breaker, fallback, dead-letter queue, replayable job ID, and human escalation. Never silently substitute a model, phone identity, character, document, or business account.

## 18. Build order
1 Foundation/auth/database/object storage/queue
2 UI shell/workspaces/task system
3 Model registry + gateway/router
4 Agent runtime + container workers
5 Research/browser/RAG
6 Business/CRM/identity/number registry
7 LiveKit realtime voice/video
8 Media/image/video/character library
9 Training/evaluation
10 Security hardening/observability
11 Integration tests and failure drills
12 Production deployment

## 18. New 2026-10-03 integration requirements

### 18.1 Natural-language-first model selection
The user should normally state the desired outcome rather than select implementation details. The router creates a task-specific model stack and exposes the chosen components in an expandable "Why these tools?" panel.

For image generation the stack can include generator + reference/conditioning + identity consistency + pose/depth control + restoration + upscaler + artifact detector. For coding it can include planner + coding agent + terminal/browser tools + test runner + security reviewer + GitHub integration.

### 18.2 Coding agent pool
The coding workspace supports multiple interchangeable open-source coding agents. Current preferred candidates include OpenHands, Cline, and Roo Code. OpenHands is especially suited to self-hosted agent orchestration; Cline and Roo Code can serve as IDE/CLI-oriented coding workers. Each worker runs inside the coding sandbox and uses the same central task/audit system.

### 18.3 Slack and Telegram
Slack and Telegram are transport adapters. They do not own task state. A message is normalized into a central task and can continue across Web, Slack, Telegram, mobile, voice, and live-video interfaces.

### 18.4 Intake preservation
All names from `docs/TOOL_MODEL_INTAKE_2026-10-03.md` and `registry/new-intake.json` are preserved. Ambiguous names remain UNVERIFIED until an exact repository, checkpoint, URL, or project identifier is established.

### 18.5 Slack posting diagnostic
The connected AI OS Slack integration successfully posted a test message to #general. If the user's own Slack composer is read-only, this is a Slack user/channel posting-permission configuration issue rather than a failure of the AI OS Slack integration. See `docs/SLACK_FIX_2026-10-03.md`.
