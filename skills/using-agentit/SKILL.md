---
name: using-agentit
description: Activate Agentit end-to-end. Triggered by natural use/usa/utilise agentit (any language). Intelligent skill packs, MCP fit, delegation, critique, verify, PR-first.
---

# Using Agentit

Single entrypoint for coding sessions. Provider-neutral. **Intelligent orchestration**: a strong main agent (Architect) with a tiny always-on skill core; load only the domain pack needed; spawn specialists when useful; always independent critique for large structural plans.

## Activation (only special phrase)

Natural language in any language that means **use Agentit**, for example:

- English: use agentit, using agentit, with agentit
- Spanish: usa agentit, usando agentit
- Other: utilise agentit, mit agentit, usa agentit, … as long as **agentit** is clearly the harness

**No other powerwords.** Ordinary prompts drive routing (files, “and”, “at the same time”, “frontend and backend”, “review and fix”, “several agents”, etc.). If jargon appears, treat it as ordinary English/Spanish — never require it.

Once activated, follow this playbook for the rest of the session without waiting for more magic words.

## Fixed paths

| Item | Path |
|---|---|
| Harness root | `~/code/agentit` |
| CLI | `agentit` |
| Router | `python3 ~/code/agentit/router/route.py "…"` |
| Effort / packs | `~/code/agentit/effort/levels.yaml` |
| Specialists | `~/code/agentit/agents/catalog.yaml` |
| Skills | `~/code/agentit/skills/<id>/SKILL.md` |
| Continuity policy | `~/code/agentit/docs/PROJECT_CONTINUITY.md` |
| Project state | `<project>/docs/agentit/STATE.md` |
| MCP catalog | `~/code/agentit/mcp/catalog.yaml` |

## Core protocol

1. Classify mechanical bypass vs product-affecting work.
2. Product work → `interview-me` (batch all material questions; **craft depth only for design/visual**).
3. Persist confirmed intent in continuity state.
4. Route: `agentit trace "…" --project .` or `python3 router/route.py "…"`.
5. Load **skill_budget**: always_core + `load_now` only — never the full catalog.
6. MCP fit when tooling matters: `mcp-tooling-fit` (status → fit → disable noise → discover gaps → plan install).
7. Execute with intelligent delegation (no hard subagent caps).
8. Critic on large structural plans before committing implementation.
9. Verify with evidence; PR-first for repo changes.
10. Keep STATE.md current.

## Domain packs (not universal Studio)

Pick a pack from profiles / router `domain_pack`:

engineering · frontend · design · backend · data · product · writing · release · research · role:custom

**Craft depth Standard/Polished/Studio applies only to design/visual work.**

Token estimates come from router `token_estimate` (project-aware). Fixed historical ranges are not bills.

## Always-core skills (tiny)

- `using-agentit`, `architect-orchestrator`, `using-agent-skills`, `task-router`
- `mcp-tooling-fit` when tooling decisions matter
- `specialist-agent-routing` when spawning
- verification skills when mutating code

Everything else is JIT from the domain pack / role.

## User roles

If the user says “act as X expert”, load role-relevant skills + always_core only. If missing locally, use `find-skills` / marketplace and propose install — do not invent coverage.

## Delegation

- Default is intelligent, not dogmatic single-agent and not forced multi-agent.
- Spawn when independence, isolation, domain specialty, or critique wins.
- If the user asks for many agents without independence, **push back** with a short reason.
- No hard min/max subagent quotas; router `subagents.recommended` is advisory.
- **Critic required** when `critic_required` is true or the plan is large/structural.

## MCP

```bash
agentit mcp status --project .
agentit mcp enable-stack developer_core --project .   # plan
agentit mcp enable context7 --project . --apply       # after OK
```

Discover beyond local catalog with `mcp-tooling-fit` (marketplace + web). Installs are plan-first + user approval.

## Playbook summary

| Step | Action |
|---|---|
| 0 | Activate on natural agentit phrase; load this skill |
| 1 | Interview if product work (domain pack; craft depth only if visual) |
| 2 | Persist STATE.md |
| 3 | Route + skill_budget + MCP fit |
| 4 | Plan; critic if structural/large |
| 5 | Implement with specialists only when useful |
| 6 | Verify evidence; update state |
| 7 | Branch + PR by default |

## Safety

- Scope only what was asked
- PR-first unless explicit override
- No deploy/remote migrations without authorization
- Safety > speed
- Never write secrets into continuity docs

## See also

- `effort/levels.yaml`
- `docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`
- `docs/PROJECT_CONTINUITY.md`
- `skills/mcp-tooling-fit`
- `skills/architect-orchestrator`
- `agents/catalog.yaml`
