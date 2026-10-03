# Paired evaluations for skill changes

Read this when a material change to a skill needs evidence that it improves behavior without broadening activation or adding context cost. It is unnecessary for an isolated typo or a documentation-only correction.

## Specify the decision boundary first

Create a compact set of realistic prompts before judging the changed skill:

- clear positive cases covering different legitimate requests;
- near-miss negatives that share vocabulary but belong to another skill or bare execution;
- one ambiguous/multi-intent case where the model must choose the smallest justified capability;
- a case that exercises a safety, provenance or handoff boundary if the change touches one.

For every case, name the observable output properties and the failure that matters. Do not reward a response merely for repeating skill vocabulary or producing a longer answer.

## Compare behavior, not a single polished example

Where feasible, run the same cases with the changed procedure and an appropriate baseline: the prior revision for a refinement, or no skill for a new capability. Keep task context, tools, evidence and output constraints equivalent. Capture delivery evidence separately from output quality: a selected body being delivered does not prove the behavior was useful.

Review these four dimensions independently:

| Dimension | Question |
| --- | --- |
| Selection | Did it activate for positives and stay out of near-misses? |
| Delivery | Was the intended complete body/reference actually supplied? |
| Behavior | Did the output meet the decision-specific evidence and quality criteria? |
| Cost | Did added instructions, tools or steps earn their complexity/time/context? |

Use reproducible assertions for mechanical properties and blinded or human comparative review for subjective quality. Label same-context critique as non-independent.

## Read failures for causes

An assertion that passes for both baseline and changed runs is non-discriminating. A high-variance result may mean the task is under-specified, the grader is vague, or the behavior is unstable. A pass rate alone can hide an unacceptable safety failure, wrong-skill activation or extra dependency. Change the procedure only when the failure pattern points to a generalizable cause; do not overfit a single prompt.

## Source-informed adaptation

- **Source:** [anthropics/skills `skill-creator`](https://github.com/anthropics/skills/tree/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/skill-creator), Apache-2.0.
- **Role:** licensed artifact and inspiration for before/after evaluation, benchmark analysis and separating qualitative review from machine assertions.
- **Observed:** its workflow compares baseline and skill-enabled outputs, investigates variance/non-discriminating assertions and uses user review for subjective quality.
- **Decision changed:** Agentit gains the smaller paired-evaluation procedure above, aligned to its own selection/delivery/behavior/context-cost contract.
- **Not imported:** Anthropic’s Claude-specific commands, browser viewer, scripts, scoring thresholds, packaging process or mandatory human loop.

This is an original provider-neutral adaptation. Preserve the Apache-2.0 license/NOTICE obligations in project notices if source-derived material is redistributed.

Distribution attribution and exact source licenses are retained in `THIRD_PARTY_NOTICES.md`, `skills/ADAPTATION_SOURCES.json` and `vendor/adaptation-licenses/`. This reference is an Agentit-authored adaptation; it does not include upstream runtime/scripts.
