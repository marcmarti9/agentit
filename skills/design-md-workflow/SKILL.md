---
name: design-md-workflow
description: Read, create, maintain and verify a project's durable DESIGN.md visual-identity contract when persistent design tokens and rationale would materially improve multi-session frontend/design consistency.
license: Apache-2.0-compatible original Agentit guidance
source: https://github.com/google-labs-code/design.md
---

# DESIGN.md Workflow

Use this skill when a project needs a durable, agent-readable visual identity that survives across sessions, agents and implementation passes.

Google Labs' `DESIGN.md` project defines an alpha format that combines machine-readable design tokens in YAML front matter with human-readable design rationale in Markdown. Agentit treats that format as an **optional current external contract**, not a global dependency and not a replacement for the project's real source-of-truth design system.

## When to load

Load when one or more are true:

- a project already contains `DESIGN.md`;
- a greenfield/redesign task needs a durable visual identity for future agents;
- Figma/design tokens exist but the coding-agent handoff lacks concise project-level rationale;
- several sessions/agents keep drifting in typography, color, spacing, radii or component styling;
- a design-system change needs a reviewable token/rationale diff.

Do **not** load for a one-off tiny UI edit where the existing component system already answers the visual question.

## Authority order

Before writing or applying `DESIGN.md`, identify the real source of truth.

Typical authority order:

```text
explicit user/brand requirements
-> existing production design system / tokens / Figma source
-> canonical DESIGN.md when intentionally maintained
-> project components/styles
-> external design references
-> model preference
```

If `DESIGN.md` conflicts with production tokens or an explicitly authoritative Figma/design-system source, do not silently choose one. Determine whether `DESIGN.md` is stale and update the correct canonical source.

`DESIGN.md` is memory, not magic. It cannot make an inaccurate design system authoritative merely because it is structured.

## Cold-session behavior

`DESIGN.md` may persist on disk because it is durable project knowledge. The **skill body remains JIT**.

A fresh session should inspect `DESIGN.md` only when visual/system consistency is material to the current task. Do not globally inject it into unrelated backend, research or writing work.

## Read workflow

When `DESIGN.md` exists:

1. Read its front matter and prose before choosing visual direction.
2. Locate actual implementation tokens/components and compare material values.
3. Treat token values as normative only to the extent the project intentionally uses `DESIGN.md` as a maintained contract.
4. Extract the project's visual thesis, semantic color roles, type hierarchy, spacing/radius rules, component rules, and explicit do/don't guidance.
5. Feed only the relevant subset to the executing design/frontend worker.

Do not dump the whole document into every worker when only one component family is changing.

## Create workflow

Create `DESIGN.md` only when persistent design memory is useful enough to maintain.

Build it from project truth, not imagination:

```text
inspect brand + current UI + tokens + components + Figma if authoritative
-> identify stable visual decisions
-> normalize semantic token roles
-> write concise rationale explaining why/how they are used
-> map important component states
-> document deliberate omissions
-> validate
-> compare implementation against the contract
```

Do not fabricate a “brand system” from generic AI preferences when the project lacks enough evidence. For greenfield work, first establish a reviewed design direction using the design pack; then encode the accepted direction.

## Current DESIGN.md structure

As of the inspected Google Labs alpha specification, the format supports YAML front matter for concepts including:

- `name` / optional version and description;
- semantic `colors`;
- `typography` roles;
- `rounded` scale;
- `spacing` scale;
- component-level token mappings;
- intentional omissions;

with Markdown rationale sections such as overview, colors, typography, layout/spacing, elevation/depth, shapes, components, and do/don't guidance.

The external format is explicitly **alpha**. Re-check the current upstream specification before depending on exact schema details, CLI flags or lint semantics in a material change.

## Token rules

Prefer semantic roles over component accidents.

Good:

```text
colors.action-primary
colors.text-muted
spacing.content-gap
rounded.control
```

Weak:

```text
blue-500
random-gray
card-padding-17
```

unless those names are already the canonical project convention.

A token should earn persistence because it encodes a repeated design decision. Do not serialize every CSS declaration into `DESIGN.md`.

## Rationale rules

The Markdown body explains decisions a raw token file cannot:

- visual thesis and brand character;
- where an accent is and is not used;
- density/whitespace intent;
- typography roles and hierarchy;
- responsive composition principles;
- material/elevation rules;
- recurring component behavior;
- anti-patterns that would make the product drift off-brand.

Write actionable constraints, not aesthetic fan fiction.

Weak:

> The interface evokes an elevated digital journey through a sophisticated technological landscape.

Useful:

> Use warm off-white surfaces and near-black text. Red is reserved for primary actions and critical status. Product pages stay content-dense; marketing pages may use larger editorial spacing.

## Component states

When the design contract covers interactive components, capture only real semantic states:

```text
default
hover (pointer surfaces)
focus-visible
pressed/active
disabled
loading
error/success when the component actually owns those states
```

Do not invent meaningless variants to make the design file look complete.

## Verification

When the current upstream CLI is available and dependency use is acceptable, prefer its validator instead of hand-waving schema validity. The inspected alpha project exposes commands equivalent to:

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md diff DESIGN-before.md DESIGN.md
```

It can also export tokens to Tailwind-oriented or DTCG formats. Re-verify current command syntax from the upstream source because the format is alpha.

Lint success alone is not visual verification. Also verify:

- referenced fonts/assets actually exist or have an approved delivery path;
- component tokens map to real project implementation;
- contrast/accessibility on actual states;
- rendered desktop/mobile behavior;
- production tokens and `DESIGN.md` have not drifted materially.

## Change discipline

When visual identity changes materially:

1. update the actual implementation/source of truth;
2. update `DESIGN.md` in the same reviewable change when it is canonical project memory;
3. explain the durable reason in project docs/ADR only if rediscovery would be costly;
4. verify the new design contract and rendered UI;
5. do not leave two conflicting token systems behind.

## Pairing

Common JIT pairings:

- `design-inspiration-research` — establish evidence-backed direction before encoding it;
- `design-taste-frontend` — art direction;
- `impeccable-design` — critique/polish;
- `figma-design-workflow` — when Figma is authoritative;
- `frontend-ui-engineering` — implement the contract;
- `browser-testing-with-devtools` — rendered verification.

Load only the pairings the current task needs.

## Failure modes

- auto-creating `DESIGN.md` in every frontend repo;
- treating an alpha external schema as permanently stable;
- making `DESIGN.md` override a stronger canonical source silently;
- copying a fashionable design system instead of encoding project truth;
- putting temporary campaign/page styling into the durable brand contract;
- duplicating every CSS variable with no rationale;
- claiming consistency because lint passed without checking rendered UI;
- loading the entire design system into unrelated sessions/workers.
