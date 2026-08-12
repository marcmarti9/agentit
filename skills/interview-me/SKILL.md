---
name: interview-me
description: Confirm product intent before planning. Ask craft depth only for design/visual work. Use for every product-affecting task; bypass only purely mechanical work.
---

# Interview Me

## Core rule

For Agentit, **interview is the default entrypoint for product work**. If the task creates or changes a product, feature, page, workflow, architecture, API, UX, visual design, content, or other meaningful engineering/product decision, interview before planning or implementation.

The only normal bypass is purely mechanical execution with no product decision: explicitly named directory/file creation, exact moves/renames, deterministic formatting, running an explicitly requested command/test, or copying exact content.

If unsure, treat as product-affecting and interview.

Canonical catalogs: `effort/levels.yaml` (domain packs + design craft depth), router domain packs / profiles.

## No powerwords

Users do not need special jargon. Ordinary language is enough. The only harness activation phrase is a natural “use / usa / utilise / … **agentit**” in the user’s language. Do not require fan-out, Studio, pipeline, or similar terms.

## Comprehensive batch first

**Ask all material questions you can reasonably formulate in one interview round.**

For product work:

1. inspect repo/docs/tools first so discoverable facts are not asked;
2. build the complete set of material user decisions identifiable now;
3. ask them together in **one numbered batch**;
4. attach a recommendation/default to every question;
5. include **domain pack** (skill family) recommendation;
6. include **craft depth** (Standard / Polished / Studio) **only if the task is design/visual**;
7. give a **project-aware token estimate** (not the old fixed 15k–80k menu as a bill);
8. wait for answers;
9. follow-up batch only for **genuinely new material decisions** that could not reasonably have been asked before.

Preferred outcome: **one comprehensive interview round → user reply → persist state → plan/build**.

## What interview must achieve

1. Discover what the user actually wants before code locks assumptions.
2. Choose the **domain pack** (which skill family / MCP stack), not a universal Studio tax.
3. For design/visual work only, confirm craft depth.
4. Persist enough state for another session/provider/machine to resume.

## Domain packs (skill families)

Recommend one primary pack from: engineering, frontend, design, backend, data, product, writing, release, research, or a user role (`role:…`).

Load **always_core + that family’s skills only**. Never load the design studio stack for pure backend work.

If the user assigns a role (“act as a finance expert”), scope skills to that role plus always_core; use `find-skills` / marketplace when local coverage is missing.

## Craft depth — design/visual only

| Level | When |
|---|---|
| **Standard** | Ordinary UI fixes/components; clean and usable |
| **Polished** | Public-facing UI, stronger polish/states/responsive QA |
| **Studio** | Flagship visual/concept work; competition/critique welcome |

Do **not** ask Standard/Polished/Studio for APIs, infra, pure logic, or docs unless there is a real visual surface.

## Spend posture (optional, soft)

If thoroughness is ambiguous for non-design work, recommend **lean / normal / thorough** as soft main-agent rigor — not a multi-agent quota and not fixed token ranges.

## Token estimates

Use router/`token_estimate` style project-aware envelopes:

- risk, complexity, domain pack, topology, specialists/critic, craft depth if any
- say they are rough and provider-dependent
- never present the old fixed tables as authoritative billing

## Build the complete interview batch

Possible dimensions (only relevant ones):

- outcome/problem;
- audience;
- success criteria;
- scope/non-goals;
- UX / visual personality (if visual);
- architecture/integration tradeoffs the user owns;
- risk/reversibility;
- domain pack / role;
- craft depth **if design/visual**;
- whether independent critique or specialists are expected (Architect may still require critic for large structural plans).

Do not ask stack, package versions, routes, or other tool-discoverable facts.

## Question format

```text
INTERVIEW — material decisions in one round.

1. Outcome
   Recommendation: ...
   Question: ...

2. Domain pack
   Recommendation: backend (+ verification). Load only API/data skills, not design studio.
   Question: Confirm or switch pack?

3. Craft depth
   (omit entirely if not design/visual)
   Recommendation: Polished for this landing.
   Question: Standard / Polished / Studio?

4. Rough cost
   Recommendation: ~40k-120k total model tokens for this repo/task (project-aware; not a bill).
   Question: Any spend ceiling?
```

## Small product changes

If only one or two decisions exist, ask both at once. Skip craft depth when irrelevant.

## Critic and specialists

Do not use interview to force multi-agent. The Architect:

- spawns specialists when ordinary language or structure shows benefit;
- always schedules an independent critic for large structural plans;
- may push back if the user asks for many agents without independence.

## Restate + persistence gate

After answers:

1. resolve contradictions;
2. follow-up only for new material decisions;
3. restate confirmed intent;
4. persist per `docs/PROJECT_CONTINUITY.md` **before implementation**.

Capture at least:

```text
Outcome: ...
Audience: ...
Success: ...
Constraints: ...
Out of scope: ...
Domain pack: backend
Craft depth: n/a (not design)
Spend: normal
Token estimate: ~40k-120k (project-aware)
Critic: required for architecture plan
```

## Stop condition

- material user decisions answered;
- design craft depth confirmed **when applicable**;
- domain pack clear;
- state persistable for a fresh agent.

## Mid-task escalation

If scope grows, ask before expanding spend. Safety/correctness may force extra work — disclose it.

## Non-interactive contexts

Do not fake interviews in CI/autonomous contexts. Block rather than guess unresolved product decisions.

## Anti-patterns

- asking Studio/Polished/Standard for non-design work;
- fixed token ranges as if universal truth;
- powerwords or jargon gates;
- loading every skill family;
- one known question per message;
- implementation before persisting intent;
- silent huge spend escalation.

## Verification checklist

- [ ] Mechanical vs product classified.
- [ ] Facts inspected before questions.
- [ ] One batch of material decisions.
- [ ] Domain pack recommended; craft depth only if design/visual.
- [ ] Project-aware token estimate (rough).
- [ ] Intent persisted before implementation.
