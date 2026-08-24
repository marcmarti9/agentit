# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**An open-source, provider-neutral reliability layer for AI coding agents.**

Agentit does not replace Codex, Claude Code, or another capable coding agent. It gives the agent a shared operating protocol for the parts that still go wrong in real repositories: understanding the actual task, challenging risky or materially weaker decisions, loading only relevant skills, delegating deliberately, preserving state, verifying with fresh evidence, keeping durable documentation aligned, and shipping through reviewable Git changes.

```text
You + your coding agent
          │
          ▼
      "use Agentit"
          │
          ▼
inspect real project state
          │
          ▼
primary task decision ──► challenge proposed method when warranted
          │
          ├──────────────► independent decision audit
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

## Human UX: no terminal ceremony

Agentit is designed to be **operated by the coding agent, not by the human through a CLI**.

For normal use, the human interface should be this simple:

```text
use Agentit
```

or naturally in another language:

```text
usa Agentit
```

On first use, if Agentit is not installed/discoverable yet, give the coding agent this repository and ask it to install and use Agentit. The **agent** owns cloning/checking the repo, inspecting the bootstrap plan, applying it when authorized, activating profiles, running verification, maintaining runtime receipts, configuring MCPs, and persisting continuity state.

The repository contains command-line interfaces because agents need deterministic mechanical surfaces. They are **agent-facing APIs and maintainer/debugging tools**, not a terminal workflow the human is expected to memorize.

There are no magic powerwords beyond telling the active agent to use the protocol.

## Why Agentit exists

Modern coding agents are already very capable. The remaining failure modes are often process failures rather than code-generation failures:

- the agent solves the wrong interpretation of the task;
- the agent rubber-stamps the user's first proposed method even when a materially better route exists;
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

### The agent should disagree when disagreement helps

Agentit is deliberately **not a yes-man protocol**.

If the user says “build X using A”, the agent separates the desired outcome (**X**) from the proposed method (**A**) unless A is an explicit hard requirement. When inspection shows that B is materially better on correctness, simplicity, maintainability, security, reversibility, performance, UX, cost, migration risk, or architecture fit, the agent should say so and recommend B.

The contract is:

```text
A is workable, but I recommend B because <material reason>.
A: <main upside> / <main downside>.
B: <main upside> / <main downside>.
My recommendation is B. If you still prefer A, I can implement A.
```

That is **constructive dissent, not insubordination**. The agent does not invent conflict for style, and a strong recommendation does not authorize destructive actions, hidden scope expansion, spend, deploys, or ignoring the user's informed final choice. Safety/authorization constraints remain hard boundaries.

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

The reviewer is not another decorative manager. It exists to catch a bad first decision while changing it is still cheap, including both uncritical agreement and pointless performative disagreement.

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

## First-run/bootstrap contract

The **human should not need to execute installer commands**. A compatible coding agent can bootstrap Agentit on the user's behalf after being given this repository.

The canonical bootstrap is now a **portable Python path for macOS and GNU/Linux**. It does not require Bash 4, GNU coreutils, Homebrew, `sha256sum`, `stat -c`, `mv -T`, or `mapfile`.

Internally, an agent can inspect a read-only plan and then apply it:

```text
python3 bootstrap.py --provider <claude|codex|antigravity|all>
python3 bootstrap.py --provider <...> --apply
```

Those commands are shown for transparency/maintainers; the user should normally just ask their coding agent to install Agentit.

The bootstrap creates:

- a self-contained runtime at `~/.agentit/runtime`;
- a private Python environment at `~/.agentit/venv` for runtime dependencies;
- bounded provider discovery surfaces containing the global `core` skills;
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

Providers currently represented by adapters/discovery are Claude Code, OpenAI Codex, and Antigravity/Open-Skills-style environments. Provider credentials and machine-local secrets are never portable project state.

## The operating lifecycle

For substantial work the policy is:

1. **Inspect facts first.** Read the actual repo/docs/tool state before asking the user for discoverable information.
2. **Create `TASK_DECISION`.** Outcome, known facts, unknowns, risk, reversibility, skills/tools, topology, implementation plan, and verification strategy.
3. **Challenge the proposed method when warranted.** Preserve user outcome/constraints; surface a materially better alternative instead of rubber-stamping.
4. **Audit independently.** Cheap capable reviewer for ordinary work; stronger critic when risk or disagreement warrants it.
5. **Interview only unresolved product decisions.** Ask one consolidated, recommendation-led round instead of silently inventing product intent.
6. **Load the smallest useful skill/tool set.** Do not spray the catalog into context.
7. **Persist continuity for substantial work.** Sessions must be replaceable.
8. **Execute directly or delegate because there is a concrete benefit.** Specialization, isolation, parallel investigation, context separation, or independent judgment—not agent theatre.
9. **Use Loop/Graph contracts for executable work.** Bounded attempts, explicit verifiers, fail-closed escalation.
10. **Update durable docs with the implementation.** Architecture/operations/contracts/decisions must not lag behind code.
11. **Verify from fresh evidence.** No `done`, `fixed`, or `passing` claim from memory, a worker summary, or stale output.
12. **Ship through reviewable Git by default.** Branch → commits → PR → reviewer/user merge decision.

Canonical end-to-end playbook: [`skills/using-agentit/SKILL.md`](skills/using-agentit/SKILL.md).

## Agent-facing mechanical interfaces

Humans should not have to drive these manually. They exist so the active agent can turn its semantic decision into deterministic, inspectable operations.

Examples of internal surfaces include:

- portable bootstrap and rollback;
- project profile activation (`status`, `enable`, `disable`);
- explicit-signal verification (`verify --signal ...`);
- continuity state/checkpoints;
- Loop/Graph runtime state and receipts;
- worker-context construction;
- MCP status/configuration;
- capability/inventory resolution.

The important boundary is that **the AI decides what the task means and which semantic signals apply; the CLI/runtime only executes explicit mechanical instructions**.

For example, a coding agent that has established an auth/API change may internally invoke verification with explicit `auth`/`api` signals. The human should only see the resulting plan/evidence when it is useful, not be asked to type the command.

## Profiles

The default profile is intentionally smaller than the full repository catalog.

| Profile | Intended use |
|---|---|
| `core` | orchestration, planning, debugging, review, testing, security, verification |
| `frontend` | UI engineering, browser/runtime checks, performance, simplification |
| `backend` | interfaces, observability, performance, simplification |
| `supabase` | backend + PostgreSQL/Supabase-specific guidance |
| `product` | intent, specs, product/growth decisions |
| `writing` | technical docs and editing |
| `design` | deeper UI/UX research, art direction, motion/spatial craft |
| `release` | CI, migrations, launch readiness |
| `research` | source-driven/context-heavy investigation |
| `growth` / `agency` | productized growth/agency workflows |
| `all` | every repository skill; explicit use only |

Profiles are inventories/discovery boundaries for the **agent**. They are not configuration choices the human should routinely manage.

## Verification

Agentit's verification runtime is signal-gated. Mechanical project facts are detected automatically; semantic facts chosen by the active AI are passed explicitly so Python never becomes a disguised natural-language router.

The current catalog includes project-native tests/build checks, secret scans, acceptance/red→green checks, and task-scoped checks for surfaces such as auth, HTTP, Postgres/Supabase, and browser/UI work.

See [`probes/catalog.yaml`](probes/catalog.yaml).

## Evaluation

Agentit intentionally separates **mechanical correctness** from **claims about model quality**.

Mechanical tests cover profile activation, manifests, path/symlink safety, capabilities, MCP state, continuity, worker context, Loop/Graph runtime, verification receipts, portable bootstrap/rollback, and architecture-policy invariants.

What the repository does **not** currently prove:

- that Agentit universally improves coding quality versus a raw frontier agent;
- that it reduces tokens, latency, or cost;
- that independent review is always worth its extra inference cost;
- that every provider follows every natural-language policy with equal reliability.

Those claims require agent-level comparative evals, not deterministic prompt classifiers. See [`evals/evaluation-plan.md`](evals/evaluation-plan.md) and [`evals/results.md`](evals/results.md).

## Maintainer testing

The repository has deterministic mechanical suites and CI. Maintainers and coding agents may invoke the underlying test commands directly; normal users should not need to.

CI validates runtime/utility suites, legacy shell syntax where applicable, registry YAML/JSON, profile/catalog integrity, architecture-policy invariants, and the **real portable bootstrap on both macOS and Ubuntu**. Public claims should refer to the CI result for the exact commit being discussed, not an old local run.

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | portable global operating rules |
| `bootstrap.py` / `router/bootstrap.py` | portable agent-facing install/rollback path |
| `bootstrap-manifest.json` | mechanical runtime/provider packaging manifest |
| `skills/using-agentit/` | end-to-end activation playbook |
| `skills/task-router/` | model-owned task decision + reviewer contracts |
| `skills/` | curated JIT knowledge modules |
| `agents/` | portable specialist roles |
| `router/` | mechanical profiles, capabilities, context, Loop/Graph, MCP and verification runtime |
| `profiles.yaml` | bounded profile composition |
| `probes/` | verification catalog + mechanical probes |
| `docs/` | canonical architecture/policy/runtime/continuity docs |
| `templates/` | explicit non-secret provider templates; machine-local `.local` files stay untracked |
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

See [`docs/SKILL_CURATION.md`](docs/SKILL_CURATION.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

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
| [`docs/SKILL_CURATION.md`](docs/SKILL_CURATION.md) | skill lifecycle, upstream provenance and promotion policy |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | upstream provenance and licenses |

## License

Agentit is licensed under the [Apache License, Version 2.0](LICENSE). Third-party material retains its applicable notices in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
