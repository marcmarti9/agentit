---
name: spec-kit-workflow
description: Run GitHub Spec Kit's gated spec-driven flow before coding — constitution, specify, clarify, plan, tasks, analyze, implement, converge. Use when starting a feature from a vague prompt, when the project already has .specify/ or specs/, or when the user asks for Spec Kit / speckit / specify. Do not use for one-line fixes.
license: Apache-2.0-compatible original Agentit guidance
metadata:
  source: https://github.com/github/spec-kit
  inspected: v1.0.6
---

# Spec Kit Workflow

GitHub Spec Kit is an optional external Spec-Driven Development toolkit. Agentit does not vendor its CLI, templates, extensions, presets or slash-command prompts.

This skill is the Agentit operating contract around that toolkit. The spec stays the source of truth. Code expresses the spec. Do not start implementation while the current gate is still open.

Live source of truth for commands, artifact paths and templates:

```text
https://github.com/github/spec-kit
```

Re-check current README/command names before depending on exact `/speckit.*` syntax. Inspected against Spec Kit `v1.0.6`.

## When to load

Load when one or more are true:

- the user asks for Spec Kit, speckit, `specify`, or spec-driven development with the GitHub toolkit;
- the repo already has `.specify/`, `specs/`, or a `constitution.md`;
- a new feature/project is too vague to code safely and needs a gated spec first;
- several independently testable capabilities are bundled in one request;
- previous agent passes drifted because there was no reviewed spec.

Do **not** load for typo fixes, one-line patches, or changes whose acceptance criteria are already explicit and local.

`spec-driven-development` remains the generic Agentit spec skill. Load this skill when the project is using, or should use, Spec Kit's artifact layout and gates. Both may be selected. Do not run two competing spec formats for the same feature.

## Authority order

```text
explicit user constraints
-> project constitution (.specify/memory/constitution.md or equivalent)
-> reviewed feature spec
-> reviewed plan / tasks
-> current official Spec Kit docs when command/template details matter
-> existing code and tests
-> model preference
```

If constitution and an existing production contract conflict, surface the conflict. Do not silently override production truth with a stale constitution.

## Cold-session behavior

`.specify/` and `specs/` may persist on disk as durable project knowledge. The **skill body remains JIT**.

A fresh session inspects those artifacts only when the current task is spec/plan/implement work against them. Do not inject the whole Spec Kit tree into unrelated writing, marketing or tiny UI edits.

## Do not vendor the runtime

Never copy Spec Kit's CLI, Python package, templates, hooks or agent integration files into Agentit.

If the project already ran `specify init`, use the artifacts in that project. If it has not:

1. Ask whether the user wants Spec Kit initialized, or a portable Agentit spec without the CLI.
2. Do not install `specify-cli` or mutate global tool state unless the user wants that install.
3. A valid fallback is the gated flow below using project Markdown only.

## Gated flow

Do not advance a gate until the current artifact is reviewable and the open questions that would change the build are resolved or explicitly deferred.

```text
constitution
-> specify
-> clarify
-> plan
-> tasks
-> analyze / checklist
-> implement
-> converge
```

Human review sits on every gate that commits structure, stack, data model or scope. FAST MODE may compress clarify+specify into one pass. It may not skip specify and jump to code on a vague feature.

### 1. Constitution

Project-level rules that survive features. Typical durable home:

```text
.specify/memory/constitution.md
```

Capture only stable standards — testing bar, library-first vs app-first, CLI/API contracts, security constraints, documentation invariants, explicit non-goals.

Write a constitution once per project, then amend it when the standard actually changes. Do not rewrite it for every feature.

### 2. Specify

WHAT and WHY, not HOW.

A feature spec must include:

- user-visible outcome and who it is for;
- in-scope / out-of-scope;
- acceptance criteria that can fail a test or a demo;
- assumptions listed explicitly, not hidden in prose;
- open questions marked instead of guessed.

Preferred layout when the project already follows Spec Kit:

```text
specs/<feature-id>/spec.md
```

If several independently testable capabilities are bundled, write a capability map first and one spec per module id. Do not produce one mega-spec that every later task has to re-parse.

### 3. Clarify

Resolve `[NEEDS CLARIFICATION]` items that would change architecture, data, auth, scope or success criteria.

Ask the fewest questions that unblock the plan. Fold answers into the spec. Do not start `/plan` while material ambiguity remains.

Pair with `interview-me` only when the missing decision is a real product choice, not a missing file you can inspect.

### 4. Plan

HOW, after WHAT is stable.

The plan names stack, major components, data/contracts, build order, risks and verification checkpoints. It must obey the constitution.

Pair with `planning-and-task-breakdown` for dependency graphs and vertical slices. If the two disagree on task mechanics, `planning-and-task-breakdown` wins for sizing/order; this skill wins for Spec Kit artifact shape.

### 5. Tasks

Small, ordered, verifiable units. Each task has:

- a single bounded outcome;
- acceptance criteria;
- a verify step;
- the files it is allowed to touch.

Mark true parallel work only when write ownership does not collide.

### 6. Analyze / checklist

Before implementation, check spec ↔ plan ↔ tasks for coverage gaps, contradictions and constitution violations.

Do not treat a generated checklist as proof. It is a review aid.

### 7. Implement

Execute one task at a time. Update the spec when reality disproves it, then continue. Do not leave the spec behind the code.

Pair with `incremental-implementation`, `test-driven-development` and `verification-before-completion` as justified. FAST MODE still requires the current task's verify step.

### 8. Converge

After implementation, diff the codebase against spec/plan/tasks. Remaining work becomes new tasks. Repeat until the feature matches the spec or the spec is explicitly changed.

"Done" means the accepted spec is satisfied with fresh evidence, not that the task list is empty because items were deleted.

## Commands are host details

Spec Kit exposes host-specific invocations. As of `v1.0.6` the documented family is:

```text
/speckit.constitution
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.tasks
/speckit.analyze
/speckit.checklist
/speckit.implement
/speckit.converge
```

Some hosts use `$speckit-*` skills instead of slash commands. Agentit must not require one host.

If those commands exist in the current host, use them. If they do not, run the same gates by writing the artifacts directly. The gate is the contract, not the slash command.

Optional CLI install is a user/project choice:

```text
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.6
specify init <project> --integration <host>
```

Re-verify the install line from current Spec Kit docs before running it. Never treat CLI presence as permission to initialize a repo.

## Pairing

Load only what the current gate needs:

- `spec-driven-development` — generic spec quality when Spec Kit is not initialized;
- `interview-me` — unresolved product decisions;
- `idea-refine` — early concept shape before specify;
- `planning-and-task-breakdown` — task graph mechanics;
- `source-driven-development` — current framework/API contracts inside the plan;
- `doubt-driven-development` — adversarial review of a high-impact spec/plan;
- `incremental-implementation` / `test-driven-development` — implement gate;
- `verification-before-completion` — fresh evidence before done;
- `documentation-and-adrs` — durable decisions that should outlive the feature spec.

## Failure modes

- installing Spec Kit into Agentit itself;
- treating slash commands as mandatory on hosts that do not have them;
- skipping specify because "the prompt is clear enough";
- writing HOW into the spec and WHAT into the plan;
- guessing away `[NEEDS CLARIFICATION]` items;
- implementing while constitution, spec and plan disagree;
- generating a 40-task list for a 20-minute change;
- claiming converge because the checklist file exists;
- loading this skill for a one-line fix.
