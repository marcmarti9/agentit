# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**An open-source, provider-neutral reliability and just-in-time expertise layer for capable AI agents.**

Agentit does not replace Codex, Claude Code, or another capable agent. It gives the active model a small operating protocol for the parts that still fail in real work: interpreting the actual task, deciding when extra process is worth its cost, loading only relevant expertise, challenging weak decisions, using current evidence when needed, delegating deliberately, preserving project state, verifying from fresh evidence, keeping durable documentation aligned, and shipping reviewable changes.

The key design constraint is simple:

> **Keep startup context tiny. Let the model decide what it needs. Load deeper skills, references, tools and workers only just in time.**

```text
You + a capable AI agent
           │
           ▼
 first meaningful task
           │
           ▼
DISPATCH_DECISION: bare | agentit
        │                 │
        │                 └── material work / uncertain
        │                            │
        │                            ▼
        │                   tiny global Agentit core
        │                   ┌──────────────────────┐
        │                   │ using-agentit        │
        │                   │ task-router          │
        │                   │ using-agent-skills   │
        │                   └──────────────────────┘
        │                            │
        │                            ▼
        │                   semantic domain pack(s)
        │                  engineering / design / ...
        │                            │
        │                            ▼
        │                   selected skill bodies only
        │                  + references/tools JIT
        │                            │
        │                            ▼
        │                   independent decision audit
        │                            │
        │                            ▼
        │                    Loop / Graph execution
        │                            │
        │                            ▼
        │                  fresh verification + docs/state
        │                            │
        │                            ▼
        │                    branch → PR → human merge
        │
        └── trivial work → direct execution + local verification
```

> **Status:** Agentit is early-stage and evolving quickly. Its mechanical safety/runtime contracts are tested; it does **not** claim that a prompt harness universally makes every model better, cheaper, or faster. See [Evaluation](#evaluation) for exactly what is and is not measured.

## Human UX: no terminal ceremony

Agentit is designed to be **operated by the agent, not by the human through a CLI**.

After installation, a fresh compatible agent should make a semantic first-task choice:

```text
DISPATCH_DECISION: bare | agentit
```

- `bare` is for trivial/conversational work or tiny obvious mechanical actions where Agentit would add no material value.
- `agentit` is preferred for material work: non-trivial implementation/debugging, design, research, current/source-sensitive domains, multi-step changes, ambiguous product decisions, tool/MCP decisions, long-running work or higher-risk changes.
- if the choice is genuinely uncertain, prefer `agentit`.

The user can always force the Agentit path naturally:

```text
use Agentit
```

or:

```text
usa Agentit
```

That is an explicit selection, not a magic powerword. Once Agentit is installed/discoverable, the user should not need to prepend it to every material request.

On first use, if Agentit is not installed yet, give the coding agent this repository and ask it to install and use Agentit. The **agent** owns inspecting the bootstrap plan, applying it when authorized, resolving skills/profiles, running verification, maintaining receipts, configuring approved tooling and persisting continuity state.

The repository contains command-line interfaces because agents benefit from deterministic mechanical surfaces. They are **agent-facing APIs and maintainer/debugging tools**, not a terminal workflow the human is expected to memorize.

## Why Agentit exists

Modern frontier agents are already capable enough that many remaining failures are process/context failures rather than raw code-generation failures:

- the agent solves the wrong interpretation of the task;
- it rubber-stamps the user's proposed method when a materially better route exists;
- a plausible first plan is never challenged independently;
- every skill/tool is dumped into context whether useful or not;
- useful domain expertise exists but is never discovered at the right moment;
- stale model memory is used for current APIs, laws, prices, standards or platform behavior;
- a social post or bookmark is treated as evidence instead of following it to the underlying source;
- subagents are spawned for theatre, or useful independent review is skipped;
- workers inherit giant contexts instead of the bounded knowledge required for their job;
- a worker loses project rules or prior decisions;
- "done" is claimed from stale or incomplete evidence;
- code changes while architecture/operations docs silently drift;
- long tasks become impossible to resume cleanly after a context reset.

Agentit turns those failure modes into explicit, inspectable contracts while leaving semantic judgment with the model that has the richest task context.

## Architecture

### 1. The global core is intentionally tiny

A normal Agentit installation exposes exactly the navigation layer globally:

```text
using-agentit
+ task-router
+ using-agent-skills
```

Everything else is JIT.

Debugging, TDD, security, design, source research, reference intelligence, MCP selection, orchestration, long-horizon recovery and specialist verification are not supposed to sit in every prompt's context just because they exist in the repository.

This is the main difference between Agentit and a giant prompt/skill bundle: **availability is not the same thing as context injection**.

### 2. Packs are semantic maps, not bundles or levels

Runtime packs live in [`skills/using-agent-skills/references/packs.md`](skills/using-agent-skills/references/packs.md).

Current maps include domains such as:

```text
engineering  frontend  design  backend  data  product
marketing    seo       research writing  release agency
```

A pack answers:

> What capabilities exist around this domain, and when might each one help?

It does **not** define:

- mandatory skills;
- a required order;
- a minimum or maximum count;
- a "normal" number of skills;
- `basic / advanced`, `essential / standard / deep`, or any other hidden tier system.

The primary AI can inspect one or several packs and select zero, one or many concrete skills depending on the actual stage.

For example:

```text
relevant_packs:
- design
- frontend

selected_skills:
- design-inspiration-research
- browser-testing-with-devtools
```

Only the selected skill bodies belong in execution context. **The pack is a map; it is not the luggage.**

### 3. Profiles and runtime packs solve different problems

[`profiles.yaml`](profiles.yaml) is an **installation/discovery inventory**. Profiles make capability sets available to provider adapters and project environments.

Runtime packs are **model-readable semantic maps** used to discover which individual skill bodies may be worth loading for the current task.

That distinction matters:

```text
profile enabled / skill installed
             ≠
skill body injected into every worker
```

Even the `design` or `all` profile must never become a giant worker-context dump. Runtime selection remains JIT.

### 4. The model decides; Python does not pretend to understand the prompt

Agentit has **no regex/keyword/scoring router for natural-language intent**.

The active primary AI owns semantic decisions from the real conversation, repository, files, tools, constraints and prior state:

```text
intent / outcome
known facts / material unknowns
relevant pack(s)
risk / reversibility / external effects
selected skills
selected tools
reference plan
worker topology
implementation plan
verification / rollback / post-check
user-method assessment
```

Mechanical code starts *after* that decision. It handles things software is actually good at: manifests, profiles, capability inventories, state, commands, Loop/Graph contracts, verification receipts, MCP configuration and reversible file operations.

See [`docs/NO_PROGRAMMATIC_ROUTER.md`](docs/NO_PROGRAMMATIC_ROUTER.md) and [`docs/LLM_NATIVE_DECISION_PROTOCOL.md`](docs/LLM_NATIVE_DECISION_PROTOCOL.md).

### 5. Reference Intelligence is also JIT

External knowledge is not globally loaded either.

Every material `TASK_DECISION` can choose:

```text
reference_plan.mode: none | curated | live | both
```

- `none` — external knowledge would not materially change the result.
- `curated` — Agentit already contains a reusable playbook/reference for the recurring problem.
- `live` — correctness depends on current or domain-authoritative sources.
- `both` — a curated procedure structures the work while current sources establish the facts.

Examples:

```text
local rename                 -> none
premium public website       -> curated + current implementation sources when needed
SEO investigation            -> curated procedure + live site/search/platform evidence
current tax/legal work       -> live authoritative domain sources
```

When external knowledge matters, `reference-intelligence` is loaded as a concrete JIT skill. The primary AI decides what sources matter; Agentit does not introduce a second keyword-based reference router.

Recurring knowledge is distilled next to the skill that actually uses it, for example:

- [`skills/design-inspiration-research/references/premium-web-production.md`](skills/design-inspiration-research/references/premium-web-production.md)
- [`skills/marketing-and-growth/references/marketing-operating-system.md`](skills/marketing-and-growth/references/marketing-operating-system.md)
- [`skills/marketing-and-growth/references/seo-growth-loop.md`](skills/marketing-and-growth/references/seo-growth-loop.md)
- [`skills/marketing-and-growth/references/launch-content-system.md`](skills/marketing-and-growth/references/launch-content-system.md)

The global [`references/INDEX.md`](references/INDEX.md) stays intentionally small. Agentit should distill durable procedures and source roles, not become a 10,000-link bookmark database.

See [`docs/REFERENCE_INTELLIGENCE.md`](docs/REFERENCE_INTELLIGENCE.md).

### 6. The agent should disagree when disagreement helps

Agentit is deliberately **not a yes-man protocol**.

If the user says “build X using A”, the agent separates the desired outcome (**X**) from the proposed method (**A**) unless A is an explicit hard requirement. When inspection shows that B is materially better on correctness, simplicity, maintainability, security, reversibility, performance, UX, cost, migration risk or architecture fit, the agent should say so and recommend B.

That is **constructive dissent, not insubordination**. A strong recommendation does not authorize destructive actions, hidden scope expansion, spend, deploys or ignoring the user's informed final choice. Safety and authorization constraints remain hard boundaries.

### 7. Material decisions get an independent audit

Before material execution, Agentit asks a bounded independent model to challenge the reviewed task decision:

```text
AUDIT: CLEAR | CHALLENGE | ESCALATE
FINDINGS:
- ...
SUGGESTED_CHECKS:
- ...
CONFIDENCE: low | medium | high
```

Ordinary work can use the cheapest competent independent reviewer. High-consequence work—production, destructive operations, auth, payments, secrets, PII, difficult migrations, major architecture or unresolved disagreement—requires stronger independent review.

The reviewer is a critic, not another semantic router and not a decorative manager.

### 8. Workers receive bounded context

Specialists are spawned only when isolation, expertise, independent judgment, breadth or parallelism provides a concrete benefit.

A worker receives conceptually bounded context:

```text
role / objective
relevant pack labels
selected skill bodies
selected references
project constraints
allowed tools / permissions
read/write ownership
expected handoff
verification / stop condition
```

Whole-pack or whole-catalog dumps are a failure mode. One worker saying “it works” is not acceptance.

### 9. Execution has mechanical receipts

For executable work, Agentit separates semantic judgment from mechanical acceptance:

- **Loop Contract** — observable goal, verifier, stop condition, attempt budget and escalation boundary.
- **Graph Contract** — explicit DAG, dependencies, write ownership, handoff artifacts and Loop Contracts for nodes.

Fresh verifier evidence and the applicable receipt decide whether the work is accepted.

See [`docs/RUNTIME_ENGINEERING.md`](docs/RUNTIME_ENGINEERING.md).

### 10. Sessions are disposable; project knowledge is not

Substantial work maintains a compact canonical state file at `docs/agentit/STATE.md` (or an existing project-equivalent source of truth) so another session/provider can resume without reconstructing the chat.

Durable architecture, component, contract, operations, troubleshooting and ADR-style knowledge belongs in normal project documentation. Agentit checks for documentation drift before substantial repository work is considered complete.

See [`docs/PROJECT_CONTINUITY.md`](docs/PROJECT_CONTINUITY.md) and [`docs/DOCUMENTATION_CONTRACT.md`](docs/DOCUMENTATION_CONTRACT.md).

## First-run/bootstrap contract

The **human should not need to execute installer commands**. A compatible coding agent can bootstrap Agentit on the user's behalf after being given this repository.

The canonical bootstrap is a **portable Python path for macOS and GNU/Linux**. It does not require Bash 4, GNU coreutils, Homebrew, `sha256sum`, `stat -c`, `mv -T` or `mapfile`.

Internally, an agent can inspect a read-only plan and then apply it:

```text
python3 bootstrap.py --provider <claude|codex|antigravity|all>
python3 bootstrap.py --provider <...> --apply
```

Those commands are shown for transparency and maintainers; a normal user should just ask the coding agent to install Agentit.

The bootstrap creates:

- a self-contained runtime at `~/.agentit/runtime`;
- a private Python environment at `~/.agentit/venv` for runtime dependencies;
- bounded provider discovery surfaces containing only the global core;
- provider-specific bounded agent profiles where applicable;
- an agent-facing CLI shim at `~/.local/bin/agentit`.

The coding agent may call the returned CLI path directly; the human does not need to modify `PATH`.

### Bootstrap safety and rollback

The portable bootstrap is plan-first and uses:

- source/destination symlink rejection;
- explicit packaging/provider allowlists in `bootstrap-manifest.json`;
- SHA-256 verification;
- per-file backup of replaced destinations;
- atomic replacement;
- a machine-readable bootstrap receipt;
- fail-closed rollback if an installed destination changed afterward.

The receipt path returned after apply can be used by the agent to inspect or apply rollback:

```text
python3 bootstrap.py --rollback <receipt-manifest>
python3 bootstrap.py --rollback <receipt-manifest> --apply
```

Rollback intentionally does not recursively delete `~/.agentit/venv` or arbitrary directories. It changes only files proven safe by the receipt.

The normal bootstrap path does **not** overwrite general provider credentials/configuration. Settings/hooks are separate explicit opt-ins, not part of launch installation.

The legacy `install.sh` / `update.sh` path remains GNU/Linux-oriented for compatibility and is no longer the canonical cross-platform bootstrap.

Providers currently represented by adapters/discovery are Claude Code, OpenAI Codex and Antigravity/Open-Skills-style environments. Provider credentials and machine-local secrets are never portable project state.

## The operating lifecycle

For a fresh task:

1. **Inspect enough real context to dispatch correctly.** Choose `bare | agentit` semantically; explicit “use Agentit” forces the Agentit path unless a higher-priority rule prevents it.
2. **Keep trivial work trivial.** If `bare`, execute directly and verify locally without manufacturing orchestration ceremony.
3. **For material work, create `TASK_DECISION`.** Outcome, known facts, unknowns, risk, reversibility, external effects, relevant packs, candidate skills/tools/references, topology, implementation plan and verification strategy.
4. **Inspect the relevant semantic pack(s).** Packs expose possibilities; they never prescribe counts, tiers or order.
5. **Load only the concrete skills the current stage earns.** Zero, one or many can be correct.
6. **Choose references and tools JIT.** Use `none | curated | live | both` for references and least-privilege external tooling only when it materially helps.
7. **Challenge the proposed method when warranted.** Preserve the user's outcome and hard constraints; surface materially better alternatives instead of rubber-stamping.
8. **Audit material decisions independently.** Cheap capable reviewer for ordinary work; stronger critic when risk or disagreement warrants it.
9. **Interview only unresolved product decisions.** Ask one consolidated, recommendation-led round instead of silently inventing product intent.
10. **Execute directly or delegate for a concrete reason.** Specialization, isolation, parallel investigation, context separation or independent judgment—not agent theatre.
11. **Use Loop/Graph contracts for executable work.** Bound retries, define evidence, fail closed and escalate instead of weakening the verifier.
12. **Persist continuity and durable docs when warranted.** Sessions should be replaceable; architecture/operations/contracts/decisions should not drift.
13. **Verify from fresh evidence.** No `done`, `fixed`, `passing`, `secure`, `premium` or equivalent claim from memory, a worker summary or stale output.
14. **Ship repository changes through reviewable Git by default.** Branch → commits → PR → reviewer/user merge decision.

Canonical end-to-end playbook: [`skills/using-agentit/SKILL.md`](skills/using-agentit/SKILL.md).

## Agent-facing mechanical interfaces

Humans should not have to drive these manually. They exist so the active agent can turn reviewed semantic decisions into deterministic, inspectable operations.

Examples include:

- portable bootstrap and rollback;
- profile activation/discovery (`status`, `enable`, `disable`);
- explicit-signal verification (`verify --signal ...`);
- continuity state/checkpoints;
- Loop/Graph runtime state and receipts;
- worker-context construction;
- MCP status/configuration;
- capability/inventory resolution.

The boundary is deliberate: **the AI decides what the task means; software executes explicit mechanical instructions**.

## Profiles

Profiles are installation/discovery bundles for agents and provider adapters. They are **not runtime context tiers**.

| Profile | Intended discovery/install scope |
|---|---|
| `core` | exactly the three-skill global navigation bootstrap |
| `frontend` | UI engineering, browser/runtime checks, performance, simplification |
| `backend` | interfaces, observability, performance, simplification |
| `supabase` | backend + PostgreSQL/Supabase-specific guidance |
| `product` | discovery, specs, product/growth decision support |
| `writing` | technical docs and editing |
| `design` | deeper UI/UX research, art direction, motion/spatial craft |
| `release` | CI, migrations, launch readiness |
| `research` | source-driven/context-heavy investigation |
| `growth` / `agency` | productized growth/agency workflows |
| `all` | every repository skill; explicit installation/discovery only |

Even when a broad profile is available, runtime workers receive only the selected skill bodies justified by the current `TASK_DECISION`.

## Verification

Agentit's verification runtime is signal-gated. Mechanical project facts can be detected automatically; semantic facts chosen by the active AI are passed explicitly so Python never becomes a disguised natural-language router.

The current catalog includes project-native tests/build checks, secret scans, acceptance/red→green checks and task-scoped checks for surfaces such as auth, HTTP, Postgres/Supabase and browser/UI work.

References are inputs to the plan, not proof that the implementation works. When reference use matters to acceptance, it belongs alongside the real outcome checks in the normal Loop/Graph verifier.

See [`probes/catalog.yaml`](probes/catalog.yaml).

## Evaluation

Agentit intentionally separates **mechanical correctness** from **claims about model quality**.

Mechanical tests cover profile activation, manifests, path/symlink safety, capabilities, MCP state, continuity, worker context, Loop/Graph runtime, verification receipts, portable bootstrap/rollback and architecture-policy invariants.

What the repository does **not** currently prove:

- that Agentit universally improves coding quality versus a raw frontier agent;
- that it reduces tokens, latency or cost;
- that independent review is always worth its extra inference cost;
- that every provider follows every natural-language policy with equal reliability.

Those claims require agent-level comparative evals, not deterministic prompt classifiers. See [`evals/evaluation-plan.md`](evals/evaluation-plan.md) and [`evals/results.md`](evals/results.md).

## Maintainer testing

The repository has deterministic mechanical suites and CI. Maintainers and coding agents may invoke the underlying test commands directly; normal users should not need to.

CI validates runtime/utility suites, legacy shell syntax where applicable, registry YAML/JSON, profile/catalog integrity, architecture-policy invariants and the **real portable bootstrap on both macOS and Ubuntu**. Public claims should refer to the CI result for the exact commit being discussed, not an old local run.

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | tiny portable global operating rules and first-task dispatch |
| `bootstrap.py` / `router/bootstrap.py` | portable agent-facing install/rollback path |
| `bootstrap-manifest.json` | mechanical runtime/provider packaging manifest |
| `skills/using-agentit/` | compact end-to-end Agentit protocol |
| `skills/task-router/` | model-owned `TASK_DECISION` + reviewer contracts |
| `skills/using-agent-skills/` | JIT skill discovery/projection rules |
| `skills/using-agent-skills/references/packs.md` | canonical flat runtime pack maps |
| `skills/reference-intelligence/` | JIT external-knowledge/provenance discipline |
| `skills/` | curated concrete JIT knowledge modules |
| `references/INDEX.md` | deliberately small global reference discovery index |
| `agents/` | portable specialist roles |
| `router/` | mechanical profiles, capabilities, context, Loop/Graph, MCP and verification runtime |
| `profiles.yaml` | installation/discovery profile composition |
| `probes/` | verification catalog + mechanical probes |
| `docs/` | canonical architecture/policy/runtime/continuity docs |
| `templates/project/REFERENCES.md` | lightweight project provenance template |
| `templates/` | explicit non-secret provider/project templates; machine-local `.local` files stay untracked |
| `incubator/` | candidate/rejected capability research |
| `.codex/agents/` | bounded Codex worker profiles |
| `reports/` | dated research/history; not all reports describe the current architecture |

## Contributing

Contributions are welcome, especially when they remove a real failure mode **without turning Agentit into a giant framework or prompt database**.

Before adding a skill, prefer this order:

```text
already covered? → strengthen the existing skill
upstream skill solves it better? → adapt with provenance/license
truly distinct repeated workflow? → incubate → evaluate → promote
one-off advice? → do not add a skill
```

For external references, prefer the same progressive-disclosure mindset:

```text
bookmark / source
→ inspect the useful underlying asset
→ extract durable procedure or evidence role
→ enrich the skill that actually uses it
→ keep live/current facts live when freshness matters
```

See [`docs/SKILL_CURATION.md`](docs/SKILL_CURATION.md), [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Documentation map

| Document | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | global dispatch and Agentit operating rules |
| [`skills/using-agentit/SKILL.md`](skills/using-agentit/SKILL.md) | canonical compact lifecycle |
| [`skills/using-agent-skills/references/packs.md`](skills/using-agent-skills/references/packs.md) | flat semantic runtime packs |
| [`docs/REFERENCE_INTELLIGENCE.md`](docs/REFERENCE_INTELLIGENCE.md) | curated/live reference architecture and provenance |
| [`docs/NO_PROGRAMMATIC_ROUTER.md`](docs/NO_PROGRAMMATIC_ROUTER.md) | AI judgment vs mechanical software boundary |
| [`docs/LLM_NATIVE_DECISION_PROTOCOL.md`](docs/LLM_NATIVE_DECISION_PROTOCOL.md) | primary decision + independent review |
| [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md) | interview/provider semantics |
| [`docs/PROJECT_CONTINUITY.md`](docs/PROJECT_CONTINUITY.md) | resumable state contract |
| [`docs/DOCUMENTATION_CONTRACT.md`](docs/DOCUMENTATION_CONTRACT.md) | durable system-documentation contract |
| [`docs/RUNTIME_ENGINEERING.md`](docs/RUNTIME_ENGINEERING.md) | Loop/Graph execution contracts |
| [`docs/CAPABILITIES.md`](docs/CAPABILITIES.md) | capability resolution / least privilege |
| [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md) | MCP catalog/runtime |
| [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md) | orchestration topologies / specialist contracts |
| [`docs/SKILL_CURATION.md`](docs/SKILL_CURATION.md) | skill lifecycle, upstream provenance and promotion policy |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | upstream provenance and licenses |

## License

Agentit is licensed under the [Apache License, Version 2.0](LICENSE). Third-party material retains its applicable notices in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
