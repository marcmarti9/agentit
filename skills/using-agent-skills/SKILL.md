---
name: using-agent-skills
description: Discover Agentit skills through semantic packs, then let the primary AI choose any concrete subset that materially helps the current stage or worker.
---

# Using Agent Skills

Skills are **JIT knowledge**, not a context dump.

A pack is only a semantic map of an area. It helps the model discover what skills exist and what each one is useful for. It does **not** prescribe a level, order, minimum, maximum, or normal number of skills.

Canonical runtime pack map: `references/packs.md`.

## Pack-first discovery

For an Agentit task/stage:

```text
understand task
-> inspect the relevant pack(s)
-> read candidate descriptions
-> AI chooses any number of skills that materially help
-> load only those SKILL.md bodies
-> execute / verify
-> add or remove skills later if new evidence changes the need
```

The primary AI owns the selection. There are intentionally **no fixed skill counts and no pack levels**.

A task may legitimately use:

```text
selected_skills: []
```

or:

```text
selected_skills:
- debugging-and-error-recovery
```

or several skills from one or more packs when the work genuinely spans those concerns.

The deciding question is not “what level is this task?” but:

> **Which skill bodies would materially improve this specific stage, and are they worth their context cost?**

## Selection rules

1. **Use packs as discovery maps, not bundles.** Never inject a whole pack merely because its domain matches.
2. **No quotas.** Do not target 1, 3, 5, or any other predetermined number of skills.
3. **Load bodies, not IDs.** A skill is active only when the executing model reads its `SKILL.md` or receives equivalent provider-native injection.
4. **Cross-pack selection is allowed.** A task can pull from `frontend` + `design`, `backend` + `security` concerns inside engineering, `marketing` + `seo`, etc., when the actual problem warrants it.
5. **Do not preload cross-cutting skills.** Security, performance, references, MCP fit, orchestration, long-horizon recovery and advanced verification remain JIT.
6. **Project-local skills win.** Prefer compatible project-local instructions/skills over generic global guidance.
7. **Do not force an unrelated pack.** If Agentit lacks a tax/legal/database/etc. pack, use authoritative live sources and discover/adapt a real skill only if a durable procedure is missing.
8. **Selection can change during work.** Add a skill when a concrete gap appears; remove/stop carrying one when it no longer helps.

## References are also JIT

`reference-intelligence` is not globally loaded.

When `TASK_DECISION.reference_plan.mode != none`, load `reference-intelligence` and the smallest relevant curated/live source set. A web task may use design references; a current tax report should use current authoritative tax sources; a trivial repository rename may use none.

## Tools are also JIT

Do not load `mcp-tooling-fit` or enable MCPs merely because they exist. Select tools only when they materially improve the reviewed plan.

## Worker Context Contract

A spawned worker should receive only what it needs to succeed:

```text
role / objective
relevant pack(s) as discovery labels
selected skill bodies
selected references (if any)
project constraints/instructions
allowed tools/permissions
read/write scope
expected output/handoff
verification / stop condition
```

`pack` is explanatory metadata. `selected skill bodies` are the actual context payload.

The parent keeps the broader catalog and integration responsibility.

## Missing capability

If the current pack(s) do not expose an adequate skill:

1. inspect project-local skills/instructions;
2. inspect another genuinely relevant Agentit pack;
3. use `find-skills` / approved skill discovery when a reusable external skill could help;
4. use authoritative live sources for current domain knowledge;
5. adapt/create a new skill only if the procedure is durable and likely to recur.

Do not create a new skill for a one-off fact lookup.

## Anti-patterns

- fixed `essential/standard/deep` pack tiers;
- hardcoded minimum/maximum skill counts;
- loading every skill in the selected pack;
- spawning every worker with the same giant context;
- using a pack name as a substitute for reading selected skill bodies;
- adding skills “just in case” without a concrete reason;
- loading PostgreSQL guidance for a random database task;
- loading design references into a fiscal report;
- keeping a huge lifecycle recipe in context when one procedure would suffice.

## Completion check

Before execution/spawn, the parent should be able to answer:

```text
Why these pack(s)?
Why each selected skill?
Why is each selected skill worth its token cost now?
What useful context did we deliberately NOT load?
```

There is no correct skill count. The correct set is whatever the primary AI can justify from the actual task.