---
name: using-agentit
description: Activate Agentit end-to-end. Use when the user says "use agentit", "usa agentit", "with agentit", "usando agentit", or asks to run work under the Agentit harness.
---

# Using Agentit

Single entrypoint for coding sessions. Agentit is provider-neutral and single-agent-first, but can interview, route, delegate specialists, research, implement, and verify when the task warrants it.

## Fixed paths

| Item | Path |
|---|---|
| Harness root | `~/code/agentit` |
| CLI | `agentit` |
| Router | `python3 ~/code/agentit/router/route.py "…"` |
| Effort catalog | `~/code/agentit/effort/levels.yaml` |
| Specialist catalog | `~/code/agentit/agents/catalog.yaml` |
| Skills | `~/code/agentit/skills/<id>/SKILL.md` |
| Project skills | `<project>/.agents/skills/` |
| MCP catalog | `~/code/agentit/mcp/catalog.yaml` |

## Core protocol

When Agentit is active:

1. classify the task as **mechanical bypass** or **product-affecting work**;
2. for product-affecting work, run `interview-me` **before planning**;
3. during that interview, recommend and get confirmation for **Standard / Polished / Studio**;
4. route the confirmed task;
5. load only relevant skills/profiles;
6. choose direct vs specialist execution according to the confirmed effort level and actual benefit;
7. implement;
8. verify before claiming completion.

The point is adaptive spending: efficient by default, extravagant only when the user knowingly chooses a level where extra context/research/iteration has enough marginal value.

## Mandatory interview for product work

Interview is not only for ambiguous prompts. It is the normal gate for **anything that creates or changes a product decision**: a feature, page, component behavior, UX, visual design, architecture, API, data model, workflow, copy, positioning, automation behavior, or other meaningful implementation tradeoff.

The interview may be extremely short when the task is already clear. A one-question confirmation is still an interview.

### Mechanical bypass

Skip interview only for exact mechanical chores that save time without choosing or changing product behavior, such as:

- creating explicitly named directories/files;
- exact moves/renames;
- running an explicitly requested command/test;
- deterministic formatting;
- copying exact content to a known location.

Do **not** bypass because a product task is easy. `Change the navbar behavior`, `add a settings page`, `add an endpoint`, or `rewrite this CTA` are product-affecting and must pass interview.

If unsure, interview.

Facts are the agent's job: inspect repo/docs/tools/live sources. Decisions/preferences belong in the interview.

## Effort levels

Canonical machine-readable policy: `effort/levels.yaml`.

Every product-affecting interview must recommend and confirm one level.

| Level | Goal | Typical total model tokens* | Typical behavior |
|---|---|---:|---|
| **Standard** | efficient production-quality work | ~15k-80k | focused implementation, minimal research, usually one agent, basic QA |
| **Polished** | visibly stronger quality | ~50k-250k | targeted research, more edge-case/polish work, 0-2 specialists when useful, more iteration |
| **Studio** | quality-first / flagship work | ~150k-800k+ | deep discovery, broad relevant research, concept exploration, specialists/competition when useful, independent critique, extensive polish |

\* Rough total-session envelopes across parent + delegated model calls. They are not billing guarantees and vary by task, provider, model, context, retries, tool output, and implementation size.

### Recommendation contract

Do not present the levels as a blind menu. The interview must say:

- which level is recommended and why;
- how the expected result changes if the user goes lower/higher;
- rough token envelope and relative cost;
- likely research, specialist, and iteration depth.

The user must explicitly confirm the level before implementation. An explicit `Studio`, `go all out`, `keep this Standard`, etc. counts when unambiguous.

If work later wants to materially exceed the confirmed level, ask before escalating. Correctness/safety are exceptions: never knowingly ship broken/unsafe work merely to preserve a token budget.

## Effort controls behavior, not correctness

### Standard

Default recommendation for ordinary clear product work when extra exploration has low marginal value.

- single agent by default;
- progressive disclosure and small context;
- research only for needed/current facts;
- no design competition;
- specialists only with a concrete payoff;
- focused tests/browser checks;
- usually 1-2 fix/verification cycles.

### Polished

Use when public-facing quality, maintainability, edge cases, or craft deserve extra work.

- targeted research where useful;
- compare approaches when the choice matters;
- 0-2 specialists normally;
- stronger responsive/state/edge-case QA;
- independent review when it has real value;
- several critique/fix cycles.

### Studio

Use when quality dominates token efficiency: flagship portfolio/company sites, important launches, premium creative work, or exceptionally difficult architecture/research.

- deep interview where needed;
- broad/current research where it can improve the outcome;
- specialist fan-out and/or model diversity when useful;
- multiple creative/architectural directions when concept uncertainty matters;
- design competition allowed;
- independent critique/performance passes;
- iterate until remaining improvements are marginal relative to cost.

**Studio is not synonymous with design.** A simple design task can be Standard. A hard architecture/research task can be Studio.

## Specialist agents

`agents/catalog.yaml` defines reusable semantic specialists. A specialist is a role + skill bundle + bounded output contract, not a permanent fake employee.

Spawn/delegate only when specialization, fresh context, independence, parallelism, different tooling/model capability, creative diversity, or independent review beats coordination overhead.

Useful roles include `ui-researcher`, `trend-researcher`, `creative-tool-scout`, `visual-storytelling-director`, `spatial-experience-designer`, `delight-and-whimsy`, `design-critic`, `performance-benchmarker`, `api-tester`, `backend-architect`, and others in the catalog.

Effort level is a budget ceiling/intent signal, not an agent quota. Even Studio should use zero subagents when they add nothing.

## Provider-neutral execution

Agentit describes capabilities, not provider-specific APIs. A specialist is not inherently a Claude subagent, Codex worker, Gemini agent, Grok worker, or any branded primitive.

Use the best mechanism available:

1. native subagent/worker;
2. isolated delegated model/tool call;
3. separate fresh-context invocation;
4. parent agent loads the same specialist skill bundle and executes directly.

Objective, skills, constraints, I/O ownership, expected output, verification, and stop condition remain semantically equivalent. Multi-agent execution is an optimization, never a correctness dependency.

Shared Agentit policy must work across OpenAI, Anthropic, Google, xAI, and compatible future providers.

## Design routing

For non-trivial visual work, the design profile can provide:

- `design-taste-frontend` — art direction;
- `impeccable-design` — critique/polish/responsive craft;
- `emil-design-eng` — interaction/motion feel;
- `design-inspiration-research` / `design-trend-researcher` — current references/trends;
- `creative-web-experiences` — concept generation;
- `visual-storytelling-director` — narrative/scene pacing;
- `creative-tool-scout` — current implementation tooling;
- `figma-design-workflow` — Figma/design-system context;
- `scrollytelling-web` + GSAP — scroll narratives;
- `threejs-spatial-experiences` — stores/showrooms/rooms/worlds;
- `threejs-product-storytelling` — real 3D product work;
- `delight-and-whimsy` — restrained memorable details.

Do not load all of these merely because `design` is active. **Effort level decides how deep to go.**

- Standard design: minimum relevant craft skills + browser check.
- Polished design: foundation + targeted specialists/research + stronger QA.
- Studio design: full relevant craft stack, research/concept exploration, specialists/competition when useful, independent critique and performance/browser loops.

### Design competition

Only normally available at Studio (or an explicit equivalent user request). Shared brief → 2-3 genuinely different concepts → explicit judging by brand fit, originality, clarity, usability, feasibility, performance and memorability → winner/justified hybrid → implementation → independent critique.

Never use it for routine UI maintenance.

## Playbook

### 0. Interview + effort gate

- mechanical bypass → proceed immediately;
- product-affecting → load `interview-me`;
- resolve material user decisions;
- recommend Standard/Polished/Studio with result/cost consequences;
- get explicit effort confirmation.

### 1. Route

```bash
python3 ~/code/agentit/router/route.py "confirmed task description"
agentit trace "confirmed task description" --project <project_root>
```

Treat router output as a plan, never permission for destructive operations.

### 2. Activate JIT profiles

```bash
agentit enable <profile> --project <project_root> --apply
agentit status --project <project_root>
```

Common profiles: `frontend`, `design`, `backend`, `supabase`, `product`, `writing`, `release`, `research`. Never enable `all` unless explicitly requested.

### 3. Load task-relevant skills

Use progressive disclosure. Standard should be context-efficient. Polished spends more only when valuable. Studio may intentionally spend substantial context when quality benefits.

### 4. Execute direct vs specialists

Default is direct. Select specialists from `agents/catalog.yaml` only when their expected value exceeds coordination cost and remains consistent with the confirmed effort level.

Delegated specialists receive the Worker Context Contract semantics: project instructions, task skills, preferences, risk, I/O, verifier, stop condition. One writer per file/shared state.

### 5. Context engines

```bash
agentit context filter <file>
agentit context archive <file> --description "…"
agentit context dedup "…" --session <id>
agentit artifact get|read|grep agentit://…
```

### 6. MCP/tools

```bash
agentit mcp status
agentit mcp enable <id> --apply
agentit mcp enable-stack developer_core --apply
agentit mcp enable-stack design_studio --apply
```

Use current primary docs for technical choices. Browser/social inspiration research is optional and effort-dependent; never bypass access controls.

### 7. Verify before done

No done/fixed/passing claim without fresh evidence after the last relevant edit.

```bash
agentit verify "task summary" --project <project_root>
agentit verify "task summary" --project <project_root> --apply
```

Respect risk gates. Design work needs rendered evidence when browser tooling is available. Studio visual work should normally receive independent visual/performance critique.

## Session bootstrap

If user says only `usa agentit`, confirm activation and wait for the task.

If user says `usa agentit y haz X`:

1. classify mechanical vs product;
2. if product, interview + effort confirmation;
3. route;
4. load profiles/skills;
5. execute at confirmed effort;
6. verify;
7. report evidence and residual risks.

## Safety

- scope only what the user asked;
- no commits/push/deploy/remote migrations/external messages without explicit authorization;
- no destructive production operations without required human gates;
- safety/correctness outrank effort budget.

## See also

- `effort/levels.yaml`
- `docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`
- `agents/catalog.yaml`
- `architect-orchestrator`
- `task-router`
- `using-agent-skills`
