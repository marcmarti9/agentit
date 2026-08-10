---
name: using-agentit
description: Activate Agentit end-to-end. Use when the user says "use agentit", "usa agentit", "with agentit", "usando agentit", or asks to run work under the Agentit harness.
---

# Using Agentit

Single entrypoint for coding sessions. Agentit is provider-neutral and single-agent-first, but can interview, route, delegate specialists, research, implement, document, and verify when the task warrants it.

## Fixed paths

| Item | Path |
|---|---|
| Harness root | `~/code/agentit` |
| CLI | `agentit` |
| Router | `python3 ~/code/agentit/router/route.py "…"` |
| Effort catalog | `~/code/agentit/effort/levels.yaml` |
| Specialist catalog | `~/code/agentit/agents/catalog.yaml` |
| Skills | `~/code/agentit/skills/<id>/SKILL.md` |
| Project continuity policy | `~/code/agentit/docs/PROJECT_CONTINUITY.md` |
| Canonical project state | `<project>/docs/agentit/STATE.md` unless the project already defines an equivalent |
| Project skills | `<project>/.agents/skills/` |
| MCP catalog | `~/code/agentit/mcp/catalog.yaml` |

## Core protocol

When Agentit is active:

1. classify the task as **mechanical bypass** or **product-affecting work**;
2. for product-affecting work, run `interview-me` before planning;
3. ask **all currently identifiable material interview questions in one batch**, including the recommended **Standard / Polished / Studio** level;
4. persist the confirmed intent and effort level in project continuity state;
5. route the confirmed task;
6. load only relevant skills/profiles;
7. choose direct vs specialist execution according to the confirmed effort level and actual benefit;
8. implement on a work branch and use a PR by default for repository changes;
9. keep continuity documentation current while work progresses;
10. verify before claiming completion.

The point is adaptive spending and resumable work: efficient by default, extravagant only when the user knowingly chooses it, and never dependent on one chat session surviving.

## Mandatory interview for product work

Interview is the normal gate for anything that creates or changes a product decision: feature, page, component behavior, UX, visual design, architecture, API, data model, workflow, copy, positioning, automation behavior, or meaningful implementation tradeoff.

Skip interview only for exact mechanical chores with no product decision, such as exact directory/file creation, moves/renames, deterministic formatting, running an explicitly requested command/test, or copying exact content.

Facts are the agent's job: inspect repo/docs/tools/live sources first. Decisions/preferences belong in the interview.

### Batch interview rule

Do not drip-feed known questions one by one. After inspecting discoverable facts, assemble every material user decision you can already identify and ask them in one numbered batch with a recommendation/default on each.

Preferred shape:

`one comprehensive batch -> one user reply -> persist state -> build`.

A second interview round is allowed only when the first answers expose genuinely new material decisions that could not reasonably have been known before. The second round must again contain all newly identifiable questions at once.

## Effort levels

Canonical policy: `effort/levels.yaml`.

| Level | Goal | Typical total model tokens* | Typical behavior |
|---|---|---:|---|
| **Standard** | efficient production-quality work | ~15k-80k | focused implementation, minimal research, usually one agent, basic QA |
| **Polished** | visibly stronger quality | ~50k-250k | targeted research, better edge-case/polish work, 0-2 specialists when useful, more iteration |
| **Studio** | quality-first / flagship work | ~150k-800k+ | deep discovery, broad relevant research, concept exploration, specialists/competition when useful, independent critique, extensive polish |

\* Rough total-session envelopes across parent + delegated calls, not billing guarantees.

The interview must recommend a level, explain what moving lower/higher changes, give the rough token envelope, and get explicit user confirmation before implementation. If execution later wants to materially exceed the level, ask before escalating unless extra work is required for correctness/safety.

## Effort controls behavior, not correctness

### Standard

- single agent by default;
- progressive disclosure and tight context;
- research only for needed/current facts;
- specialists only with clear payoff;
- focused tests/browser checks;
- usually 1-2 fix/verification cycles.

### Polished

- targeted research;
- compare approaches when the choice matters;
- 0-2 specialists normally;
- stronger responsive/state/edge-case QA;
- independent review when valuable;
- several critique/fix cycles.

### Studio

- deep discovery where needed;
- broad/current research when valuable;
- specialist fan-out/model diversity when useful;
- multiple creative/architectural directions when concept uncertainty matters;
- design competition allowed;
- independent critique/performance passes;
- iterate until remaining improvements are marginal relative to cost.

Studio is not synonymous with design. A simple visual task can be Standard; a hard architecture/research task can be Studio.

## Continuity: chat context is disposable

**Everything needed to resume meaningful work must live outside the conversation.** Assume the current session can disappear at any time because of token exhaustion, model/provider switch, app crash, machine switch, or user pause.

Canonical policy: `docs/PROJECT_CONTINUITY.md`.

For every product-affecting task, maintain `docs/agentit/STATE.md` in the target project unless an equivalent canonical state doc already exists.

At minimum persist:

- current goal and why;
- confirmed intent, audience, success criteria, constraints, non-goals;
- confirmed Standard/Polished/Studio level;
- current status: complete / in progress / blocked / not started;
- durable technical/product/design decisions and rationale;
- important files, artifacts, branch and PR;
- verification commands/results;
- next executable actions;
- open questions/blockers.

Update the state immediately after interview confirmation, after expensive-to-rediscover decisions, after meaningful milestones, before any handoff/pause/context exhaustion, and before completion.

Do not persist secrets, credentials, chain-of-thought, full chat transcripts, or giant tool dumps. Store compact operational state and point to canonical artifacts.

### Resume protocol

When continuing an existing task/session/project:

1. read `docs/agentit/STATE.md` (or recorded equivalent) before asking the user to repeat anything;
2. inspect the referenced branch/PR/diff and only the files needed next;
3. verify stale assumptions;
4. repair missing/stale state before proceeding;
5. do not re-interview decisions already documented unless the task changed materially.

A fresh agent should be able to answer: what are we doing, why, what has been decided, what exists now, what has been verified, and what should happen next?

## Git workflow: PR-first by default

For repository mutations, Agentit defaults to:

`work branch -> commits -> verification -> pull request -> user/reviewer decision`.

Rules:

- do not write commits directly onto the default branch by default;
- do not merge a PR automatically by default;
- do not push/fast-forward `main`/`master` directly unless the user explicitly asks for that exception or project instructions explicitly require another workflow;
- documentation/continuity updates belong on the same branch/PR as the implementation they describe;
- if the user explicitly says direct-to-main for a specific task, that instruction overrides the PR-first default for that task only.

This policy is provider-neutral and applies whether execution is through OpenAI, Anthropic, Google, xAI, or another compatible client.

## Specialist agents

`agents/catalog.yaml` defines reusable semantic specialists. Spawn/delegate only when specialization, fresh context, independence, parallelism, different tooling/model capability, creative diversity, or independent review beats coordination overhead.

Effort level is a budget/intent signal, not an agent quota. Even Studio should use zero children when they add nothing.

Provider fallback order:

1. native subagent/worker;
2. isolated delegated model/tool call;
3. separate fresh-context invocation;
4. parent loads the same specialist skill bundle and executes directly.

Multi-agent execution is an optimization, never a correctness dependency.

## Design routing

For non-trivial visual work, relevant design capabilities include:

- `ui-ux-pro-max-intelligence` — JIT product/style/color/typography/UX/chart/icon/motion/stack intelligence from the upstream searchable database;
- `design-taste-frontend` — art direction;
- `impeccable-design` — critique/polish/responsive craft;
- `emil-design-eng` — interaction/motion feel;
- `design-inspiration-research` / `design-trend-researcher` — live references/trends;
- `creative-web-experiences` — concept generation;
- `visual-storytelling-director` — narrative/scene pacing;
- `creative-tool-scout` — current implementation tooling;
- `figma-design-workflow` — Figma/design-system context;
- `scrollytelling-web` + GSAP — scroll narratives;
- `threejs-spatial-experiences` — spatial worlds;
- `threejs-product-storytelling` — real 3D product work;
- `delight-and-whimsy` — restrained memorable details.

UI UX Pro Max is an **intelligence source**, not the creative director. Query it JIT and summarize relevant results; do not dump its entire database into context or let presets override brand/product judgment.

Effort depth:

- Standard design: minimum relevant craft guidance, optional narrow UI/UX intelligence lookup, browser check.
- Polished design: targeted UI/UX intelligence + foundation + targeted research/specialists + stronger QA.
- Studio design: UI/UX intelligence as one evidence source among live research, concept exploration, full relevant craft stack, independent critique, performance/browser loops.

### Design competition

Normally Studio-only (or explicit equivalent user instruction). Shared brief -> 2-3 genuinely different concepts -> explicit judging by brand fit, originality, clarity, usability, feasibility, performance and memorability -> winner/justified hybrid -> implementation -> independent critique.

## Playbook

### 0. Interview + effort

- mechanical bypass -> proceed;
- product-affecting -> inspect facts, then load `interview-me`;
- ask all currently known material questions in one batch;
- recommend/confirm Standard, Polished, or Studio;
- persist confirmed intent in project continuity state.

### 1. Route

```bash
python3 ~/code/agentit/router/route.py "confirmed task description"
agentit trace "confirmed task description" --project <project_root>
```

### 2. Activate JIT profiles

```bash
agentit enable <profile> --project <project_root> --apply
agentit status --project <project_root>
```

Common profiles: `frontend`, `design`, `backend`, `supabase`, `product`, `writing`, `release`, `research`. Never enable `all` unless explicitly requested.

### 3. Load task-relevant skills

Use progressive disclosure. Standard stays tight. Polished spends selectively. Studio may intentionally spend substantial context when quality benefits.

### 4. Execute direct vs specialists

Default direct. Specialists receive the Worker Context Contract: project instructions, task skills, preferences, risk, I/O, verifier, stop condition. One writer per file/shared state.

### 5. Keep continuity state current

After milestones/decisions, update the project's state document before moving on. Before any expected context/session boundary, checkpoint first.

### 6. Context/MCP/tools

```bash
agentit context filter <file>
agentit context archive <file> --description "…"
agentit context dedup "…" --session <id>
agentit artifact get|read|grep agentit://…

agentit mcp status
agentit mcp enable <id> --apply
agentit mcp enable-stack developer_core --apply
agentit mcp enable-stack design_studio --apply
```

Use current primary docs for technical choices. Never bypass access controls.

### 7. Verify before done

No done/fixed/passing claim without fresh evidence after the last relevant edit.

```bash
agentit verify "task summary" --project <project_root>
agentit verify "task summary" --project <project_root> --apply
```

Update continuity state with the final verification result and remaining risk.

### 8. Deliver through PR by default

If repository changes were made, ensure the work branch and continuity docs are current, open/update the PR, and leave merge to the user unless explicitly authorized otherwise.

## Session bootstrap

If user says only `usa agentit`, confirm activation and wait for the task.

If user says `usa agentit y haz X`:

1. classify mechanical vs product;
2. product -> batch interview + effort confirmation;
3. persist state;
4. route/load skills;
5. execute at confirmed effort;
6. continuously document;
7. verify;
8. PR by default;
9. report evidence, PR/state location, and residual risks.

## Safety

- scope only what the user asked;
- PR-first repository workflow unless explicitly overridden;
- no deploy/remote migrations/external messages without authorization;
- no destructive production operations without required gates;
- safety/correctness outrank effort budget;
- never write secrets into continuity docs.

## See also

- `effort/levels.yaml`
- `docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`
- `docs/PROJECT_CONTINUITY.md`
- `agents/catalog.yaml`
- `architect-orchestrator`
- `task-router`
- `using-agent-skills`
