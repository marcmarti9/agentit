---
name: diagram-and-architecture-visuals
description: Choose and produce truthful diagrams for systems, processes, data, architecture and presentations. Route branded/general visual diagrams toward diagram-design, code-grounded interactive architecture maps toward Archify, and keep simple cases simple.
license: MIT-compatible original Agentit guidance
sources:
  - https://github.com/cathrynlavery/diagram-design
  - https://github.com/tt-a1i/archify
---

# Diagram and Architecture Visuals

Use this skill when a diagram will communicate structure, flow, state, ownership, dependencies or quantitative relationships better than prose/table alone.

Do not make a diagram merely because the task is technical. A good diagram reduces cognitive load; a bad one converts readable text into boxes and arrows.

## First decision: should this be a diagram?

Prefer prose/table when:

- the relationship is trivial;
- a two-column or three-column table communicates the same thing;
- there is only one meaningful node/action;
- the artifact would need a paragraph of legend just to become understandable.

Use a diagram when spatial relationship, order, branching, state, trust boundaries, topology, ownership or relative quantity is materially easier to understand visually.

## Route by job

Agentit does not vendor every upstream diagram skill into core. Choose the smallest useful implementation family JIT.

### General/branded visual communication -> diagram-design

Use or inspect `cathrynlavery/diagram-design` when the job is primarily **visual explanation** and benefits from a polished standalone diagram.

The inspected upstream supports a broad type library including architecture, flowchart, sequence, state machine, ER/data model, timeline, swimlane, quadrant, radar, loop/flywheel, trees, layers, Sankey, Wardley, deployment, dependency, UML, story maps and database schemas. It uses progressive disclosure: choose the visual/semantic type, then load only its relevant reference material.

Useful upstream principles to preserve:

- choose semantic meaning before styling;
- prefer deletion over decorative density;
- one visual grammar per artifact;
- keep hierarchy visible rather than using identical boxes everywhere;
- brand/style tokens should come from project truth, not generic “tech” defaults;
- verify geometry, labels and connectors rather than trusting a screenshot glance.

Do not copy its whole reference tree into Agentit context. Inspect only the current upstream material required by the selected diagram type and license/project fit.

### Code-grounded system map -> Archify

Use or inspect `tt-a1i/archify` when the job is primarily **truthful architecture mapping from a codebase/system description**, especially when validation, source evidence, deterministic rendering or before/after architecture comparison matters.

The inspected Archify workflow uses typed JSON IR and deterministic validation/rendering to produce interactive HTML/SVG-style system maps. It is particularly suitable for:

- repository runtime architecture;
- architecture review before/after a change;
- workflow/sequence/data-flow/lifecycle views;
- route and dependency inspection;
- maps where authored relationships must not be invented by the viewer;
- source-linked architecture evidence when requested.

Treat Archify output as a communication artifact grounded in the evidence supplied to it, not omniscient runtime truth. “Reach” in an authored graph is not automatically production impact.

### Simple/portable source diagram -> project-native format

For small maintainable documentation diagrams, Mermaid, PlantUML, Graphviz, D2 or the project's existing format may be stronger than introducing a new tool.

Prefer the project's existing source-controlled diagram format when it already solves the job adequately.

### Quick scratch explanation -> text

For a tiny conversational explanation, a short text/ASCII diagram can be enough. Do not spin up a full visual toolchain for three boxes.

## Diagram selection

Choose the visual form from the relationship being communicated:

```text
components + connections       -> architecture / dependency graph
messages over time             -> sequence
branching decisions            -> flowchart
states + transitions           -> state machine / lifecycle
entities + relationships       -> ER / database schema
cross-team handoffs            -> swimlane / workflow
movement of data               -> data flow / Sankey where quantity matters
trust/security boundaries      -> architecture / data flow with explicit boundaries
work over time                 -> timeline / Gantt
ownership/reporting            -> org/ownership map
causal categories              -> fishbone
value chain vs evolution       -> Wardley map
```

Do not combine several diagram grammars into one page unless the relationship genuinely requires it. An overview plus focused detail is usually clearer.

## Evidence before layout

For technical architecture, collect source truth before drawing:

- repository/component boundaries;
- entry points;
- actual calls/events/dependencies;
- stores/queues/external systems;
- trust boundaries and credentials flows when relevant;
- deployment/runtime placement when known;
- important failure/retry paths;
- source paths/commits when source-backed claims matter.

Mark uncertain/inferred relationships explicitly. Do not turn a plausible architecture guess into a solid arrow.

## Complexity budget

A diagram should have a clear reading order and focal question.

Before rendering, define:

```text
question: <what should the reader understand?>
audience: <who?>
view: <architecture|sequence|flow|...>
primary path: <main story>
secondary detail: <what can move to cards/notes/detail view?>
evidence status: <observed|inferred|mixed>
```

If the overview needs dozens of equally weighted nodes, split it:

```text
overview -> one or more focused detail diagrams
```

Do not solve complexity by shrinking labels until they become unreadable.

## Visual anti-slop gate

Reject the generic generated-diagram bundle when it is not project-appropriate:

- dark canvas + cyan/purple glow merely to signal “tech”;
- every node as the same rounded card;
- monospace for every label;
- excessive gradients/shadows;
- arrows crossing through unrelated nodes;
- unexplained color coding;
- decorative icons with no semantic value;
- huge legend compensating for unclear layout;
- 20+ nodes on one “high-level” view;
- fabricated metrics/topology to make the visual look complete.

Use existing brand/system tokens when the artifact belongs to a branded project. If a canonical `DESIGN.md` exists, pair with `design-md-workflow` and extract only the relevant visual roles.

## Architecture documentation contract

A diagram supplements durable docs; it does not replace them.

When a substantial architecture diagram is committed:

- keep an editable/source representation when practical;
- state its scope and evidence date/commit when staleness matters;
- link it from the canonical architecture/component documentation;
- explain boundaries/invariants that are unsafe to infer from geometry alone;
- update or remove it when the documented architecture changes materially.

A stale beautiful diagram is worse than no diagram because it looks authoritative.

## Verification

Verification depends on the chosen tool, but should cover the artifact rather than only successful generation.

Check:

- all nodes/relationships correspond to approved or evidenced facts;
- labels are readable at delivery size;
- arrows/routes are unambiguous and do not create accidental relationships;
- primary path is visually obvious;
- color/shape semantics are consistent;
- accessibility/contrast is reasonable for the delivery surface;
- responsive/export behavior works when HTML/SVG is delivered;
- source-controlled diagrams regenerate deterministically enough for review;
- source links, if present, point to the intended revision/range;
- before/after architecture views distinguish authored facts from inferred impact.

When using an upstream tool, run its current validators/doctor/delivery checks when available instead of asserting quality from inspection alone.

## Pairing

Useful JIT pairings include:

- `documentation-and-adrs` — durable architecture/system docs;
- `source-driven-development` — current tool/spec docs or source-grounded architecture;
- `context-engineering` — very large repositories/evidence sets;
- `design-md-workflow` — branded design-token consistency;
- `browser-testing-with-devtools` — HTML/SVG interaction/export verification;
- `reference-intelligence` — current external diagram/tool research when materially needed.

Do not load all of them by default.

## Handoff

For material diagram work, leave a compact receipt:

```text
DIAGRAM_DECISION
goal: <reader question>
format/type: <...>
implementation_family: project-native | diagram-design | archify | other
source_of_truth: <repo/docs/data/user description>
evidence_status: observed | inferred | mixed
scope_excluded: <what intentionally stays out>
source_artifact: <path if committed>
rendered_artifact: <path/url if applicable>
verification: <checks/results>
```

## Failure modes

- installing a large diagram stack for a trivial sketch;
- choosing a visual type from aesthetics rather than semantics;
- using Archify as if static analysis proves live production behavior;
- using a general diagram renderer to invent undocumented topology;
- shipping only a PNG when the diagram must evolve with the code;
- copying an upstream default skin into a branded project;
- mixing several diagram languages into one unreadable artifact;
- treating a generated architecture diagram as documentation complete by itself.
