---
name: skill-authoring-and-evals
description: Creates, edits and evaluates agent-facing skills and instruction documents with discriminative triggers, progressive disclosure and activation tests. Use when adding or changing SKILL.md files, AGENTS.md/CLAUDE.md guidance, skill descriptions, trigger behavior, or skill evals. Do not use merely because a task happens to consume an existing skill.
---

# Skill Authoring and Evals

## Purpose

Make agent instructions reliable without turning the repository into a prompt megapack.

A good skill has one coherent responsibility, a trigger a model can distinguish from neighboring skills, an explicit non-trigger boundary, and a small main body whose branch-specific material is progressively disclosed.

Read Agentit's own `docs/SKILL_CURATION.md` before adding a permanent skill.

## BUILDER workflow

### 1. Establish the gap

Before writing a new skill, inspect existing Agentit coverage.

Prefer, in order:

1. no change if the behavior is already covered;
2. strengthen the existing owner if the responsibility is the same;
3. adapt a genuinely better external capability;
4. create a new skill only for a distinct repeated workflow.

Do not create synonyms for existing skills.

### 2. Write the activation contract

Define:

- **responsibility** — one job this skill owns;
- **positive triggers** — distinct situations where it should be selected;
- **negative triggers** — nearby situations where it should not be selected;
- **completion criteria** — observable evidence that the procedure succeeded;
- **references** — only branch-specific material worth keeping out of the main body.

The frontmatter description is a context pointer. It should say both what the skill does and when it applies. Do not stuff it with synonyms that describe the same branch.

### 3. Keep the hierarchy legible

The main `SKILL.md` contains the steps and rules needed on every invocation.

Move material behind a reference only when some invocations do not need it. A pointer must state when to read that reference.

Do not hide mandatory execution steps behind vague links. Do not duplicate the same rule in multiple documents.

### 4. Write for Agentit authority

A skill may recommend a procedure; it may not:

- broaden host/user permissions;
- auto-activate another skill;
- replace `task-router` semantic selection;
- convert its own upstream workflow into a mandatory project lifecycle;
- override BUILDER/REVIEW verification cadence;
- claim that listing or installing a skill means its body was loaded.

If a third-party workflow conflicts with Agentit policy, adapt the useful capability rather than importing the conflict.

### 5. Minimal authoring checks

During BUILDER, perform only the checks needed to avoid a broken skill:

- valid YAML frontmatter;
- `name` matches the directory ID;
- description is discriminative and within repository limits;
- referenced local files exist;
- the skill appears in at least one discovery pack or core;
- no unintended core/profile expansion.

Do not build an elaborate eval harness for a tiny wording change.

## REVIEW workflow

When the skill is ready, test **selection quality and delivered behavior**.

Use a compact eval set containing:

- clear positive prompts;
- near-miss negative prompts;
- ambiguous prompts where another skill should own the task;
- one or two realistic multi-intent prompts.

Evaluate separately:

1. **Discovery/selection:** was this skill chosen only when justified?
2. **Delivery:** was the exact complete selected `SKILL.md` body delivered?
3. **Behavior:** did the procedure improve the output without violating Agentit policy?
4. **Context cost:** did the new permanent surface earn its size?

Do not optimize only for trigger recall. A skill that activates everywhere is broken.

For subjective skills, human comparative review can be more useful than invented numeric metrics. For mechanically verifiable skills, prefer reproducible assertions.

For a material behavior or activation change, read [paired-evaluations.md](references/paired-evaluations.md) before defining the evaluation. Compare selection, delivery, behavior and cost separately; a fixture manifest alone is not a model benchmark.

## Description tuning

If selection has false negatives, sharpen the missing branch in the description.

If it has false positives, narrow the scope or add an explicit non-trigger.

Do not solve trigger problems by making a skill global/core unless it truly belongs in most material tasks.

## Agent-document rule

The same discipline applies to `AGENTS.md`, `CLAUDE.md` and other agent-facing docs:

- always-loaded material must earn every line;
- put the governing rule close to where it is used;
- point to deeper material with a clear condition;
- avoid competing sources of truth;
- write completion criteria instead of motivational prose.

## Completion criteria

The change is complete when:

- the responsibility is distinct;
- triggers and non-triggers are clear;
- the skill is discoverable without being globally active;
- selected activation delivers the complete body;
- branch-only references are explicit and resolvable;
- a focused eval demonstrates acceptable positive/negative selection behavior;
- provenance/license obligations are recorded for substantial external adaptation.
