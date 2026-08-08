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
- For landings/visual work, run design read + dials (`design-taste-frontend`) — not purple-template defaults.
- Never claim done without fresh command evidence (`verification-before-completion`).
- Touch only the requested scope; no drive-by refactors.
- If something is ambiguous and expensive to reverse, stop and ask **one** sharp question.

This is the practical meaning of “usa agentit”: more discipline, not more agents.

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

Do **not** enable `all` unless the user asks.

### 3. Load only recommended skills

For each id in `skills_available` (and project-active skills that match the task):

1. Open `SKILL.md` (harness path first).
2. Follow its process; load `references/*` only when a step needs them.
3. Never dump the full skill catalog into context.

High-value specialized skills (examples):

| Need | Skill |
|------|--------|
| Landing / portfolio / visual redesign | `design-taste-frontend` |
| Product UI / a11y | `frontend-ui-engineering` |
| Light anti-slop checklist | `anti-ai-slop-design` |
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

### 6. MCP (when tools are needed)

```bash
agentit mcp status
agentit mcp enable <id> --apply
agentit mcp enable-stack developer_core --apply
```

Plan-first without `--apply`. RISK_3/4 needs `--force` where required. Prefer `context7` for live library docs, `github` for PRs, `playwright` for browser proof.

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
