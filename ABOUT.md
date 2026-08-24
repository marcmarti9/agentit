# About Agentit

Agentit is an **open-source, provider-neutral reliability layer for AI coding agents**.

It is not another coding model and it is not a framework that tries to replace the native capabilities of Codex, Claude Code, or other capable agents. Agentit supplies a shared operating protocol around them: model-owned task decisions, independent review, just-in-time skills and tools, bounded delegation, resumable project state, mechanical execution receipts, fresh verification, durable documentation, and reviewable Git handoffs.

The [README](README.md) is the canonical public introduction and installation guide. This document explains the design identity behind it.

## Design identity

### AI judgment stays with the AI

Agentit deliberately does **not** use regexes, keyword scores, or a Python classifier to infer natural-language intent, risk, topology, or the right skill from a prompt.

The active primary model sees the actual conversation and project context and produces `TASK_DECISION`. A separate model reviews material decisions. Deterministic software then enforces the parts that are genuinely mechanical: manifests, capability resolution, runtime state, receipts, verification probes, continuity artifacts, and safe configuration changes.

### Orchestration must earn its cost

Agentit has no fixed "Architect → Manager → Supervisor → Worker" pyramid.

Delegation is useful when it creates a concrete advantage such as:

- specialist expertise;
- independent criticism;
- parallel read-only investigation;
- context isolation for large source sets;
- independent design alternatives;
- bounded implementation ownership.

Tightly coupled work can remain direct. Multi-node work gets an explicit Graph Contract rather than an invisible hierarchy.

### Skills are curated, not sprayed into context

Agentit uses small, task-scoped skills and bounded profiles. A skill is not considered used because its ID appears in a catalog; the executing model must actually receive its body.

The repository can learn from strong upstream projects, but external skills are not bulk-imported simply because they are popular. The preferred order is:

```text
strengthen existing capability
        ↓
adapt a better upstream idea with provenance
        ↓
incubate a genuinely distinct repeated workflow
        ↓
evaluate
        ↓
promote only if it earns permanent context/maintenance cost
```

See [`docs/SKILL_CURATION.md`](docs/SKILL_CURATION.md) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Core layers

```text
┌──────────────────────────────────────────────────────────────┐
│  Semantic policy                                            │
│  TASK_DECISION → independent audit → escalation when needed │
└─────────────────────────────┬────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────┐
│  JIT capability layer                                       │
│  skills → profiles → specialists → MCP/tool capabilities    │
└─────────────────────────────┬────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────┐
│  Mechanical execution layer                                 │
│  Loop contracts → Graph contracts → receipts                │
└─────────────────────────────┬────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────┐
│  Project reliability layer                                  │
│  continuity → verification → durable docs → Git review      │
└──────────────────────────────────────────────────────────────┘
```

### 1. Semantic policy

The primary model owns task interpretation. An independent reviewer challenges the decision before material execution, with stronger review for high-consequence changes.

### 2. JIT capabilities

Profiles expose a bounded discovery set. The active agent selects the smallest useful skill/tool set, and workers receive only task-scoped project instructions, capabilities, and skill bodies.

### 3. Mechanical execution

Executable work uses Loop Contracts with observable goals, verifiers, stop conditions, bounded attempts, and escalation boundaries. Multi-node work uses Graph Contracts with explicit dependencies and write ownership.

### 4. Project reliability

Substantial work can resume from repository state instead of a chat transcript. Completion claims require fresh evidence, and durable architecture/operations documentation must remain aligned with implementation.

## Safety posture

Agentit's management operations are designed to be explicit and reversible, but the exact mutation contract depends on the command:

- `install.sh`, `update.sh`, and `security/harden-local.sh` are **plan-first** and require `--apply` for their managed filesystem changes;
- profile and MCP enable/disable operations are **plan-first** and require `--apply` to apply managed configuration;
- continuity commands such as `continuity init` and `continuity checkpoint` are explicit state-writing commands by design;
- verification is plan-first, while `verify --apply` executes probes and writes a receipt;
- provider credentials and machine secrets must never be committed to the repository.

Filesystem-management code rejects unsafe symlink/path states where applicable and uses hashes/manifests for managed reversible writes.

## Provider neutrality

The protocol and shared skills are intended to remain provider-neutral. Provider adapters are deliberately thin and may have different feature maturity.

The current shell installer has explicit targets for Claude Code, OpenAI Codex, and Antigravity-style skill discovery. The **current installer scripts are GNU/Linux-oriented**; that is a packaging/platform limitation, not a claim that the underlying skill/protocol format is Linux-only.

## Evidence posture

Agentit is early-stage. Mechanical contracts can be tested deterministically; claims that it universally improves code quality, token use, latency, or cost cannot.

Public claims therefore distinguish:

- **implemented/tested contract** — backed by code/tests/CI for the exact revision;
- **design hypothesis** — a reason Agentit may improve agent reliability;
- **comparative claim** — requires controlled agent-level baseline experiments.

See [`evals/evaluation-plan.md`](evals/evaluation-plan.md).

## Open source

Agentit is licensed under the [Apache License, Version 2.0](LICENSE).

- [README](README.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)
