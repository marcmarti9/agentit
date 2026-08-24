# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/version-v0.3.2--stable-green.svg)](https://github.com/marcmarti9/agentit/releases)

**An open-source, provider-neutral reliability layer for AI coding agents.**

Agentit does not replace Codex, Claude Code, or another capable coding agent. It gives the agent a shared operating protocol for the parts that still go wrong in real repositories: understanding the actual task, challenging risky decisions, loading only relevant skills, delegating deliberately, preserving state, verifying with fresh evidence, keeping durable documentation aligned, and shipping through reviewable Git changes.

```text
You + your coding agent
          │
          ▼
      use agentit
          │
          ▼
inspect real project state
          │
          ▼
primary task decision ──► independent decision audit
          │                         │
          │                 challenge / escalate
          ▼
JIT skills + tools + bounded delegation
          │
          ▼
Loop / Graph execution contracts
          │
          ▼
fresh verification + docs drift check
          │
          ▼
branch → commits → pull request → human merge decision
```

> **Status:** Agentit is early-stage and evolving quickly. Its mechanical safety/runtime contracts are tested; it does **not** claim that a prompt harness universally makes every model better, cheaper, or faster. See [Evaluation](#evaluation) for exactly what is and is not measured.

## Why Agentit exists

Modern coding agents are already very capable. The remaining failure modes are often process failures rather than code-generation failures:

- the agent solves the wrong interpretation of the task;
- a plausible first plan is never challenged;
- every skill/tool is dumped into context whether useful or not;
- subagents are spawned for theatre, or useful independent review is skipped;
- a worker loses project rules or prior decisions;
- "done" is claimed from stale or incomplete evidence;
- the code changes but architecture/operations docs silently drift;
- long tasks become impossible to resume cleanly after a context reset.

Agentit turns those failure modes into explicit, inspectable contracts while leaving semantic judgment with the model that has the full context.

## What makes it different

### The model decides; Python does not pretend to understand the prompt

Agentit has **no regex/keyword/scoring router for natural-language intent**. The active primary AI owns a structured `TASK_DECISION` from the conversation, repository, files, tools, constraints, and prior state.

Mechanical code starts *after* that decision. It handles things software is actually good at: manifests, profiles, capability inventories, Loop/Graph state, verification receipts, continuity artifacts, MCP configuration, and reversible file operations.

See [`docs/NO_PROGRAMMATIC_ROUTER.md`](docs/NO_PROGRAMMATIC_ROUTER.md).

### A second model challenges material decisions

Before material execution, Agentit asks an independent model to return:

```text
AUDIT: CLEAR | CHALLENGE | ESCALATE
FINDINGS:
- ...
SUGGESTED_CHECKS:
- ...
CONFIDENCE: low | medium | high
```

Ordinary work can use a cheap/fast reviewer. High-consequence work—production, destructive operations, auth, payments, secrets, PII, difficult migrations, or major architecture—requires stronger independent review.

The reviewer is not another decorative manager. It exists to catch a bad first decision while changing it is still cheap.

See [`docs/LLM_NATIVE_DECISION_PROTOCOL.md`](docs/LLM_NATIVE_DECISION_PROTOCOL.md).

### Skills and specialists are just-in-time

Agentit ships a curated skill library, but the whole catalog is not meant to be loaded for every task. `profiles.yaml` groups capabilities and keeps the globally visible `core` bounded; domain/design/release/research packs are opt-in and task-scoped.

A skill only counts as used when the executing model actually receives its body. A specialist only gets the context and capabilities required for its bounded job.

### Execution has receipts

For executable work, Agentit separates semantic judgment from mechanical acceptance:

- **Loop Contract** — observable goal, verifier, stop condition, attempt budget, escalation boundary.
- **Graph Contract** — explicit DAG, dependencies, write ownership, handoff artifacts, and Loop Contracts for nodes.

"The worker says it worked" is not acceptance. Fresh verifier evidence and the applicable receipt are.

See [`docs/RUNTIME_ENGINEERING.md`](docs/RUNTIME_ENGINEERING.md).

### Sessions are disposable; project knowledge is not

Substantial work maintains a compact canonical state file at `docs/agentit/STATE.md` (or an existing project-equivalent source of truth) so another session/provider can resume without reconstructing the chat.

Durable architecture, component, contract, operations, troubleshooting, and ADR-style knowledge belongs in normal project documentation. Agentit explicitly checks for documentation drift before substantial repository work is considered complete.

See [`docs/PROJECT_CONTINUITY.md`](docs/PROJECT_CONTINUITY.md) and [`docs/DOCUMENTATION_CONTRACT.md`](docs/DOCUMENTATION_CONTRACT.md).

## 60-second tour

After installation, activation is intentionally boring:

```text
use agentit
```

or naturally in another language:

```text
usa agentit
```

There are no magic powerwords beyond telling the active agent to use the protocol.

Useful mechanical commands:

```bash
# Inspect/enable bounded skill profiles for this project
agentit status --project .
agentit enable backend --project .
agentit enable backend --project . --apply

# Plan verification, then execute it
agentit verify "changed the login flow" --project . --signal auth
agentit verify "changed the login flow" --project . --signal auth --apply

# Continuity state
agentit continuity status --project .
agentit continuity init "ship account settings" --project .

# MCP state remains plan-first
agentit mcp status --project .
agentit mcp enable context7 --project .
agentit mcp enable context7 --project . --apply
```

`--apply` is intentionally explicit on commands that mutate managed state.

## Install

### Current prerequisites

- Git
- Python 3
- PyYAML
- Bash 4+
- **GNU/Linux for the current `install.sh` / `update.sh` implementation**

The shared skills and Python runtime are provider-neutral, but the current shell installer uses GNU-specific utilities. macOS is therefore **not yet a supported installer target**; do not assume the shell scripts are portable merely because the skill format is portable.

```bash
git clone https://github.com/marcmarti9/agentit.git ~/code/agentit
cd ~/code/agentit
python3 -m pip install --user PyYAML

# Preview first: no writes
bash install.sh --provider codex --with-guides

# Apply after reviewing the plan
bash install.sh --provider codex --with-guides --apply

# Put the CLI on PATH
mkdir -p ~/.local/bin
ln -sf ~/code/agentit/agentit ~/.local/bin/agentit
```

Providers currently handled by the installer are `claude`, `codex`, and `antigravity`; `all` installs the shared core into all supported targets. Provider-specific local credentials/configuration are intentionally not treated as portable project state.

> Want macOS support? The portability work should land before Agentit is marketed as cross-platform. Until then the limitation is explicit rather than hidden.

## The operating lifecycle

For substantial work the policy is:

1. **Inspect facts first.** Read the actual repo/docs/tool state before asking the user for discoverable information.
2. **Create `TASK_DECISION`.** Outcome, known facts, unknowns, risk, reversibility, skills/tools, topology, implementation plan, and verification strategy.
3. **Audit independently.** Cheap capable reviewer for ordinary work; stronger critic when risk or disagreement warrants it.
4. **Interview only unresolved product decisions.** Ask one consolidated, recommendation-led round instead of silently inventing product intent.
5. **Load the smallest useful skill/tool set.** Do not spray the catalog into context.
6. **Persist continuity for substantial work.** Sessions must be replaceable.
7. **Execute directly or delegate because there is a concrete benefit.** Specialization, isolation, parallel investigation, context separation, or independent judgment—not agent theatre.
8. **Use Loop/Graph contracts for executable work.** Bounded attempts, explicit verifiers, fail-closed escalation.
9. **Update durable docs with the implementation.** Architecture/operations/contracts/decisions must not lag behind code.
10. **Verify from fresh evidence.** No `done`, `fixed`, or `passing` claim from memory, a worker summary, or stale output.
11. **Ship through reviewable Git by default.** Branch → commits → PR → reviewer/user merge decision.

Canonical end-to-end playbook: [`skills/using-agentit/SKILL.md`](skills/using-agentit/SKILL.md).

## Profiles

The default profile is intentionally smaller than the full repository catalog.

| Profile | Intended use |
|---|---|
| `core` | orchestration, planning, debugging, review, testing, security, verification |
| `frontend` | UI engineering, browser/runtime checks, performance, simplification |
| `backend` | interfaces, observability, performance, simplification |
| `supabase` | backend + PostgreSQL/Supabase discipline |
| `product` | intent, specs, product/growth decisions |
| `writing` | technical docs and editing |
| `design` | deeper UI/UX research, art direction, motion/spatial craft |
| `release` | CI, migrations, launch readiness |
| `research` | source-driven/context-heavy investigation |
| `growth` / `agency` | productized growth/agency workflows |
| `all` | every repository skill; explicit use only |

Run the profile manager without a command to inspect resolved skill IDs:

```bash
python3 router/profiles.py --profile core
```

## Verification

`agentit verify` is signal-gated. Mechanical project facts are detected automatically; semantic facts chosen by the active AI are passed explicitly so Python never becomes a disguised natural-language router.

Examples:

```bash
agentit verify "changed auth middleware" --signal auth --signal api --project .
agentit verify "changed auth middleware" --signal auth --signal api --project . --apply
```

The current catalog includes project-native tests/build checks, secret scans, acceptance/red→green checks, and task-scoped checks for surfaces such as auth, HTTP, Postgres/Supabase, and browser/UI work.

See [`probes/catalog.yaml`](probes/catalog.yaml).

## Evaluation

Agentit intentionally separates **mechanical correctness** from **claims about model quality**.

Mechanical tests cover profile activation, manifests, path/symlink safety, capabilities, MCP state, continuity, worker context, Loop/Graph runtime, verification receipts, and architecture-policy invariants.

What the repository does **not** currently prove:

- that Agentit universally improves coding quality versus a raw frontier agent;
- that it reduces tokens, latency, or cost;
- that independent review is always worth its extra inference cost;
- that every provider follows every natural-language policy with equal reliability.

Those claims require agent-level comparative evals, not deterministic prompt classifiers. See [`evals/evaluation-plan.md`](evals/evaluation-plan.md) and [`evals/results.md`](evals/results.md).

## Testing

```bash
python3 -m unittest discover -s router -p "test_*.py"
python3 -m unittest discover -s tests
bash -n install.sh update.sh security/harden-local.sh
```

CI runs the mechanical suites and validates YAML/JSON/catalog integrity. Public claims should refer to the CI result for the exact commit being discussed, not an old local run.

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | portable global operating rules |
| `skills/using-agentit/` | end-to-end activation playbook |
| `skills/task-router/` | model-owned task decision + reviewer contracts |
| `skills/` | curated JIT knowledge modules |
| `agents/` | portable specialist roles |
| `router/` | mechanical profiles, capabilities, context, Loop/Graph, MCP and verification runtime |
| `profiles.yaml` | bounded profile composition |
| `probes/` | verification catalog + mechanical probes |
| `docs/` | canonical architecture/policy/runtime/continuity docs |
| `incubator/` | candidate/rejected capability research |
| `.codex/agents/` | bounded Codex worker profiles |
| `reports/` | dated research/history; not all reports describe the current architecture |

## Contributing

Contributions are welcome, especially when they remove a real failure mode without turning Agentit into a giant framework.

Before adding a skill, prefer this order:

```text
already covered? → strengthen the existing skill
upstream skill solves it better? → adapt with provenance/license
truly distinct repeated workflow? → incubate → evaluate → promote
one-off advice? → do not add a skill
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Third-party adaptations and inspirations are documented in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Documentation map

| Document | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | global agent playbook |
| [`docs/NO_PROGRAMMATIC_ROUTER.md`](docs/NO_PROGRAMMATIC_ROUTER.md) | AI judgment vs mechanical software boundary |
| [`docs/LLM_NATIVE_DECISION_PROTOCOL.md`](docs/LLM_NATIVE_DECISION_PROTOCOL.md) | primary decision + independent review |
| [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md) | interview/provider semantics |
| [`docs/PROJECT_CONTINUITY.md`](docs/PROJECT_CONTINUITY.md) | resumable state contract |
| [`docs/DOCUMENTATION_CONTRACT.md`](docs/DOCUMENTATION_CONTRACT.md) | durable system-documentation contract |
| [`docs/RUNTIME_ENGINEERING.md`](docs/RUNTIME_ENGINEERING.md) | Loop/Graph execution contracts |
| [`docs/CAPABILITIES.md`](docs/CAPABILITIES.md) | capability resolution / least privilege |
| [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md) | MCP catalog/runtime |
| [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md) | orchestration topologies / specialist contracts |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | upstream provenance and licenses |

## License

Agentit is licensed under the [Apache License, Version 2.0](LICENSE). Third-party material retains its applicable notices in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
