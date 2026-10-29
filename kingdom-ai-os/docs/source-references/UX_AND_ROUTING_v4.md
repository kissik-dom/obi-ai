# Kingdom AI OS — Maximum-Usability UX and Automatic Model Stack

## Principle
The user asks for an outcome. The system selects the implementation.

Example request:
> Make a realistic 4K image of a curvy melanated woman.

The user should NOT have to say "use model X + LoRA Y + face consistency tool Z" unless they deliberately open Advanced Mode.

## Visual request planner
The planner converts natural language into a structured `MediaIntent`:
- subject
- demographics/descriptors supplied by user
- body/wardrobe/pose
- realism level
- resolution
- aspect ratio
- number of outputs
- identity/character ID
- reference images
- environment
- lighting
- camera
- negative constraints
- rights/provenance requirements

## Model-stack planner
The router chooses a stack rather than one model:
1. primary generator
2. conditioning/reference adapter
3. identity/character consistency
4. pose/depth/control
5. detail/restoration
6. upscale
7. artifact detector
8. human-review gate when required

Each layer can run locally, through an approved API, or through a hybrid route.

## Unlimited-feeling media UX
The interface accepts any requested quantity/duration and turns it into a durable queue. There is no arbitrary "maximum 4 images" or "maximum 60 seconds" product rule.

Actual execution is bounded by:
- GPU availability
- API quotas
- storage
- rate limits
- provider terms
- safety/policy constraints

The UI must show:
`Requested → Queued → Running → QC → Complete` and never pretend that unbounded physical compute exists.

## Character Library
Characters are reusable assets. A user can:
- create a character
- import a character
- search by natural language
- drag/drop a character into a project
- ask chat to attach a character
- save a generated character
- version a character
- lock canonical identity references
- attach voice/wardrobe/personality

Natural language example:
> Find the character with the red braided hair from my library and use her in this video.

The system searches the Character Library, resolves the canonical ID, attaches it to the job, and shows a small confirmation chip.

## Coding workspace
Default coding stack:
- OpenHands for self-hosted agent orchestration
- Cline or Roo Code as optional editor/terminal coding agents
- Open WebUI as a unified conversational front end
- GitHub as repository/issue/PR system
- MCP/tool registry for controlled external actions
- isolated coding containers for execution

No coding agent receives unrestricted host access by default. Each session receives a project-scoped filesystem, network policy, secrets references, and approval policy.

## Slack command surface
Slack is a transport surface, not the source of truth. Messages become tasks in the AI OS. The same task can continue in Web UI, Slack, Telegram, or another approved channel.

Example:
`@KingdomAI build the landing page in repo X, run tests, open a PR, and report back.`

The command becomes a task with:
- requester
- channel/message reference
- business/project
- repository
- agent/team
- container
- model stack
- tool permissions
- approvals
- artifacts
- final response

## Telegram command surface
Use a Telegram adapter implementing the same `MessageTransport` interface. Do not build a second agent architecture. Telegram, Slack, web, mobile, voice and live-video all submit to the same central task API.
