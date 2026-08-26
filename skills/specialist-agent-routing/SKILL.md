---
name: specialist-agent-routing
description: Select and use temporary domain specialists with bounded JIT context and concrete task-scoped skills.
---

# Specialist Agent Routing

Specialists are temporary capabilities, not a permanent org chart. Spawn one only when specialization, independent judgment, context isolation, or real parallelism materially improves the reviewed plan.

## Discovery

Use `agents/catalog.yaml` as a model-readable specialist catalog and `skills/using-agent-skills/references/packs.md` as the semantic skill map. Catalog triggers are discovery hints for the model, never executable keyword-routing rules.

Profiles determine what can be installed/discovered. Packs expose possible expertise. **Workers receive selected skill bodies and selected references, never whole profiles or packs.**

## Worker contract

For every delegated worker define:

```text
role / objective
scope
relevant_packs (discovery labels only)
selected_skills
selected_references
allowed tools / permissions
read/write ownership
expected output / handoff
risk / safety
verification
stop / escalation
```

The parent decides how much work the task deserves through the semantic `TASK_DECISION` — including complexity, plan, topology, review, and verification. There is no pack-depth vocabulary, fixed skill count, or required worker count.

## Spawn when it earns its cost

Good reasons include:

- distinct expertise;
- fresh independent proposal or review;
- a large research/source set that should stay isolated from parent context;
- truly independent work packages that can run in parallel;
- different tools/capabilities that a bounded specialist can use more effectively.

Avoid job-title theater, duplicate writers, identical contexts, or delegation that creates more integration work than it removes.

## Parent responsibilities

The parent keeps decomposition, semantic decisions, ownership, integration, user communication, and final verification. If a worker discovers a material scope/risk change or missing capability, it reports the gap rather than silently expanding context or permissions.

If the host cannot spawn the preferred specialist, ordinary delegation may fall back to a host-native worker or the parent with the same bounded skill set. When genuine independence is required for safety/review, degrade visibly and escalate instead of pretending same-context review is independent.

## Multiple concepts

Independent concept workers can be useful for ambitious design or architecture when real alternatives would improve judgment. The model decides whether that exploration is worth the cost; there is no named quality tier that automatically triggers it.

Worker claims are never sufficient evidence by themselves. Completion still follows Agentit's verification and Loop/Graph contracts.
