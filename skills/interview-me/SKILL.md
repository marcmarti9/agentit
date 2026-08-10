---
name: interview-me
description: Confirm product intent and effort level before planning. Use for every product-affecting task; bypass only purely mechanical work with no product decision.
---

# Interview Me

## Core rule

For Agentit, **interview is the default entrypoint for product work**. If the task creates or changes a product, feature, page, workflow, architecture, API, UX, visual design, content, or other meaningful engineering/product decision, interview before planning or implementation.

The only normal bypass is purely mechanical execution with no product decision: explicitly named directory/file creation, exact moves/renames, deterministic formatting, running an explicitly requested command/test, or copying exact content.

If unsure whether a task is mechanical or product-affecting, treat it as product-affecting and interview.

Canonical effort catalog: `effort/levels.yaml`.

## Comprehensive batch first

Agentit should minimize conversational latency. **Ask all material questions you can reasonably formulate in one interview round instead of drip-feeding questions one by one.**

For product work:

1. inspect repo/docs/tools first so discoverable facts are not asked;
2. build the complete set of material user decisions identifiable now;
3. ask them together in **one numbered batch**;
4. attach a recommendation/default to every question;
5. include the Standard / Polished / Studio recommendation in the same batch;
6. wait for the user's answers;
7. ask a **follow-up batch** only if those answers expose **genuinely new material decisions** that could not reasonably have been asked before.

Do not intentionally save known questions for later. Preferred outcome: **one comprehensive interview round, one user reply, then persist state and implement**.

A follow-up is valid when an answer creates a previously irrelevant branch. It is not valid merely because the agent wanted shorter messages.

## Interview goals

The interview must:

1. discover what the user actually wants before code locks in assumptions;
2. confirm how much work Agentit should spend: Standard, Polished, or Studio;
3. produce enough confirmed state for another session/provider/machine to resume the work.

## Effort levels

### Standard

Efficient production-quality execution. Minimal research, usually one agent, focused implementation and verification.

Typical total model-token envelope: **~15k-80k** across parent + delegated calls.

### Polished

Higher-quality execution with deliberate research/review, stronger edge-case handling, more visual/interaction polish, and more iterations when useful.

Typical total model-token envelope: **~50k-250k**.

### Studio

Quality-first flagship/high-ambition execution. Deep discovery, current research, multiple concepts when useful, specialist delegation/model diversity, independent critique, broader QA, and more iteration.

Typical total model-token envelope: **~150k-800k+**.

These are rough total-session estimates, not billing guarantees. Never pretend precision.

## Build the complete interview batch

Before asking, identify every currently knowable decision category that could materially change the result. Use only relevant dimensions, but do not defer a relevant question because there are many.

Possible dimensions:

- outcome/problem;
- audience;
- success criteria;
- scope/non-goals;
- business/information goal;
- behavior/workflow;
- UX tradeoffs;
- visual personality, references, anti-references;
- content/copy/brand/positioning;
- device/platform/browser constraints;
- accessibility;
- performance/latency/cost;
- privacy/security/data ownership;
- architecture/integration tradeoffs the user actually owns;
- acceptable risk/reversibility;
- launch/deployment expectations if in scope;
- maintainability/learning/handoff expectations;
- effort level.

Do not ask stack, package versions, repo layout, existing routes/styles, test commands, or other facts that tools can inspect.

## Question format

Every question gets a recommendation/default and enough explanation for fast reaction.

```text
INTERVIEW — I think I can cover the material decisions in one round.

1. Primary audience
   Recommendation: recruiters + technical hiring managers.
   Question: Is that primary, or should clients/founders be equally important?

2. Visual risk
   Recommendation: ambitious but usable; unusual interactions only when they improve the story.
   Question: Confirm or prefer conservative?

3. Effort
   Recommendation: Studio because concept quality is a major part of the value.
   Standard: ~15k-80k — clean, limited exploration.
   Polished: ~50k-250k — stronger research/polish.
   Studio: ~150k-800k+ — deeper research, concepts, specialists, critique.
   Question: Which level do you confirm?
```

The user should be able to answer all numbers in one message.

## Small product changes

Mandatory interview does not imply a huge questionnaire. If only two decisions exist, ask both at once.

```text
I only see two decisions:
1. Keep current animation and only change breakpoint? Recommendation: yes.
2. Effort: Standard. Recommendation: Standard (~15k-80k envelope; likely far below the ceiling here).
Confirm/correct both and I'll implement.
```

## Effort recommendation contract

Do not present the levels as a blind menu. Recommend by marginal value and explain:

- why the level fits;
- what lower/higher levels change when relevant;
- rough token envelope / relative cost;
- likely research/specialist/iteration depth;
- what the user gains or gives up.

The user must confirm the effort level before implementation. Explicit `Studio`, `go all out`, `keep it Standard`, etc. counts when unambiguous.

## Restate + persistence gate

After answers arrive:

1. resolve contradictions;
2. if answers exposed new material decisions, ask one follow-up batch containing all of them;
3. otherwise restate confirmed intent compactly;
4. persist confirmed state according to `docs/PROJECT_CONTINUITY.md` **before implementation**.

For meaningful work, capture:

```text
Outcome: ...
Audience: ...
Success: ...
Constraints: ...
Out of scope: ...
Effort: Polished
Budget expectation: ~50k-250k total model tokens, rough/provider-dependent
```

Do not rely on chat history as the only copy.

## Stop condition

Stop interviewing when:

- all currently material user decisions are answered;
- effort is confirmed;
- no known material question is intentionally deferred;
- further questions are unlikely to change the result materially.

For open-ended/high-cost work ask: `Can a fresh agent read persisted intent and make the same major decisions without this chat?` If not, ask/document what is missing.

## Mid-task escalation

If execution reveals the selected level is no longer realistic, do not silently burn a much larger budget. Ask one compact escalation batch containing every newly exposed user decision plus the proposed effort change.

Correctness/safety are exceptions: never knowingly ship broken/unsafe work to preserve budget.

## Non-interactive contexts

Do not fake interviews in CI/scheduled/autonomous contexts. If unresolved product decisions or effort confirmation are required and no live user/documented answer exists, block rather than guess.

## Anti-patterns

- one known question per message when several are already identifiable;
- deliberately withholding questions for later;
- implementation before effort confirmation;
- bypassing because a product change looks easy;
- asking discoverable facts;
- generic giant questionnaires with irrelevant questions;
- Studio by default for design;
- precise-looking token billing promises;
- silent Standard → Studio escalation;
- finishing interview without persisting decisions.

## Verification checklist

- [ ] Mechanical bypass vs product work classified.
- [ ] Product work interviewed before planning/implementation.
- [ ] Discoverable facts inspected first.
- [ ] All currently identifiable material questions asked in the same batch.
- [ ] Every meaningful question included a recommendation/default.
- [ ] Effort recommendation included consequences and rough token estimates.
- [ ] User explicitly confirmed effort.
- [ ] Follow-up only for genuinely new material decisions.
- [ ] Confirmed intent persisted before implementation.
- [ ] Execution stayed within effort spirit or asked before escalation.
