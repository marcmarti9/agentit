# Reference Intelligence architecture

Agentit should make an agent **better at using external knowledge**, not wrap the agent in a second knowledge engine implemented in Python.

The core rule is:

> **The model decides what knowledge it needs; Agentit supplies curated knowledge where useful, live research where needed, and existing runtime/verification primitives for execution.**

## Startup context stays tiny

Reference Intelligence is **not globally loaded**.

A fresh Agentit installation exposes only the minimal navigation core:

- `using-agentit`;
- `task-router`;
- `using-agent-skills`.

The first prompt is semantically dispatched as `bare | agentit`. Material work prefers Agentit; trivial work may stay bare. Once Agentit is selected, the model chooses a domain pack/depth and concrete skills JIT.

If `reference_plan.mode != none`, `reference-intelligence` is then loaded as one of those concrete JIT skills.

This keeps reference discipline available without paying its context cost on every prompt.

## Why this exists

Without an explicit reference discipline, agents tend to fail in opposite directions:

- ignore useful references unless the user re-pastes them;
- load too many references into every task;
- stop at a social post instead of reading the underlying article/repository;
- treat creator/vendor claims as facts;
- accumulate giant prompt libraries without converting them into reusable capability;
- copy designs instead of extracting principles;
- use stale memory for laws, APIs, prices, standards or current platform behavior;
- forget where a durable project decision came from.

Reference Intelligence addresses those failures primarily through **agent instructions and domain skills**, not bespoke routing code.

## Architecture

```text
user task + project context
        ↓
first-prompt dispatch
   bare | agentit
        ↓ agentit
primary AI TASK_DECISION
        ↓
pack + depth + selected skills
        ↓
references needed?
  none | curated | live | both
        ↓ if needed
load reference-intelligence JIT
        ↓
read only the useful material
        ↓
extract evidence / principles / procedure
        ↓
apply through the relevant domain skill
        ↓
execute with normal Agentit Loop/Graph contracts
        ↓
verify actual outcome
        ↓
record durable provenance when it matters
```

The cheap independent auditor challenges obviously weak task/reference decisions. It does not become the semantic router.

## Relationship to skill packs

Runtime packs are defined in `skills/using-agent-skills/references/packs.md`.

Packs are semantic discovery scopes, not bundles injected into context. Each task/stage chooses:

```text
pack: <domain>
depth: essential | standard | deep
selected_skills:
- <small concrete subset>
```

Reference Intelligence is a cross-cutting candidate that becomes relevant when external/current knowledge or provenance matters. For example:

- `design:standard/deep` may load design references;
- `seo:standard` may combine curated SEO procedure + live search/platform evidence;
- `research:standard/deep` may load source/provenance discipline;
- a current fiscal report with no pre-curated Agentit pack can still use authoritative live fiscal sources.

Choosing a deep pack does not imply loading Reference Intelligence—or any other skill—unless the task earns it.

## Curated knowledge structure

Agentit keeps a small human/agent-readable discovery index:

- `references/INDEX.md`

Deep recurring knowledge belongs **next to the skill that uses it**, for example:

- `skills/design-inspiration-research/references/premium-web-production.md`
- `skills/marketing-and-growth/references/marketing-operating-system.md`
- `skills/marketing-and-growth/references/seo-growth-loop.md`
- `skills/marketing-and-growth/references/launch-content-system.md`

This is intentional progressive disclosure:

```text
minimal Agentit dispatcher
-> pack/depth
-> selected skill
-> relevant deep reference
-> live source only when needed
```

The global index should not become a 10,000-link database.

## Why no reference router / CLI

The active model understands the task better than a keyword classifier or a custom Python scoring layer.

Agentit therefore does **not** need a bespoke runtime that tries to infer:

- this is fiscal, therefore load pack X;
- this is frontend, therefore load links Y/Z;
- this prompt contains “SEO”, therefore inject every marketing reference.

The primary AI already makes that semantic choice inside `TASK_DECISION`.

Software remains useful for mechanical work Agentit already owns: bootstrap, state, commands, Loop/Graph execution, receipts, tool configuration and other deterministic operations.

## Reference modes

### `none`

External knowledge would not materially change the result.

Examples: local rename, formatting, self-contained repository bug.

### `curated`

Agentit already contains a useful playbook/reference for a recurring problem.

Example: a Studio website can load the premium-web production reference.

### `live`

The task needs current/domain authority not pre-curated in Agentit.

Example: a Spanish fiscal report should use current legislation/tax-authority sources. Agentit does not need a permanent fiscal pack to be capable of this.

### `both`

A curated procedure helps structure the work, while current sources establish facts.

Example: SEO uses a curated audit/feedback procedure plus current site/GSC/search evidence.

## Read the underlying asset

For bookmarks, the social post is often only the pointer. If it links to a richer article, repository, course, prompt collection, component library or documentation site, the agent should inspect the useful underlying material before deciding what to preserve.

Promotion path:

```text
bookmark
-> underlying asset
-> durable insight?
   no  -> keep out of core
   yes -> already covered by a skill?
          yes -> enrich that skill / references/*.md
          no  -> add the smallest new capability that is actually missing
```

This is how the bookmark batch should evolve over time.

## Prompt libraries

Large prompt collections are treated as **source datasets**, not Agentit's runtime interface.

The useful transformation is:

```text
many prompts
-> repeated jobs/capabilities
-> inputs
-> intermediate decisions/artifacts
-> outputs
-> evidence/QA
-> reusable procedure
```

For example, the bookmarked 500-marketing-prompt corpus is distilled into customer research, positioning, content, copy, SEO, email, campaign and analytics procedures inside the marketing skill instead of being copied verbatim.

## Design references

Design references are decomposed into dimensions such as:

- structure and rhythm;
- hierarchy/composition;
- typography;
- color/material;
- imagery/artifacts;
- component archetypes;
- interaction/motion;
- responsive behavior.

Then they are recombined around the target project's own content/brand/constraints.

A reference can inspire a layout without proving conversion. Price/revenue claims attached to “premium website” posts remain creator claims.

## Source roles

Keep the distinction between:

- canonical/current authority;
- licensed reusable artifact;
- corroborated evidence;
- creator/vendor claim;
- inspiration;
- internal project/client evidence.

Authority is contextual. Official API documentation can establish API behavior but not whether using that API is a good product decision.

## Project provenance

If an external source materially changes an expensive-to-rediscover decision, reuse the project's canonical decision/reference docs or default to:

`docs/agentit/REFERENCES.md`

Record only what matters:

```text
source
-> role
-> principle/evidence actually used
-> project decision
-> affected area
-> date / recheck trigger when relevant
```

Do not store browser history, transcripts or private reasoning.

## Verification

References are inputs, not proof that the result works.

If reference use is material to acceptance, the primary AI includes it in the **existing Loop/Graph verifier** alongside the real outcome checks.

No second reference-specific Python verification system is necessary.

## What belongs in Agentit

Promote a reference when it gives Agentit something durable:

- a recurring procedure;
- a strong reusable reference library;
- an external artifact worth evaluating;
- a domain workflow that improves an existing skill;
- a repeated source of truth.

Do not promote something globally just because it is interesting. Experimental local-inference projects, salary anecdotes and one-off hype can be researched live when a future task actually concerns them.

## Design principle for future Agentit work

When deciding between adding agent guidance and adding framework code, prefer this order:

1. Can the capable model reason about this directly?
2. Can a skill/reference teach it the missing durable knowledge?
3. Can the existing Agentit runtime enforce the resulting acceptance contract?
4. Only then add new deterministic code if there is a genuinely mechanical invariant the model should not own.

In short:

> **Use code to make execution reliable; use the model to make semantic decisions; spend context only on knowledge the current task has earned.**
