---
name: using-agent-skills
description: Discover Agentit skills through semantic packs and depth levels, then load only the smallest concrete skill set needed by the current stage or worker.
---

# Using Agent Skills

Skills are **JIT knowledge**, not a context dump.

The goal is not to make every agent know every Agentit skill. The goal is to let the primary AI quickly discover the right domain family, choose an appropriate depth, and project only the few skill bodies that materially improve the current task.

Canonical runtime pack map: `references/packs.md`.

## Pack-first discovery

For an Agentit task/stage:

```text
understand task
-> choose primary pack
-> choose depth: essential | standard | deep
-> inspect candidate skills for that pack/depth
-> select smallest useful concrete subset
-> load those SKILL.md bodies
-> execute / verify
-> escalate depth or add one skill only when evidence shows a gap
```

A pack is a **search scope**, not a bundle injection.

Choosing:

```text
pack: design
depth: deep
```

does **not** mean load every design skill. It means advanced design skills are eligible candidates. A worker might still receive only:

```text
selected_skills:
- design-inspiration-research
- scrollytelling-web
- browser-testing-with-devtools
```

## Depth levels

### `essential`

Minimum useful domain process for bounded work. Prefer this first when the task is straightforward.

### `standard`

Normal production depth. Use when common implementation/review concerns matter.

### `deep`

Specialist/high-risk/high-craft/niche candidate pool. Use only when the task actually requires advanced expertise or the current pass proves insufficient.

Depth may increase during work. Do not start at `deep` for ceremony.

## Selection rules

1. **One primary pack per stage when possible.** Add a secondary pack only when the stage genuinely crosses a domain boundary.
2. **Load bodies, not IDs.** A skill is active only when the executing model reads its `SKILL.md` or receives equivalent provider-native injection.
3. **Never project a whole pack to a worker.** Project only selected skill bodies plus bounded task/project context.
4. **Do not preload cross-cutting skills.** Security, performance, references, MCP fit, orchestration, long-horizon recovery and deep verification are JIT when their conditions actually apply.
5. **Project-local skills win.** Prefer the project's own compatible instructions/skills over generic global guidance.
6. **Do not force a pack onto an unrelated domain.** If Agentit lacks a tax/legal/database/etc. pack, use authoritative live sources and discover/adapt a real skill if the procedure is durable.
7. **Escalate by evidence.** Add depth/skills because a concrete gap appeared, not because more context feels safer.

## References are also JIT

`reference-intelligence` is not globally loaded.

When `TASK_DECISION.reference_plan.mode != none`, load `reference-intelligence` and the smallest relevant curated/live source set. A web task may use design references; a current tax report should use current authoritative tax sources; a trivial repository rename may use none.

## Tools are also JIT

Do not load `mcp-tooling-fit` or enable MCPs merely because they exist. Select tools after the semantic task/pack decision and only when they materially improve execution.

## Worker Context Contract

A spawned worker should receive only what it needs to succeed:

```text
role / objective
pack
depth
selected_skills
selected references (if any)
project constraints/instructions
allowed tools/permissions
read/write scope
expected output/handoff
verification / stop condition
```

The parent keeps the broader catalog and integration responsibility.

## Missing capability

If the current pack does not contain an adequate skill:

1. inspect project-local skills/instructions;
2. inspect another genuinely relevant Agentit pack;
3. use `find-skills` / approved skill discovery when a reusable external skill could help;
4. use authoritative live sources for current domain knowledge;
5. adapt/create a new skill only if the procedure is durable and likely to recur.

Do not create a new skill for a one-off fact lookup.

## Anti-patterns

- all skills globally installed as if they must all be read;
- loading every skill in the selected pack;
- spawning every worker with the same giant context;
- choosing `deep` by default;
- using a pack name as a substitute for reading the selected skill bodies;
- loading PostgreSQL guidance for a random database task;
- loading design references into a fiscal report;
- loading security/performance/orchestration skills when there is no corresponding problem;
- keeping a huge lifecycle recipe in context when the current stage needs only one procedure.

## Completion check

Before execution/spawn, the parent should be able to answer:

```text
Why this pack?
Why this depth?
Why each selected skill?
What useful context did we deliberately NOT load?
```

If the answer to the last question is “nothing, we loaded everything”, skill selection probably failed.
