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

## Design exception: quality over context thrift

General engineering work still uses progressive disclosure. **Serious design work is the explicit exception to token thrift.** Do not weaken art direction, motion analysis, visual QA, or design-system inspection merely to minimize context.

When the `design` profile is active, load the foundational trio for non-trivial visual work:

1. `design-taste-frontend` — art direction, visual thesis, composition, type/material/motion intensity;
2. `impeccable-design` — craft director, critique/polish/hardening, responsive and state completeness;
3. `emil-design-eng` — interaction feel, animation decisions, perceived performance, invisible detail.

Then load specialists by signal:

| Signal | Add |
|---|---|
| Figma link/frame/design system/Code Connect | `figma-design-workflow` + official `figma` MCP |
| scroll-driven / scrollytelling / pinned / scrub / parallax / image sequence | `scrollytelling-web` + `gsap-scrolltrigger` + `gsap-performance` |
| product explodes/decomposes/disassembles, GLB/glTF, true 3D camera/material work | previous scroll stack + `threejs-product-storytelling` |
| ordinary micro-interaction / component motion | keep `emil-design-eng`; do not escalate to cinematic tooling without cause |

This is intentional context spending. Avoid loading every specialist for a simple button, but when the task is a cinematic landing, the complete relevant stack should be in context.

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

For any non-trivial request whose main success criterion is visual design, motion direction, landing-page craft, visual redesign, scrollytelling, or product presentation, prefer activating **`design`** instead of stopping at `frontend`.

Do **not** enable `all` unless the user asks.

### 3. Load task-relevant skills

For each id in `skills_available` and project-active skills that match the task:

1. Open `SKILL.md` (harness path first).
2. Follow its process; load references when a step needs them.
3. For general engineering, avoid dumping unrelated skills into context.
4. For design, apply the quality-first exception above: foundational design skills can be loaded together and specialist stacks should be loaded when their signal is present.

High-value specialized skills:

| Need | Skill |
|------|--------|
| Art direction / landing / portfolio / visual redesign | `design-taste-frontend` |
| Design critique / polish / responsive craft | `impeccable-design` |
| Product UI interaction / motion feel | `emil-design-eng` |
| Figma design-to-code / design-system context | `figma-design-workflow` |
| Cinematic scroll narrative | `scrollytelling-web` |
| Pin/scrub ScrollTrigger mechanics | `gsap-scrolltrigger` |
| Animation runtime performance | `gsap-performance` |
| Exploded/3D product storytelling | `threejs-product-storytelling` |
| Product UI / a11y engineering | `frontend-ui-engineering` |
| Tests first | `test-driven-development` |
| Debug | `debugging-and-error-recovery` |
| Security boundary | `security-and-hardening` |
| Postgres / Supabase | `supabase-postgres-best-practices` |
| Done claims | `verification-before-completion` |
| Hard external gates | `verification-gauntlet` (`agentit verify`) |

If a skill is in `skills_recommended_missing`, either enable the profile that provides it, load it from `~/code/agentit/skills/…` if present, or state that it is unavailable.

### 4. Execute with single-agent-first

- Default topology: `direct` (you do the work).
- Spawn subagents only if topology is `probe` / `fan_out` / `pipeline` / `writer_reviewer` / `audit` **and** independence or isolation is real.
- Any subagent must go through the Worker Context Contract (`agentit worker build` / `router/worker_context.py`): project instructions, task skills, preferences, risk, I/O, verifier. Precedence: `safety > user > project > preferences > defaults`.

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
- Design completion additionally needs rendered evidence when browser tooling is available; scrollytelling needs the full sequence tested, not a hero screenshot.
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
3. Execute and verify.
4. Report: what changed, evidence, residual risks.

## Safety (non-negotiable)

- Scope only what the user asked.
- No commits, push, deploy, remote migrations, or external messages without explicit ask.
- No destructive production ops without human gates from the router.
- Do not reverse harness-managed files without cause; update with `bash ~/code/agentit/update.sh` / `install.sh` as documented.

## See also

- Global policy: `~/AGENTS.md` and `~/code/agentit/AGENTS.md`
- Skill discovery map: `using-agent-skills`
- Router skill detail: `task-router`
- Adaptive topology: `architect-orchestrator`
