---
name: architect-orchestrator
description: Choose direct work or bounded delegation. Use for coupling, parallelism, orchestration, specialist agents, or independent review; not for focused single-agent changes.
---

# Adaptive Agent Architecture

## Core rule

Use one capable agent by default. Add agents only when context isolation, true parallelism, specialization, permissions, creative diversity, or independent verification provide a concrete benefit greater than coordination overhead.

The roles are capabilities, not a mandatory org chart:

- **Architect**: user-facing owner, task router, decision maker and final integrator.
- **Orchestrator**: coordinator for a real DAG of packages with separate ownership.
- **Supervisor**: temporary owner of one package; implements directly by default.
- **Worker**: minimal, local executor with a strict contract.
- **Specialist**: temporary domain expert selected from `agents/catalog.yaml`; mapped to implementer/reviewer/probe runtime roles.
- **Auditor**: independent, read-only risk review.

## Specialist catalog

Agentit maintains `agents/catalog.yaml` as the role-to-capability map. A catalog role is a reusable prompt/skill bundle, not a persistent process. When a specialist is useful:

1. select one role id whose triggers and domain match the task;
2. project only that role's listed skills and the minimum task context;
3. map its catalog `mode` to the Worker Context Contract runtime role;
4. require the catalog output contract;
5. return control to the Architect for acceptance/integration.

Do not create a specialist when loading the corresponding skill into the parent is cheaper and equally effective.

## Routing modes

1. **Direct** — focused or tightly coupled work.
2. **Plan + direct** — broad but sequential work; persist state between milestones.
3. **Probe** — isolated read-only investigation or fault localization.
4. **Specialist probe** — a bounded expert researches or designs one domain-specific package.
5. **Fan-out/fan-in** — 2-5 independent searches or implementation packages.
6. **Pipeline** — ordered packages connected by explicit artifacts.
7. **Writer + reviewers** — one writer owns changes; independent agents review.
8. **Design competition** — 2-3 independent creative concepts from a shared brief, then explicit jury/selection before implementation.
9. **Orchestrated DAG** — several packages with dependencies, integration and distinct ownership.
10. **Audit** — high-risk gate or arbitration between alternatives.

Do not use agent count, file count or perceived importance as routing criteria. Strong coupling favors one agent; separable uncertainty favors probes; independent work favors fan-out; concept uncertainty plus high creative value may justify design competition.

## Delegation test

Before spawning, score the candidate on:

- independence;
- coupling and shared mutable state;
- context isolation benefit;
- real parallel speedup;
- distinct tools, permissions or expertise;
- creative diversity benefit;
- risk reduction from independence;
- total coordination and integration cost.

If there is no specific advantage, stay single-agent.

## Design competition

Use only when the user asks for a genuinely ambitious redesign/brand experience or when choosing the creative concept is a major part of the task.

Workflow:

1. one researcher creates a shared evidence/reference brief;
2. 2-3 concept specialists receive the same brief but independent context;
3. each proposes a distinct visual thesis, narrative/interaction model, feasibility notes, performance risks, and mobile fallback;
4. a `design-critic` or parent creative director evaluates against explicit criteria: brand fit, originality, clarity, usability, technical feasibility, performance, and memorability;
5. choose one winner or a justified hybrid;
6. only then assign implementation.

Prefer model diversity or deliberately different constraints when useful. Do not majority-vote. Evaluate concepts by criteria.

## Minimal subagent contract

Every delegated spawn **must** go through the Worker Context Contract runtime (`router/worker_context.py`, `agentit worker build|render`). This is topology runtime, not a skill. Fresh context without project-instruction projection is fresh negligence.

Every delegated task declares an auditable `worker_context` with:

- exact objective, scope, and done condition;
- optional specialist role id from `agents/catalog.yaml`;
- projected project instructions (`AGENTS.md` / `CLAUDE.md` / … at root and work subdir);
- task-scoped active skills only (never the full catalog);
- safe applied preferences (no secrets);
- risk classification and constraints (no commits/pushes/external by default);
- allowed inputs and read/write ownership;
- artifact URIs when needed;
- expected artifact or output schema;
- verification command;
- stop condition and escalation boundary.

Precedence: `safety > explicit user instruction > project instruction > preferences > defaults`.

Never copy the full parent conversation or broad project documentation. Store large outputs as filesystem artifacts and return references plus a compact receipt.

## Concurrency and isolation

- Default subagents: zero.
- Normal specialist use: 1-2.
- Normal fan-out: 2-3; usual maximum: 5.
- Design competition: 2-3 concepts plus one integrator/judge; concept agents are read-only/proposal-only.
- Default depth: one child generation.
- One writer per file, contract or shared state.
- Parallel writers use isolated worktrees/branches.
- Sequence strongly coupled packages rather than forcing parallelism.
- The Architect is the only agent that communicates with the user.

## Verification by risk

- Low risk: focused checks by the implementer.
- Medium risk: relevant tests and Architect diff review.
- High risk: mandatory tests plus an independent Auditor. High risk includes auth, secrets, RLS, destructive migrations, money, central calculations, public contracts and irreversible data changes.
- Design-heavy work: rendered browser evidence plus independent visual critique when the user explicitly requests premium/high-ambition output.

Every delegated package returns: artifacts/files changed, tests run or skipped with reason, known risks, pending decisions and stop reason.

## Acceptance and correction

- Treat worker reports as claims, not evidence. Before acceptance, the Architect inspects the actual working tree and complete diff, confirms scope, and reruns the relevant verification.
- The Architect retains architecture, interfaces, decomposition, review, correction decisions, and final acceptance.
- If a worker is wrong, preferably return a corrected specification to the same worker and verify again; do not create a replacement worker merely to avoid a pending correction.
- Run independent tasks with non-overlapping files in parallel only when useful; serialize shared-file and dependent tasks.
- Workers must not create PRs, push, deploy, or run migrations without explicit authorization from the Architect or user.

## Model policy

Choose models by role, not prestige:

- strongest judgment/reasoning available: architecture, creative direction, arbitration, difficult reviews;
- strong general coding model: main implementation and complex refactors;
- fast/cheap capable model: bounded implementation, extraction, variants, browser iteration, repetitive QA;
- independent model family can be valuable for creative diversity or adversarial review.

Do not escalate by habit. A specialist's value can come from a better prompt/skill/context boundary even when using a cheaper model.

## Context and memory

Use project instructions as a routing index, not a knowledge dump. Load skills and documentation on demand. Persist plans and decisions in small artifacts for long tasks. Promote only stable, reusable lessons into memory or skills; do not store session narratives.

## Anti-patterns

- fixed Architect → Orchestrator → Supervisor → Worker pipelines;
- one agent per conventional job title;
- spawning the whole `agents/catalog.yaml` team for every task;
- agents reviewing their own work as independent validation;
- multiple writers touching the same files;
- passing huge parent prompts to children;
- unbounded correction loops;
- full test matrices on every exploratory task;
- debate or peer-to-peer chatter without information asymmetry;
- using expensive models for mechanical work;
- design competitions for routine UI maintenance.
