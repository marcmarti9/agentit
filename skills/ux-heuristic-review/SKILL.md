---
name: ux-heuristic-review
description: Review a concrete user task or prototype flow for navigation, comprehension, state transitions, error prevention/recovery and user control. Use for an expert usability walkthrough before or after implementation. Not a visual polish pass, participant research, keyboard/AT certification or a reason to redesign a functioning flow.
license: Apache-2.0
---

# UX Heuristic Review

Find where a person loses the ability to understand, act or recover. Evaluate
the user's task rather than counting violations of a style checklist. An expert
walkthrough proposes risks; it does not establish actual user-test results.

## Define the task and evidence

Identify the actor, starting point, intended outcome, prerequisites, permissions
and meaningful failure paths. Use known product context and actual data shapes.
Bound the screens and branches before reviewing; do not invent a full research
program for a localized change.

Record whether the target is a live flow, prototype, annotated wireframe,
screenshots or source. A prototype can prove proposed transitions but not real
data persistence. An arrow in a flow diagram is not an observed implemented state.
Label each conclusion as observed, source-confirmed, proposed or not assessed.

## Walk the flow

1. Walk once as an unfamiliar person, following visible instructions rather than
   private knowledge of how the system was built. At each step state what the
   person is trying to do, what options appear and what signals progress.
2. Walk the frequent-user path where relevant: repeated actions, safe shortcuts,
   return visits and recovering context. Do not add shortcuts to infrequent tasks
   just to satisfy a heuristic.
3. Check the actual state graph: entry, pending, success, empty, error, interruption
   and return/undo where the flow can reach them. Include invalid input, rejected
   permission, stale data or interrupted network only when relevant to this task.
4. Inspect the decision points against these lenses:

| Lens | Concrete questions |
| --- | --- |
| Status | Can the person distinguish pending, completed and failed work? Is feedback tied to the action? |
| Language/mental model | Do labels and ordering match the domain and actor's understanding? |
| Control | Can the person exit, backtrack, undo or cancel safely where appropriate? |
| Consistency | Does the same action/term behave the same way across this flow? |
| Prevention | Are destructive, ambiguous or repeated actions guarded proportionately? |
| Recognition | Are prior choices and needed context visible rather than recalled? |
| Efficiency | Does frequent work require avoidable repeated entry or navigation? |
| Relevance | Does secondary content obscure the decision or next action? |
| Recovery | Is the error intelligible, associated with the cause, and recoverable without losing valid work? |
| Assistance | Is help available at the difficult step without replacing understandable design? |

Heuristics explain a failure; they do not require every control to implement
every listed feature. Preserve proven native/platform conventions and brand.
Do not substitute perceived visual novelty for a working task model.

## Prioritize evidence, not checklist totals

For each finding, include task/step/state, evidence, the affected actor, failure
mechanism, impact, proposed smallest repair and a way to verify it. Distinguish
blocking task loss, substantial repeated friction and minor inconvenience.
Frequency/reach require actual evidence or are marked unknown; do not manufacture
persona research, task-completion percentages or a precise composite score.

Look for deceptive interaction only from observed behavior: concealed charges,
obscured cancellation, misleading consent or an action that contradicts its label.
Describe the mechanism and user harm. A heuristic review alone does not establish
legal noncompliance; legal determinations require applicable current authority.

If readability, overload or remembering information is the principal issue,
select the cognitive-load branch of `accessibility-design-review`; a generic
flow review need not load it. A contrast/AT audit or animation review similarly
has a separate specialist scope, not automatic activation.

## Plan or rendered review

- **Before implementation:** return proposed state gaps and acceptance scenarios.
  Verify that every important failure has a recovery route and each proposed
  control serves the task. A wireframe is not runtime evidence.
- **After implementation:** execute permitted relevant paths when tools exist;
  record what happened. Without execution, return a source/prototype review and
  pending retests rather than claiming the task is usable in production.
- **Accumulated product drift:** read [design-debt.md](references/design-debt.md)
  only for a requested cross-surface debt inventory. Do not expand a local
  walkthrough into a product-wide redesign.

## Completion and limits

Return the task and coverage, prioritized located findings, viable paths to
preserve, concrete corrections and test scenarios. Default to read-only; a
review request does not authorize production transactions or remediation.
Participant research, cognitive accessibility, visual taste and functioning
implementation remain distinct evidence surfaces. Never claim an independent
evaluation for a same-context self-check.

Adapted from Owl-Listener's heuristic evaluation; MIT source notice retained in
the adaptation manifest. Removed fixed evaluator counts and arbitrary score
arithmetic; kept a task-based, host-neutral procedure.
