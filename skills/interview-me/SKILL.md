---
name: interview-me
description: Confirm product intent and effort level before planning. Use for every product-affecting task; bypass only purely mechanical work with no product decision.
---

# Interview Me

## Core rule

For Agentit, **interview is the default entrypoint for product work**. If the task creates or changes a product, feature, page, workflow, architecture, API, UX, visual design, content, or other meaningful engineering/product decision, interview before planning or implementation.

The only normal bypass is purely mechanical execution whose purpose is to save time and which does not require or encode a product decision: creating explicitly named directories/files, exact moves/renames, deterministic formatting, running an explicitly requested command/test, or copying exact content.

If unsure whether a task is mechanical or product-affecting, treat it as product-affecting and interview.

Canonical effort catalog: `effort/levels.yaml`.

## Interview philosophy: comprehensive batch first

Agentit should minimize conversational latency. **Ask every material question you can reasonably formulate in one interview round instead of drip-feeding questions one by one.**

For a product task:

1. inspect the repo/tools first so you do not ask discoverable facts;
2. build the complete set of material user decisions you can identify now;
3. ask them together in one numbered interview batch;
4. attach a recommendation/default to every question;
5. include the Standard / Polished / Studio recommendation in that same batch;
6. wait for the user's answers;
7. ask a follow-up batch only if those answers expose genuinely new material decisions that could not reasonably have been asked before.

Do not artificially split a known interview into multiple messages. The preferred outcome is **one comprehensive interview round, one user reply, then implementation**.

A follow-up is valid when an answer creates a new branch that was unknowable beforehand, for example: the user chooses authentication and that exposes a previously irrelevant identity-provider decision. It is not valid merely because the agent chose to save questions for later.

## Why

The interview has three jobs:

1. discover what the user actually wants before implementation locks in assumptions;
2. agree how much work Agentit should spend: **Standard, Polished, or Studio**;
3. produce enough confirmed state to document the task so another session/provider/machine can resume it.

The goal is not maximum questioning. The goal is maximum alignment with minimum conversational round-trips.

## Mandatory effort-level choice

Every product-affecting interview must recommend and confirm an effort level before implementation.

### Standard

Efficient production-quality execution. Minimal research, usually one agent, focused implementation and verification. Good when the desired direction is clear and broad exploration would have low marginal value.

Typical total model-token envelope: **~15k-80k** across the parent and any delegated calls.

### Polished

Higher-quality execution with more deliberate research/review, stronger edge-case handling, additional visual/interaction polish, and usually more iterations. Specialists may be used when they clearly help.

Typical total model-token envelope: **~50k-250k**.

### Studio

Quality-first execution for flagship/high-ambition work. Deep discovery, current research where relevant, multiple concepts when useful, specialist delegation, independent critique, broader QA, and more iteration. Token efficiency stops being the primary optimization only here.

Typical total model-token envelope: **~150k-800k+**.

These are rough total-session estimates, not guarantees. Actual usage varies with task size, provider, model, context, retries, tool output, and whether multiple agents/models are used. Never present them as precise billing forecasts.

## Build the complete interview batch

Before asking, identify all currently knowable decision categories that could materially change the result. Include only relevant categories, but do not postpone a relevant question merely because there are many.

Possible dimensions include:

- desired outcome / problem being solved;
- audience / user type;
- success criteria;
- scope and non-goals;
- business or information goal;
- behavior and workflow expectations;
- UX preferences and tradeoffs;
- visual personality / references / anti-references;
- content, copy, brand, and positioning decisions;
- compatibility/device/browser/platform requirements;
- accessibility requirements;
- performance/latency/cost constraints;
- data ownership / privacy / security expectations;
- architecture and operational tradeoffs the user actually owns;
- integration/dependency constraints;
- acceptable risk / reversibility;
- launch/deployment expectations if in scope;
- maintainability/learning/handoff expectations;
- effort level.

Do not ask a user for facts the agent can inspect: stack, package versions, repo structure, existing routes, available files, current styles, test commands, or documentation that exists locally should be discovered first.

## Question format

Ask one numbered batch. Every question must include your best recommendation/default and enough explanation for a quick reaction.

Example:

```text
INTERVIEW — I think I can cover the material decisions in one round.

1. Primary audience
   Recommendation: recruiters + technical hiring managers, because this is a professional portfolio.
   Question: Is that the main audience, or should clients/founders be equally important?

2. Visual risk
   Recommendation: ambitious but usable; unusual interactions only when they improve the story.
   Question: Do you want that, or a more conservative direction?

3. Content priority
   Recommendation: projects > experience > skills list.
   Question: Agree, or should another signal dominate?

4. Effort
   Recommendation: Studio, because the concept itself is a large part of the value.
   Standard: ~15k-80k — clean, limited exploration.
   Polished: ~50k-250k — more research/polish.
   Studio: ~150k-800k+ — deeper research, concept exploration, specialists and critique.
   Question: Which level do you confirm?
```

The user should be able to answer `1..., 2..., 3..., 4...` in one message.

## Small product changes

Mandatory interview does not imply a huge questionnaire. If only one or two product decisions exist, ask all of them in one tiny batch.

Example:

```text
I only see two decisions before I can do this:

1. Behavior: keep the current animation and only change the breakpoint? Recommendation: yes.
2. Effort: Standard (~15k-80k total-session envelope; likely far below the ceiling for this small task). Recommendation: Standard.

Confirm/correct both and I'll implement.
```

## Effort recommendation contract

Do not dump the levels as an unexplained menu. Recommend one based on marginal value and explain:

- why it fits;
- what lower/higher levels would change when relevant;
- rough total token envelope;
- likely research/specialist/iteration depth;
- what the user gains or gives up.

Do not recommend Studio simply because the task is design-related. Do not recommend Standard simply because it is cheaper.

The user must confirm the level before implementation. An explicit user instruction such as `Studio`, `go all out`, or `keep it Standard` counts when unambiguous.

## Restate + persistence gate

After the user answers the batch:

1. resolve contradictions or new ambiguity;
2. if genuinely new material questions appeared, ask one follow-up **batch containing all of them**;
3. otherwise restate the confirmed intent compactly;
4. persist the confirmed state according to `docs/PROJECT_CONTINUITY.md` before implementation.

For meaningful work, the restate should cover:

```text
Outcome: ...
Audience: ...
Success: ...
Constraints: ...
Out of scope: ...
Effort: Polished
Budget expectation: ~50k-250k total model tokens, rough/provider-dependent
```

Do not rely on the chat transcript as the only source of these decisions.

## Stop condition

Stop interviewing when:

- all currently material user decisions are answered;
- the effort level is confirmed;
- no known unanswered question is being intentionally deferred;
- further questions are unlikely to materially alter the chosen result.

For open-ended/high-cost tasks, ask yourself: `Can a fresh agent read the persisted intent and make the same major decisions without this chat?` If not, either ask the missing question now or document the remaining blocker explicitly.

## Mid-task escalation

If execution reveals that the confirmed level is no longer realistic, do not silently burn a much larger token budget.

Ask in one compact escalation batch containing every newly material decision:

```text
This turned out to be more coupled than expected.
- Staying Standard means: <tradeoff>.
- Moving to Polished likely adds roughly <token/time delta> and buys <specific benefit>.
Recommendation: Polished because <reason>.

I also need one newly exposed decision: <question + recommendation>.
Confirm both?
```

Correctness and safety are exceptions: do not knowingly ship unsafe/incorrect work merely to preserve a token budget. Explain the conflict and ask how to proceed when possible.

## Non-interactive contexts

Do not fake an interview in CI, scheduled jobs, autonomous loops, or contexts without a live user. If product-affecting work requires unresolved decisions or effort confirmation, surface it as a blocker instead of guessing.

## Interaction with other Agentit skills

- `idea-refine`: downstream of confirmed intent.
- `spec-driven-development`: writes the confirmed requirements.
- `planning-and-task-breakdown`: plans only after interview/effort selection.
- `architect-orchestrator`: maps the confirmed effort level to topology, specialists, and iteration depth.
- `source-driven-development`: discovers facts; do not ask the user for facts it can verify.
- `using-agentit`: enforces continuity documentation after the interview.

## Anti-patterns

- asking one known question per message when several material questions are already identifiable;
- deliberately withholding questions for a later round;
- starting product implementation before effort level is confirmed;
- bypassing interview because the product change looks easy;
- asking the user facts that tools/repo can answer;
- making every interview Studio-sized;
- recommending Studio by default for design;
- quoting token estimates as precise billing numbers;
- silently escalating from Standard into a multi-agent research marathon;
- treating `whatever you think` as effort confirmation when cost/quality tradeoffs are material;
- one enormous generic questionnaire containing irrelevant categories;
- using an interview for exact mechanical chores;
- completing the interview but failing to persist the decisions.

## Verification checklist

- [ ] Task classified as mechanical bypass or product-affecting.
- [ ] Product-affecting tasks ran an interview before planning/implementation.
- [ ] Agent inspected discoverable facts before questioning the user.
- [ ] All currently identifiable material questions were asked in the same batch.
- [ ] Every meaningful question included a recommendation/default.
- [ ] Standard / Polished / Studio recommendation included consequences and rough token estimates.
- [ ] User explicitly confirmed the effort level.
- [ ] Follow-up round happened only because answers exposed genuinely new material decisions.
- [ ] Confirmed intent was persisted before implementation for continuing work.
- [ ] Execution stayed within the confirmed effort level or asked before material escalation.
