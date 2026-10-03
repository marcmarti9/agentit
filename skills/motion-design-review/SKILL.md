---
name: motion-design-review
description: Review existing UI motion when a product, component, or flow needs evidence-led feedback on animation purpose, interaction frequency, interruption, reduced-motion behavior, or runtime cost. Use for a motion audit or critique; do not use to create animation, select a library, or optimize a proven performance bottleneck.
license: Apache-2.0
---

# Motion Design Review

Review how existing motion communicates state without deciding an aesthetic
direction or implementing a fix. This skill owns diagnosis; `emil-design-eng`,
GSAP, Motion, and platform-specific skills own creation and library mechanics.

## Trigger and boundary

Use for an existing rendered interface or source target when the question is
whether its motion earns its place, interferes with use, handles interruption,
or respects motion preferences. A request may cover a component, workflow, or
screen transition.

Do not use for a request to add animation, redesign a visual system, migrate an
animation library, or profile a demonstrated performance regression. Route
those jobs to the current creation, design-system, or performance owner.

Do not turn a review into remediation. Offer minimal, retestable repair
directions; change source only when remediation is included in the user’s request.

## Establish the review target

Record the smallest reviewable scope before judging it:

1. Identify the user goal, the exact state transition, trigger, and affected
   controls or content. Preserve the existing brand and stack as evidence.
2. State interaction frequency and consequence: rare/celebratory, occasional,
   frequent, keyboard-initiated, or system-driven. Frequency informs scrutiny;
   it is not a duration rule.
3. Obtain a reproducible route/component state and the available evidence:
   source location, browser observation, reduced-motion setting, and any
   performance trace. If absent, perform a partial source review and label the
   missing observation.
4. Read local motion/design decisions when they exist. Do not infer an intended
   brand language from a generic pattern or replace a stack library.

## Review each meaningful transition

For every candidate motion, answer in this order:

1. **Purpose.** Does it reveal a state change, preserve spatial continuity,
   acknowledge input, explain a relationship, or deliberately provide rare
   delight? If none applies, record decorative motion as a concern only when it
   competes with task completion or repeats enough to become friction.
2. **Context.** Is its prominence appropriate to the product, content, and
   frequency? A productive tool and a playful onboarding flow may reasonably
   reach different conclusions. Do not impose a universal duration, spring, or
   easing threshold.
3. **Control and interruption.** When input reverses, Escape closes, focus
   moves, navigation changes, data fails, or reduced motion is selected, does
   the visible state remain correct and the next action available? Flag an
   interrupted transition only with observed or source-located evidence.
4. **Entry, exit, and state continuity.** Check whether a new, removed, loading,
   error, or reordered state becomes understandable without unexplained jumps,
   stranded focus, duplicate content, or stale announced status.
5. **Reduced motion.** Inspect the actual preference branch when available.
   Essential information and controls must remain usable; a reduced version may
   be instant, simplified, or otherwise appropriate. Never assume a CSS media
   query exists from a screenshot.
6. **Runtime cost.** Separate an observed/measured problem from a likely code
   risk. Inspect layout-affecting animation, sustained scroll work, uncontrolled
   repeated timers, and cleanup on unmount/navigation. Do not claim FPS, frame
   time, or a contrast value from screenshots; use a profiler/trace for a
   measured performance finding.

## Evidence labels and priority

Use one evidence label on every finding:

- **Measured** — trace/profile or reproducible runtime measurement, with tool
  and state recorded.
- **Observed** — replayed in the specified rendered state.
- **Source-located** — file/line or stable snippet shows the behavior/risk.
- **Reported** — supplied by a user or test report and not independently seen.
- **Pending manual review** — requires device, assistive technology, or product-owner
  judgment not available in this run.

Prioritize by user impact and reach: blocking/task disorientation first, then
repeated friction or preference failure, then isolated polish. Do not label a
preference as a defect without a user/task consequence.

## Finding format

Use a compact table. Each row must be retestable.

| Priority | State and evidence | User cost | Minimal repair direction | Retest |
|---|---|---|---|---|
| High | Cart removal, **Observed** at `/cart`; focus remains on removed control | Keyboard user loses location | Restore a stable focus target after exit completes or is skipped | Remove with keyboard under normal and reduced motion |

The repair direction states the behavioral outcome, not a library migration or
unapproved design replacement. Where a finding needs implementation detail,
name the existing owner and preserve its current stack.

## Completion and limits

A review is complete when it names the reviewed states, context/frequency,
evidence coverage, prioritized findings, and missing checks. Report a clean
scope as “no issue observed in the reviewed states,” never as universal motion,
accessibility, or performance approval.

Read [coverage.md](references/coverage.md) only when the target includes
scroll-linked motion, data-driven state changes, native platforms, or a claimed
performance issue.
