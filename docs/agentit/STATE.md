# Agentit project state

**Updated:** 2026-08-12  
**Status:** implementing on branch feat/intelligent-orchestration-v1 — push + PR next  
**Branch:** feat/intelligent-orchestration-v1  
**PR:** pending  
**Mode:** Agentit active; local implementation in progress

## Goal (revised)

Make Agentit **intelligent orchestration**, not dogmatic single-agent-first:

1. Main agent is a strong general organizer (Architect) with a **small always-on skill core**.
2. Load **only task-relevant skill families**; never dump design/studio stack onto backend work.
3. **Spawn specialists when useful** — no forced multi, no forced solo, no hard min/max caps.
4. **Always independent critique** before committing to large structural plans.
5. **MCP fit**: audit installed + catalog + marketplace/internet; enable/disable/install with plan-first safety.
6. **Token budgets estimated from real project/task**, not fixed Standard/Polished/Studio envelopes.
7. Standard/Polished/Studio return to **design craft depth only** (frontend/visual), not universal effort.

## User direction (confirmed intent)

- Profiles/skill families exist so the agent picks the **right family per task** — currently ignored in practice (Studio/Polished asked for every product task).
- Fixed token ranges (15k–80k etc.) are not realistic; estimate per project.
- Not full single-agent-first: intelligent spawn when better; if user asks multi-agent, main agent may push back if unnecessary.
- Subagents = domain specialists with scoped skills (why so many skills exist).
- User role (“act as finance expert”) → load that domain’s skills + tiny universal core only.
- Missing skills/MCPs → search marketplace/internet and propose install.
- Large structural proposals → always a critic subagent so the main agent doesn’t lock onto its own plan.
- No hard subagent min/max caps; effort-style knobs for design only, not global multi-agent bureaucracy.

## Diagnosis add-on (effort / skills / MCP)

### Why Studio/Polished/Standard leaked everywhere

- `effort/levels.yaml` + `interview-me` + `using-agentit` mandate effort on **all product work**.
- Profiles already encode families (`frontend`, `backend`, `design`, `product`…) but interview asks craft depth as if every task were a landing page.
- Design profile description explicitly ties itself to Standard/Polished/Studio; that model was generalized incorrectly.

### Why too many skills load

- Policy text encourages “load recommended skills” without a hard **budget of skill bodies**.
- `core` profile already includes frontend + several engineering skills globally.
- Router recommends skill **ids** but agents often load whole profiles / design stack by habit.

### MCP gap

- Runtime exists: `agentit mcp status|available|enable|disable|enable-stack|recommend` + agentit-manager tools.
- Missing: a **skill playbook** that forces (1) inventory, (2) fit to project, (3) disable unused, (4) search catalog + marketplace + web, (5) dry-run install, (6) human gate for RISK_3+.

### Parallelism (from prior diagnosis)

- Router still keyword-only; `recommended: 0` even on fan_out; multi-agent overrides broken; no structural independence score.

## Target architecture (agreed direction)

### A. Three orthogonal axes (replace one universal “effort”)

| Axis | Purpose | Values (proposal) |
|---|---|---|
| **Domain pack** | Which skill family + MCP stack | engineering / frontend / design / backend / data / product / writing / release / research / role-custom |
| **Craft depth** | Only for visual/design tasks | standard \| polished \| studio (or skip if non-design) |
| **Spend / rigor** | Main-agent thoroughness (optional, soft) | lean \| normal \| thorough — **no token fixed ranges**; estimate from project signals |

Interview asks craft depth **only if** the task is visual/design. Non-design product work asks domain intent + constraints, not Studio.

### B. Skill loading policy

```
always_core (tiny):
  using-agentit | architect-orchestrator | using-agent-skills | task-router
  verification-before-completion | verification-gauntlet (when mutating)
  + planning / code-review only when planning or reviewing

task_family (JIT, 1–N skills):
  from profiles.yaml + registry category + role hint

never:
  design_studio stack on pure backend
  entire catalog into parent or worker
```

Role override: user says “experto en finanzas” → finance skills (or find/install) + always_core; skip frontend/design.

### C. Delegation policy (no caps)

- Default: intelligent, not “0 subagents”.
- Spawn when independence, isolation, specialist domain, or independent critique wins.
- Soft guidance only (suggested count from decomposition), **no hard min/max**.
- User requests multi-agent → Architect evaluates and may decline with reason.
- **Critic gate:** any non-trivial structural plan / large work proposal → independent critic subagent before implementation commitment.

### D. Token estimate (project-aware)

Router or a small estimator uses signals:

- repo size / touched modules estimate
- risk
- domain pack
- whether UI browser loops needed
- planned specialist count (if any)

Output: `token_estimate: { low, high, basis: [...] }` — not the fixed 15k–80k table.

### E. MCP skill (new)

`skills/mcp-tooling-fit/SKILL.md` (name TBD):

1. `agentit mcp status` + list active vs catalog
2. Infer project stack (package.json, docker, supabase, etc.)
3. Recommend enable stack / disable unused
4. Search curated catalog + skills marketplace / web for gaps
5. Plan install (dry-run); apply only with user consent / --apply; RISK_3+ force

### F. Parallelism decision (keep from prior plan)

- Structural signals + overrides + score
- No hard caps; recommended is advisory
- RISK raises verification, does not forbid independent parallel packages

## Implementation phases (revised)

### Phase A — Policy pivot (docs + catalogs)  
Deprecate universal Standard/Polished/Studio for all product work; craft depth design-only; update interview-me, using-agentit, effort/levels.yaml shape, AGENTIT_INTERVIEW policy, AGENTS.md.

### Phase B — Router: domain pack + skill budget + token estimate  
Extend `route_task` with domain_pack, skill_budget, token_estimate, craft_depth (optional), delegation_advice without hard caps.

### Phase C — Parallelism intelligence  
Signals, overrides, recommended≠0 when useful, critic_required flag for large plans.

### Phase D — MCP tooling fit skill + wire into playbook  
New skill + registry + profile hook (core or research) + tests.

### Phase E — Architect core strengthening  
Ensure architect-orchestrator + specialist-agent-routing encode: smart spawn, critic gate, skill family projection, pushback on unnecessary multi-agent.

### Phase F — Evals/tests  
Cases for: backend without design skills; design craft depth; critic_required; multi-agent pushback; MCP recommend; multi-path fan_out; role-scoped skills.

## Open decisions for user

1. Name for non-design thoroughness: **lean/normal/thorough** vs drop named tiers and only estimate tokens?
2. Critic gate threshold: always on “structural plan with large work” — OK as qualitative rule?
3. MCP skill may propose install from internet — always require explicit user approve before `--apply`? (recommend yes)
4. Keep profile names (`frontend`, `design`, …) as the domain packs?

## Defaults if user says “procede”

- lean/normal/thorough as soft spend (optional interview only when ambiguous)
- craft depth design-only
- critic gate on large structural plans
- MCP install always plan-first + user confirm
- profiles as domain packs
- soft delegation guidance, no hard caps
- implement on `feat/intelligent-orchestration-v1` local branch

## Verification so far

- Prior router probes (parallelism too conservative).
- Confirmed effort policy is universal; design profile owns Studio language.
- MCP runtime + catalog exist; skill playbook missing.
- No implementation commits yet.

## Next

User confirms revised plan → branch → Phase A+B first slice.
