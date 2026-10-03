---
name: data-visualization-design
description: Design or review a decision-facing chart or analytical exhibit for honest encoding, perceptual clarity, uncertainty, accessibility, and target-size rendering. Use after data definitions are trustworthy; do not use to repair data-quality mathematics, invent precision, or compose a whole dashboard system.
license: Apache-2.0
---

# Data Visualization Design

Turn validated evidence into a chart whose visual claim matches the data. This skill owns message,
encoding, scale, annotation, and render review for an exhibit. The data owner owns collection,
definitions, joins, calculations, forecasts, and quality math.

## Use when

- A report, product, presentation, or analysis needs a chart selected or improved.
- An existing visual may mislead through scale, chart type, clutter, colour, or missing context.
- A decision audience needs one clear, auditable takeaway from an analytical exhibit.

## Do not use when

- The task is validating source data, statistics, forecasts, causal claims, or reconciliation;
  use the data-quality/analysis owner first.
- The request is layout, navigation, KPI hierarchy, filters, or multi-chart product behaviour;
  use the dashboard/product owner.
- A table provides the needed exact lookup and no visual comparison is justified.
- Values, units, grain, denominator, missingness, or uncertainty are unknown; do not fabricate
  a chart or infer numeric precision.

## Inputs and boundary

Require a one-sentence decision question, intended audience/action, validated data source,
definitions and units, grain/time range, missingness, uncertainty, and delivery constraints. Mark
every reported or supplied fact as such. A chart can clarify evidence; it cannot make uncertain
inputs certain.

## Procedure

1. State the decision message before choosing a chart: comparison, change over time, distribution,
   composition, relationship, or geography. Name the action the reader should be able to take.
2. Inspect the data contract. Confirm measures, denominators, ordering, inclusion/exclusion,
   rounding, intervals, and missing values with the data owner. Stop at a labelled specification if
   material facts are unresolved.
3. Choose the encoding that makes the key comparison accurate. Prefer aligned position or length
   for magnitude; use a chart type justified by the message, not a decorative default. Reject 3-D
   effects, pictorial area guesses, and dual axes that manufacture apparent correlation.
4. Set truthful scales. Bars start at zero; line or dot scales may focus on change only when the
   bounds and reason are plainly disclosed. Keep comparable panels on comparable scales. Show
   units, time coverage, denominators, and baselines.
5. Compose the exhibit. Use an action title, direct labels or a nearby legend, restrained emphasis,
   useful annotation, and source/date notes. Remove ink that does not improve reading, but preserve
   provenance and caveats.
6. Encode uncertainty where it could change the decision: intervals, ranges, scenario bands,
   completeness notes, or a precise limitation. Never replace an unknown interval with a precise
   single value.
7. Build accessible alternatives: colour-independent distinction, adequate text/mark contrast,
   text alternative/caption, and a backing table or accessible data access where exact values
   matter. Recompose at narrow widths; do not simply scale down labels and marks.
8. Render at the stated target sizes and inspect the takeaway, labels, clipping, overlap, axes,
   contrast, colour-vision distinction, and interactive focus/motion where relevant. Keep the
   rendered artifact and source/definition record together.

## Decision rules

| Message | Usual starting point | Integrity gate |
|---|---|---|
| Ranked comparison | Sorted bar or dot plot | Common baseline and stated units |
| Trend | Line or aligned small multiples | Time continuity and disclosed bounds |
| Distribution | Histogram, dot, box, or interval view | Spread and outliers not hidden by averages |
| Composition | Stacked/bar comparison when parts matter | Denominator and residual/missing parts shown |
| Relationship | Scatter or aligned paired view | No causal claim from correlation alone |
| Geographic pattern | Map only when location is the question | Normalisation, bins, and no-data treatment |

## Evidence and degradation

Without validated data, calculations, or rendering, produce a labelled chart specification or
placeholder and list the pending integrity checks. Do not call it accurate, accessible, responsive,
or decision-ready. Publication and downstream operational decisions remain separately authorised.

## Handoff

Ship the chart source or reproducible specification with its data snapshot/reference, field
definitions, calculation owner, annotation text, accessibility alternative, target renders, and
review date. A visual review does not approve the underlying query, statistical method, or business
decision; route those sign-offs to their responsible owners.

## Common failures

- Selecting a visually familiar chart before stating the decision question.
- Using a truncated bar axis, unequal panels, or dual scales to amplify a small difference.
- Hiding no-data categories, provisional values, or uncertainty in a footnote too small to read.
- Relying on colour and a detached legend when direct labels or pattern cues are needed.

## Completion record

Record the data version or query reference, calculation owner, selected encoding, scale decision,
target render sizes, and outstanding limitations. This lets reviewers reproduce the visual claim
without confusing visual design evidence with mathematical validation.

## Acceptance

- The message, source, definitions, units, uncertainty, and decision context are visible.
- Type, scale, and encoding match the key comparison without visual exaggeration.
- The target render communicates the stated takeaway with accessible alternatives.
- Any data-quality, calculation, or render limitations are explicit and not hidden by polish.
