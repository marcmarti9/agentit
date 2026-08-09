---
name: using-agentit
description: Activate Agentit end-to-end. Use when the user says "use agentit", "usa agentit", "with agentit", "usando agentit", or asks to run work under the Agentit harness.
---

# Using Agentit

Single entrypoint for coding sessions. When the user says **use agentit** / **usa agentit** (or equivalent), follow this playbook for the rest of the session unless they cancel it.

## Trigger phrases

Activate this skill when the message includes (any language, loose match):

- `use agentit` / `usa agentit` / `usando agentit` / `with agentit`
- `agentit mode` / `modo agentit`
- explicit ask to route/plan with Agentit

If global `AGENTS.md` already marks Agentit as the default harness, still follow this playbook for non-trivial work.

## Fixed paths (this machine)

| Item | Path |
|------|------|
| Harness root | `~/code/agentit` |
| CLI | `agentit` (`~/.local/bin/agentit` → harness) |
| Router | `python3 ~/code/agentit/router/route.py "…"` |
| Specialist catalog | `~/code/agentit/agents/catalog.yaml` |
| Skill bodies (source of truth) | `~/code/agentit/skills/<id>/SKILL.md` |
| Skill references | `~/code/agentit/skills/<id>/references/` |
| Global Open Skills | `~/.agents/skills/` |
| Project skills (JIT) | `<project>/.agents/skills/` |
| MCP catalog | `~/code/agentit/mcp/catalog.yaml` |

Prefer harness skill paths when provider copies are stale or missing.

## Craft bar (why this harness exists)

When Agentit is active, **raise the bar** vs a casual agent session:

- Prefer the boring correct solution over vibes and half-finished UI/API surface.
- Default to tests for behavior changes (`test-driven-development` when logic changes).
- For visual work, use the craft-first design stack rather than purple-template defaults.
- Never claim done without fresh command evidence (`verification-before-completion`).
- Touch only the requested scope; no drive-by refactors.
- If something is ambiguous and expensive to reverse, stop and ask **one** sharp question.

This is the practical meaning of “usa agentit”: more discipline, not more agents.

## Specialist agents: skills can become temporary experts

Agentit has reusable specialist roles in `agents/catalog.yaml`. A specialist combines a role, a small skill bundle, an output contract, and a bounded worker context. This lets the parent agent either use a skill directly **or** delegate that skill set to a fresh subagent when specialization or isolation is worth the overhead.

Before spawning, load `specialist-agent-routing` and ask:

- would fresh context materially improve this branch?
- is independent research/review valuable?
- does the task benefit from a different model or toolset?
- can the specialist work without fighting over shared files/state?
- is the output independently consumable by the parent?

If not, keep the work in the parent. Do not build a fake company for a small task.

Examples:

| Need | Optional specialist |
|---|---|
| current visual/UI references | `ui-researcher` |
| current design/creative trends | `trend-researcher` |
| choose libraries/tools for an unusual concept | `creative-tool-scout` |
| direct narrative/pacing for an immersive page | `visual-storytelling-director` |
| design a store/museum/showroom journey | `spatial-experience-designer` |
| add memorable micro-moments late in polish | `delight-and-whimsy` |
| independent premium visual critique | `design-critic` |
| animation/WebGL/mobile performance review | `performance-benchmarker` |
| API edge-case review | `api-tester` |
| backend architecture probe | `backend-architect` |

All delegated specialists still go through the Worker Context Contract. The parent/Architect integrates and verifies; specialist reports are inputs, not final truth.

## Design exception: quality over context thrift

General engineering work still uses progressive disclosure. **Serious design work is the explicit exception to token thrift.** Do not weaken research, art direction, motion analysis, visual QA, design-system inspection, or concept exploration merely to minimize context.

When the `design` profile is active, load the foundational trio for non-trivial visual work:

1. `design-taste-frontend` — art direction, visual thesis, composition, type/material/motion intensity;
2. `impeccable-design` — craft director, critique/polish/hardening, responsive and state completeness;
3. `emil-design-eng` — interaction feel, animation decisions, perceived performance, invisible detail.

Then load or delegate specialists by signal:

| Signal | Add / delegate |
|---|---|
| current inspiration / references | `design-inspiration-research`; optionally `ui-researcher` |
| trend-sensitive / “what is cutting edge now?” | `design-trend-researcher`; optionally `trend-researcher` |
| open-ended “invent a memorable web experience” | `creative-web-experiences` |
| narrative/cinematic pacing matters | `visual-storytelling-director`; optionally specialist role of same name |
| unusual implementation / choose best creative library | `creative-tool-scout` skill or specialist |
| Figma link/frame/design system/Code Connect | `figma-design-workflow` + official `figma` MCP |
| scroll-driven / pinned / scrub / parallax / image sequence | `scrollytelling-web` + `gsap-scrolltrigger` + `gsap-performance` |
| virtual store / room / museum / environment / walkthrough | `threejs-spatial-experiences`; optionally `spatial-experience-designer` |
| product explodes/decomposes/disassembles, GLB/glTF, true 3D camera/material work | relevant scroll stack + `threejs-product-storytelling` |
| late-stage memorable micro-moments | `delight-and-whimsy`; optionally its reviewer specialist |
| ordinary micro-interaction / component motion | keep `emil-design-eng`; do not escalate to cinematic tooling without cause |

### Design competition

When the user explicitly asks to “go all out”, create a premium/award-level redesign, or otherwise makes concept quality a major success criterion, the Architect may choose the `design competition` topology:

1. create one shared research/reference brief;
2. ask 2-3 independent concept agents for **different** directions;
3. optionally use different capable model families or deliberate creative constraints;
4. judge proposals with explicit criteria: brand fit, originality, clarity, usability, technical feasibility, performance, and memorability;
5. choose one winner or a justified hybrid;
6. only then implement;
7. after implementation, run an independent `design-critic` and browser/performance pass.

Do not use this topology for routine UI maintenance.

## Playbook (every non-trivial task)

### 1. Route (+ optional local trace)

```bash
python3 ~/code/agentit/router/route.py "short task description in the user language"
# or persist a trail for yourself:
agentit trace "short task description" --project <project_root>
```

Read at least: `risk`, `topology`, `skills_available`, `skills_recommended_missing`, `applied_preferences`, `verification`, `jit_profile_recommendations`, `reasons`.

The JSON is a **plan**, not permission to run destructive ops. Traces land in `.agentit/traces/` for debugging the harness on real work — not as public metrics theatre.

### 2. Activate missing profiles (JIT)

If `jit_profile_recommendations` is non-empty, or a needed skill is only in an on-demand profile:

```bash
agentit enable <profile> --project <project_root> --apply
agentit status --project <project_root>
```

Common profiles: `frontend`, `design`, `backend`, `supabase`, `product`, `writing`, `release`, `research`.

For any non-trivial request whose main success criterion is visual design, motion direction, landing-page craft, visual redesign, scrollytelling, spatial experience, or product presentation, prefer activating **`design`** instead of stopping at `frontend`.

Do **not** enable `all` unless the user asks.

### 3. Load task-relevant skills

For each id in `skills_available` and project-active skills that match the task:

1. Open `SKILL.md` (harness path first).
2. Follow its process; load references when a step needs them.
3. For general engineering, avoid dumping unrelated skills into context.
4. For design, apply the quality-first exception above: foundational design skills can be loaded together and specialist stacks should be loaded when their signal is present.
5. If a branch of work would benefit from isolation or independent expertise, inspect `agents/catalog.yaml` and use `specialist-agent-routing` rather than stuffing every role into the parent.

High-value specialized skills:

| Need | Skill |
|------|--------|
| Specialist selection/delegation | `specialist-agent-routing` |
| Art direction / landing / portfolio / visual redesign | `design-taste-frontend` |
| Design critique / polish / responsive craft | `impeccable-design` |
| Product UI interaction / motion feel | `emil-design-eng` |
| Current project inspiration | `design-inspiration-research` |
| Current trend mapping | `design-trend-researcher` |
| Invent creative web concepts | `creative-web-experiences` |
| Visual narrative / scene pacing | `visual-storytelling-director` |
| Choose current creative tooling | `creative-tool-scout` |
| Delight / whimsy pass | `delight-and-whimsy` |
| Figma design-to-code / design-system context | `figma-design-workflow` |
| Cinematic scroll narrative | `scrollytelling-web` |
| Pin/scrub ScrollTrigger mechanics | `gsap-scrolltrigger` |
| Animation runtime performance | `gsap-performance` |
| Spatial environments / walkthroughs | `threejs-spatial-experiences` |
| Exploded/3D product storytelling | `threejs-product-storytelling` |
| Product UI / a11y engineering | `frontend-ui-engineering` |
| Tests first | `test-driven-development` |
| Debug | `debugging-and-error-recovery` |
| Security boundary | `security-and-hardening` |
| Postgres / Supabase | `supabase-postgres-best-practices` |
| Done claims | `verification-before-completion` |
| Hard external gates | `verification-gauntlet` (`agentit verify`) |

If a skill is in `skills_recommended_missing`, either enable the profile that provides it, load it from `~/code/agentit/skills/…` if present, or state that it is unavailable.

### 4. Execute with single-agent-first + specialist escalation

- Default topology: `direct` (you do the work).
- If a matching skill is enough, load it directly.
- If specialization, context isolation, independent review, or creative diversity materially helps, select a role from `agents/catalog.yaml` and delegate with `specialist-agent-routing`.
- Use `design competition` only for genuinely high-ambition concept work.
- Any subagent must go through the Worker Context Contract (`agentit worker build` / `router/worker_context.py`): project instructions, task skills, preferences, risk, I/O, verifier. Precedence: `safety > user > project > preferences > defaults`.
- One writer owns each file/shared state. Proposal/research/review specialists should normally be read-only.

### 5. Context engines (when noisy)

```bash
agentit context filter <file>
agentit context archive <file> --description "…"
agentit context dedup "…" --session <id>
agentit artifact get|read|grep agentit://…
```

Do not use context compression as a reason to strip design references that materially affect the requested visual result.

### 6. MCP (when tools are needed)

```bash
agentit mcp status
agentit mcp enable <id> --apply
agentit mcp enable-stack developer_core --apply
agentit mcp enable-stack design_studio --apply
```

Plan-first without `--apply`. RISK_3/4 needs `--force` where required. Prefer `context7` for live library docs, `github` for PRs, and Playwright/DevTools for browser proof.

For Figma-driven work, use the **official remote Figma MCP** and OAuth. The `design_studio` MCP stack combines Figma, Context7, Playwright, and Chrome DevTools. Never put a Figma credential/token in the repository.

For inspiration/tool research, use live web/browser access when available. Social sources such as TikTok are browser-first and may require an isolated authenticated profile; never bypass access controls. Treat catalogs such as `designengineer.tools` as discovery surfaces, then verify implementation choices against current primary documentation.

### 7. Verify before done (gauntlet)

- No **done / fixed / passing** claim without **fresh command evidence** from this turn after the last relevant edit (`verification-before-completion`).
- For implementation work, run the signal-gated gauntlet:

```bash
agentit verify "task summary" --project <project_root>
agentit verify "task summary" --project <project_root> --apply
```

- Honor router `verification` flags (tests, dry-run, backup, independent review).
- RISK_3/RISK_4: full fidelity, human review for critical ops; do not lower inferred risk.
- If `verification-before-completion` or `verification-gauntlet` is in `skills_available`, treat them as mandatory for close-out.
- Design completion additionally needs rendered evidence when browser tooling is available; scrollytelling/spatial experiences need the full sequence tested, not a hero screenshot.
- Premium/high-ambition design should receive independent visual critique after implementation.
- Close-out shape: what changed · verify receipt path · blocking probe statuses · checklist evidence · residual risk.
- **Anti-greenwash:** agent-authored “200 tests passed” without gauntlet receipt is not completion.

## Session bootstrap reply (first turn after trigger)

When the user only says “usa agentit” / “use agentit” without a task:

1. Confirm Agentit is active.
2. Ask for the concrete task **or** wait for the next message.
3. Do not invent work.

When the user pairs the trigger with a task (“usa agentit y haz X”):

1. Route immediately.
2. Enable profiles / load skills.
3. Decide direct vs specialist topology.
4. Execute and verify.
5. Report: what changed, evidence, residual risks.

## Safety (non-negotiable)

- Scope only what the user asked.
- No commits, push, deploy, remote migrations, or external messages without explicit ask.
- No destructive production ops without human gates from the router.
- Do not reverse harness-managed files without cause; update with `bash ~/code/agentit/update.sh` / `install.sh` as documented.

## See also

- Specialist role catalog: `~/code/agentit/agents/catalog.yaml`
- Global policy: `~/AGENTS.md` and `~/code/agentit/AGENTS.md`
- Skill discovery map: `using-agent-skills`
- Router skill detail: `task-router`
- Adaptive topology: `architect-orchestrator`
