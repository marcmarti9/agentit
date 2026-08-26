---
name: specialist-agent-routing
description: Select and spawn domain specialists with bounded pack/depth context and only the concrete skills they need. Intelligent spawn, no hard caps, critic for large plans.
---

# Specialist Agent Routing

Specialists are temporary domain experts, not a permanent org chart. Spawn when isolation, specialization, independent judgment, breadth, latency or parallelism materially improves the result.

## Source of truth

Read `agents/catalog.yaml` for specialist roles and `skills/using-agent-skills/references/packs.md` for runtime pack/depth discovery.

Profiles/installations determine what can be discovered. Packs determine the semantic candidate scope. **Workers receive selected skills, never whole profiles/packs.**

## Spawn decision

Create a specialist when at least one is true:

- distinct expertise vs current parent context;
- independent proposal or review, including critic;
- research branch without shared mutable state;
- different tools/model efficiency;
- context isolation for large research/design/diagnostics;
- genuinely parallel independent work packages.

Do not spawn for job-title theater. A single capable primary with one relevant skill is better than five workers sharing the same context.

## Specialist contract

For each worker define:

```text
role / objective
scope
pack
pack_depth: essential | standard | deep
selected_skills
selected references if any
allowed tools / permissions
read/write ownership
expected output / handoff
risk / safety
verification
stop / escalation
```

The selected skill bodies are projected through the Worker Context Contract. `pack` and `pack_depth` explain why those skills were chosen; they are not instructions to load the rest of the pack.

### Good

```text
role: landing interaction implementer
pack: design
pack_depth: deep
selected_skills:
- scrollytelling-web
- gsap-performance
- browser-testing-with-devtools
```

### Bad

```text
pack: design
skills: <every design skill in Agentit>
```

## Context budget

The worker should receive the smallest self-sufficient context that lets it complete its bounded objective:

- exact objective/acceptance criteria;
- project instructions/constraints that apply;
- necessary files/artifacts/context;
- selected skill bodies;
- selected references only when relevant;
- tool permissions;
- verifier/stop condition.

The parent keeps unrelated conversation, other packs, global catalogs and integration context.

If the worker discovers a missing capability, it should report the concrete gap and request/escalate rather than silently loading a giant additional pack.

## No hard caps

There is no mandatory min/max specialist count. Stop spawning when ownership, context projection or integration cost exceeds the benefit.

## Critic specialists

For large structural plans, high-impact architecture or ambitious visual work, use a fresh read-only critic before commitment when it materially improves judgment. High-risk review requirements from `task-router` still apply.

## Parent responsibilities

The parent/architect owns:

- decomposition;
- pack/depth and selected-skill choice;
- acceptance criteria;
- dependency/write ownership;
- conflict resolution;
- integration;
- final verification;
- user-facing answer.

Worker claims are not evidence by themselves.

## Missing skills

If the chosen pack lacks a real fit:

1. inspect project-local skills/instructions;
2. inspect another genuinely relevant pack;
3. use `find-skills` / approved skill discovery;
4. use authoritative live sources when current domain knowledge is the real gap;
5. adapt/create a durable skill only when recurrence justifies it.

Do not force an unrelated pack onto the worker.

## Design competition

For Studio-level visual work, 2–3 independent concepts can be useful before a jury selects one direction. Each concept worker should still receive a bounded design pack subset, not the whole design catalog.

## Anti-patterns

- one subagent per job title;
- hard quotas for show;
- multiple writers on the same files/shared state;
- dumping the full skill catalog or whole pack into workers;
- giving every worker the same context;
- starting every worker at `deep`;
- spawning when a single selected skill in the parent would suffice;
- skipping required independent review on high-risk/structural work.
