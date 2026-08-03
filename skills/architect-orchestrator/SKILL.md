---
name: architect-orchestrator
description: Choose direct work or bounded delegation. Use for coupling, parallelism, orchestration, or independent review; not for focused single-agent changes.
---

# Adaptive Agent Architecture

## Core rule

Use one capable agent by default. Add agents only when context isolation, true parallelism, specialization, permissions, or independent verification provide a concrete benefit greater than coordination overhead.

The roles are capabilities, not a mandatory org chart:

- **Architect**: user-facing owner, task router, decision maker and final integrator.
- **Orchestrator**: coordinator for a real DAG of packages with separate ownership.
- **Supervisor**: temporary owner of one package; implements directly by default.
- **Worker**: minimal, local executor with a strict contract.
- **Auditor**: independent, read-only risk review.

## Routing modes

1. **Direct** — focused or tightly coupled work.
2. **Plan + direct** — broad but sequential work; persist state between milestones.
3. **Probe** — isolated read-only investigation or fault localization.
4. **Fan-out/fan-in** — 2-5 independent searches or implementation packages.
5. **Pipeline** — ordered packages connected by explicit artifacts.
6. **Writer + reviewers** — one writer owns changes; independent agents review.
7. **Orchestrated DAG** — several packages with dependencies, integration and distinct ownership.
8. **Audit** — high-risk gate or arbitration between alternatives.

Do not use agent count, file count or perceived importance as routing criteria. Strong coupling favors one agent; separable uncertainty favors probes; independent work favors fan-out.

## Delegation test

Before spawning, score the candidate on:

- independence;
- coupling and shared mutable state;
- context isolation benefit;
- real parallel speedup;
- distinct tools, permissions or expertise;
- risk reduction from independence;
- total coordination and integration cost.

If there is no specific advantage, stay single-agent.

## Minimal subagent contract

Every delegated task declares:

- exact objective and done condition;
- allowed inputs;
- read/write ownership;
- relevant invariants only;
- expected artifact or output schema;
- verification command;
- stop condition and escalation boundary.

Never copy the full parent conversation or broad project documentation. Store large outputs as filesystem artifacts and return references plus a compact receipt.

## Concurrency and isolation

- Default subagents: zero.
- Normal fan-out: 2-3; usual maximum: 5.
- Default depth: one child generation.
- One writer per file, contract or shared state.
- Parallel writers use isolated worktrees/branches.
- Sequence strongly coupled packages rather than forcing parallelism.
- The Architect is the only agent that communicates with the user.

## Verification by risk

- Low risk: focused checks by the implementer.
- Medium risk: relevant tests and Architect diff review.
- High risk: mandatory tests plus an independent Auditor. High risk includes auth, secrets, RLS, destructive migrations, money, central calculations, public contracts and irreversible data changes.

Every delegated package returns: artifacts/files changed, tests run or skipped with reason, known risks, pending decisions and stop reason.

## Acceptance and correction

- Treat worker reports as claims, not evidence. Before acceptance, the Architect inspects the actual working tree and complete diff, confirms scope, and reruns the relevant verification.
- The Architect retains architecture, interfaces, decomposition, review, correction decisions, and final acceptance.
- If a worker is wrong, preferably return a corrected specification to the same worker and verify again; do not create a replacement worker merely to avoid a pending correction.
- Run independent tasks with non-overlapping files in parallel only when useful; serialize shared-file and dependent tasks.
- Workers must not create PRs, push, deploy, or run migrations without explicit authorization from the Architect or user.

## Model policy

- Prefer direct execution or Terra Medium for normal tasks.
- Use Luna Max for extensive, well-delimited reading, writing, or implementation.
- Use Sol Medium for coordination or architecture when it adds concrete value; reserve Sol High for exceptionally difficult or high-risk decisions.
- Reserve a second independent Sol review for RISK_4, critical security, destructive migrations, hard-to-reverse public contracts, or equivalent risk; it is not mandatory for routine features.
- Do not escalate by habit or delegate when coordination costs more than direct execution.

## Context and memory

Use project instructions as a routing index, not a knowledge dump. Load skills and documentation on demand. Persist plans and decisions in small artifacts for long tasks. Promote only stable, reusable lessons into memory or skills; do not store session narratives.

## Anti-patterns

- fixed Architect → Orchestrator → Supervisor → Worker pipelines;
- one agent per conventional job title;
- agents reviewing their own work as independent validation;
- multiple writers touching the same files;
- passing huge parent prompts to children;
- unbounded correction loops;
- full test matrices on every exploratory task;
- debate or peer-to-peer chatter without information asymmetry;
- using expensive models for mechanical work.
