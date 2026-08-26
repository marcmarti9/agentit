# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**A provider-neutral reliability and just-in-time expertise layer for capable AI agents.**

Agentit gives coding agents a compact operating protocol for material work: choose the right expertise only when it is useful, challenge important decisions independently, use current references when needed, delegate with bounded context, preserve project state, verify execution with fresh evidence, and ship reviewable changes.

It is open source under Apache-2.0 and is designed to sit around the coding agent you already use.

```text
You + capable coding agent
          │
          ▼
 DISPATCH: bare | agentit
          │
          ▼
   tiny Agentit core
          │
          ▼
 semantic domain packs
          │
          ▼
 selected skills only
 + references/tools JIT
          │
          ▼
 independent decision audit
          │
          ▼
 Loop / Graph execution
          │
          ▼
 fresh verification
 + resumable project state
          │
          ▼
 branch → PR → human merge
```

## Quick start

Give this repository to a compatible coding agent and ask it:

```text
Install Agentit for this environment, inspect the installation plan before applying it,
and then use Agentit automatically for material work.
```

After installation, work normally. The agent makes a first-task semantic decision:

```text
DISPATCH_DECISION: bare | agentit
```

Trivial work can stay direct. Material work activates Agentit's JIT workflow.

For maintainers and agents that want the explicit bootstrap surface:

```bash
python3 bootstrap.py --provider <claude|codex|antigravity>
python3 bootstrap.py --provider <claude|codex|antigravity> --apply
```

The canonical bootstrap supports macOS and GNU/Linux and produces verified, reversible installation state.

## What Agentit gives an agent

### Tiny global core

A normal installation exposes only three global navigation skills:

```text
using-agentit
+ task-router
+ using-agent-skills
```

Everything deeper is loaded just in time.

### Agent-owned task decisions

The active model owns semantic judgment from the real conversation, repository, files, tools, constraints and project state.

For material work it creates a compact `TASK_DECISION` covering the relevant outcome, unknowns, risk, skills, references, tools, topology, ownership, plan and verification strategy.

Mechanical software then enforces the reviewed plan through deterministic state and execution contracts.

### JIT skill packs

Agentit organizes expertise into flat semantic discovery maps such as:

```text
engineering  frontend  design  backend  data  product
marketing    seo       research writing  models release agency
```

A pack helps the model discover useful capabilities. The model chooses the concrete skill bodies and how many are worth their context cost.

Example:

```text
relevant_packs:
- engineering

selected_skills:
- debugging-and-error-recovery
- verification-before-completion
```

Only selected skill bodies enter the working context.

### Reference Intelligence

For material tasks the model can choose:

```text
reference_plan.mode: none | curated | live | both
```

Agentit can combine reusable curated procedures with live authoritative sources when freshness or domain authority matters. Durable external knowledge can be distilled into the skill that actually uses it while provenance remains explicit.

### Independent decision review

Material `TASK_DECISION`s can receive a bounded independent review:

```text
AUDIT: CLEAR | CHALLENGE | ESCALATE
```

The reviewer checks intent, risk, skill/reference/tool selection, delegation, ownership and verification. Higher-consequence work can escalate to a stronger independent critic.

### Adaptive delegation

The primary model can choose direct execution or a useful topology such as:

```text
direct
probe
fan_out
pipeline
writer_reviewer
audit
custom DAG
```

Delegated workers receive bounded context: objective, selected skills, selected references, project constraints, permissions, ownership, handoff and verifier.

### Loop Engineering

Every executable unit can be bound to a Loop Contract:

```text
observable goal
→ action
→ fresh evidence
→ verifier
→ accept / retry / escalate
```

Loops have explicit stop conditions, bounded attempts and persisted receipts.

### Graph Engineering

Multi-node work can be materialized as a DAG with explicit:

- dependencies;
- read/write ownership;
- handoff artifacts;
- per-node Loop Contracts;
- final Graph Receipt.

The runtime validates execution state and prevents invalid dependency or ownership transitions.

### Resumable project state

Substantial work can maintain compact continuity state in:

```text
docs/agentit/STATE.md
.agentit/checkpoints/*.json
```

A fresh session, provider or machine can recover the objective, decisions, branch/PR, verification status, blockers and next actions from repository state instead of reconstructing a chat transcript.

### Provider-neutral capabilities

Agentit uses stable capability IDs and explicit host inventories so semantic roles are not tied to one vendor-specific tool name.

Capability resolution produces least-privilege envelopes containing the selected provider binding and the permissions required for that task.

### MCP runtime

Agentit includes a curated MCP catalog and runtime management surface. It can inspect, enable and disable approved MCP integrations for supported hosts while keeping semantic selection with the primary model.

Current MCP configuration surfaces include Claude Code, Cursor, Codex, Grok, Antigravity and portable project `.mcp.json` files.

### Verification receipts

Agentit records fresh evidence rather than accepting narrative success. Verification can include project-native tests/builds, explicit semantic verification signals, Loop Receipts and Graph Receipts.

### Durable documentation

Material architecture, contracts, operations and decisions stay in normal project documentation. Continuity state records only the compact operational information required to resume work.

### Reviewable Git workflow

Repository changes default to:

```text
work branch → implementation → fresh verification → pull request → human merge
```

## Example flow

A request such as:

```text
Fix the authentication regression and make sure it cannot silently recur.
```

can produce a task-specific Agentit flow like:

```text
DISPATCH_DECISION: agentit

packs:
- engineering

selected skills:
- debugging-and-error-recovery
- security-and-hardening
- verification-before-completion

reference plan:
- current sources only if the implementation depends on a changing API/protocol

review:
- independent decision audit

execution:
- reproduce
- localize
- implement bounded fix
- run Loop verifier
- preserve relevant regression coverage
- create PR with fresh evidence
```

The exact skills, references, tools and topology remain decisions of the active model for the actual task.

## Architecture boundary

Agentit separates two kinds of work:

```text
LLM judgment
├─ understand intent
├─ choose packs / skills / references / tools
├─ assess risk and alternatives
├─ choose topology
└─ define verification

Deterministic runtime
├─ manifests and profiles
├─ capability resolution
├─ MCP configuration
├─ continuity state
├─ Loop / Graph state machines
├─ verification receipts
└─ reversible bootstrap operations
```

This keeps semantic interpretation with the model that has the richest context while making execution state inspectable and testable.

## Installation and discovery profiles

`profiles.yaml` controls installation/discovery availability. Runtime skill selection remains JIT.

| Profile | Discovery scope |
|---|---|
| `core` | three-skill Agentit navigation core |
| `frontend` | frontend implementation and runtime verification |
| `backend` | APIs, services, observability and backend engineering |
| `supabase` | backend plus PostgreSQL/Supabase-specific guidance |
| `product` | discovery, requirements and product decisions |
| `writing` | technical writing and documentation |
| `design` | UI/UX, visual direction, motion and spatial craft |
| `release` | CI/CD, migrations and release readiness |
| `research` | source-driven and context-heavy research |
| `growth` / `agency` | marketing, growth and multi-domain delivery |
| `all` | complete repository skill inventory |

## Safety and reversibility

Agentit's mechanical surfaces are designed around explicit state and bounded mutation. The portable bootstrap includes:

- read-only planning before apply;
- bounded provider/package allowlists;
- symlink checks;
- SHA-256 verification;
- per-file backups;
- atomic replacement;
- machine-readable receipts;
- rollback guarded against post-install user modifications.

Risk-sensitive Agentit work can require independent review, rollback planning, dry runs and post-change verification according to the task's actual impact.

## Evaluation

Agentit keeps mechanical/runtime evaluation separate from agent-quality evaluation.

CI covers deterministic contracts including bootstrap/rollback, profiles, capability and MCP resolution, continuity, worker context, Loop/Graph execution, verification receipts and architecture-policy invariants.

Paired real-agent evaluation is tracked in [issue #29](https://github.com/marcmarti9/agentit/issues/29). The protocol compares the same model/provider/environment with and without Agentit and records task success, regressions, retries, model calls, exposed token usage, elapsed time, interventions, verifier evidence and documentation drift.

Benchmark claims are intended to follow that evidence rather than precede it.

See:

- [`evals/evaluation-plan.md`](evals/evaluation-plan.md)
- [`evals/results.md`](evals/results.md)

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | compact global Agentit rules and dispatch |
| `skills/using-agentit/` | canonical Agentit lifecycle |
| `skills/task-router/` | model-owned task decision + review contract |
| `skills/using-agent-skills/` | semantic pack discovery and JIT projection |
| `skills/reference-intelligence/` | curated/live source and provenance workflow |
| `skills/` | concrete JIT expertise modules |
| `router/` | deterministic capabilities, context, Loop/Graph, MCP and verification runtime |
| `profiles.yaml` | installation/discovery profiles |
| `probes/` | mechanical verification catalog |
| `docs/` | architecture, runtime, continuity and policy documentation |
| `evals/` | mechanical and paired agent-level evaluation plan/results |

## Core docs

- [`skills/using-agentit/SKILL.md`](skills/using-agentit/SKILL.md)
- [`skills/using-agent-skills/references/packs.md`](skills/using-agent-skills/references/packs.md)
- [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md)
- [`docs/RUNTIME_ENGINEERING.md`](docs/RUNTIME_ENGINEERING.md)
- [`docs/PROJECT_CONTINUITY.md`](docs/PROJECT_CONTINUITY.md)
- [`docs/CAPABILITIES.md`](docs/CAPABILITIES.md)
- [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md)
- [`docs/REFERENCE_INTELLIGENCE.md`](docs/REFERENCE_INTELLIGENCE.md)
- [`evals/evaluation-plan.md`](evals/evaluation-plan.md)

## Contributing

Contributions are welcome when they add durable capability, improve execution contracts, strengthen verification, expand provider portability, or remove unnecessary protocol cost.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/SKILL_CURATION.md`](docs/SKILL_CURATION.md).

## License

Apache License 2.0. See [`LICENSE`](LICENSE) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).