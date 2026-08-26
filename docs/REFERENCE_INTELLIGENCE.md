# Reference Intelligence architecture

Agentit makes capable agents better at using external knowledge without adding a second semantic router.

> **The model decides what knowledge it needs; Agentit supplies curated knowledge where useful, live research where needed, and existing execution/verification primitives for the outcome.**

## JIT by default

A fresh Agentit installation exposes only the tiny navigation core:

- `using-agentit`
- `task-router`
- `using-agent-skills`

The first meaningful task is semantically dispatched as `bare | agentit`. Once Agentit is selected, the primary AI chooses relevant pack(s) and concrete skills JIT. Packs are flat discovery maps: they have no depth levels, fixed ordering, or prescribed skill count.

For every material `TASK_DECISION`, choose:

```text
reference_plan.mode: none | curated | live | both
```

If the mode is not `none`, load `reference-intelligence` JIT. Do not preload it globally.

## Flow

```text
user task + project context
        ↓
bare | agentit
        ↓ agentit
primary AI TASK_DECISION
        ↓
relevant pack(s) + selected skills
        ↓
references needed?
none | curated | live | both
        ↓ if needed
reference-intelligence JIT
        ↓
read only useful sources
        ↓
extract evidence / principles / procedure
        ↓
apply through selected domain skills
        ↓
Loop / Graph execution
        ↓
fresh verification
```

How much research and evidence a task deserves follows the semantic complexity, risk, plan, and desired outcome in `TASK_DECISION`; it is not determined by a named pack-depth tier.

## Reference modes

### `none`
External/current knowledge would not materially improve the result, such as a self-contained local rename or obvious repository-only fix.

### `curated`
A recurring Agentit/project reference already contains useful procedure or principles.

### `live`
The task depends on current or domain-authoritative facts: laws, tax rules, APIs, prices, standards, platform behavior, recent research, or other freshness-sensitive information.

### `both`
Curated procedure structures the work while live/current sources establish facts.

## Curated knowledge structure

Use `references/INDEX.md` as a small discovery index. Deep recurring knowledge belongs next to the skill that consumes it, for example:

- `skills/design-inspiration-research/references/premium-web-production.md`
- `skills/marketing-and-growth/references/marketing-operating-system.md`
- `skills/marketing-and-growth/references/seo-growth-loop.md`
- `skills/marketing-and-growth/references/launch-content-system.md`

Progressive disclosure is:

```text
tiny Agentit core
-> relevant pack(s)
-> selected skill
-> specific curated reference
-> live source when needed
```

Do not turn the global index into a giant prompt/link database.

## Underlying sources and provenance

A social post or bookmark is often only a pointer. When it links to a richer article, repository, paper, documentation set, course, or component library, inspect the useful underlying source before deciding what is durable.

Keep source roles distinct:

- canonical/current authority
- licensed reusable artifact
- corroborated evidence
- creator/vendor claim
- inspiration
- internal project/client evidence

Authority is contextual. Official API docs can establish API behavior, but not whether that API is a good product choice.

## Prompt libraries

Treat large prompt collections as source datasets, not Agentit's runtime interface. Distill repeated jobs, inputs, decisions, outputs, and QA into reusable skills/procedures instead of injecting hundreds of prompts.

## Design references

Extract reusable principles — structure, hierarchy, typography, color/material, imagery, component archetypes, motion, responsive behavior — and recombine them around the target project's content and constraints. Inspiration is not proof of conversion or quality claims.

## Project provenance

Task-local research/provenance can stay private under `.agentit/` when it is only needed to continue the current work. Promote a source into tracked project documentation only when it materially supports a durable public/team decision whose provenance is worth preserving.

Never store browser history, raw chats, private reasoning, credentials, or personal planning in tracked project docs.

## Verification

References are inputs, not proof the result works. If reference use matters to acceptance, include it in the normal Loop/Graph verification together with real outcome checks. No second reference-specific verification engine is needed.

## Design principle

When choosing between more framework code and better agent guidance:

1. Can the capable model reason about it directly?
2. Can a skill/reference supply durable missing knowledge?
3. Can existing Agentit runtime enforce the acceptance contract?
4. Only then add deterministic code for a genuinely mechanical invariant.

> **Use code to make execution reliable; use the model to make semantic decisions; spend context only on knowledge the current task earns.**
