---
name: interview-me
description: Confirm product intent and effort level before planning. Use for every product-affecting task; bypass only purely mechanical work with no product decision.
---

# Interview Me

## Core rule

For Agentit, **interview is the default entrypoint for product work**. If the task creates or changes a product, feature, page, workflow, architecture, API, UX, visual design, content, or other user-facing/engineering decision, interview before planning or implementation.

The only normal bypass is **purely mechanical execution** whose purpose is to save the user time and which does not require or encode a product decision: creating explicitly named directories/files, exact moves/renames, deterministic formatting, running an explicitly requested command/test, or copying exact content.

If you are unsure whether a task is mechanical or product-affecting, treat it as product-affecting and interview.

Canonical effort catalog: `effort/levels.yaml`.

## Why

The interview has two jobs:

1. discover what the user actually wants before implementation locks in assumptions;
2. agree how much work Agentit should spend: **Standard, Polished, or Studio**.

The goal is not maximum questioning. The goal is maximum alignment per question.

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

These are **rough total-session estimates, not guarantees**. Actual usage varies with task size, provider, model, context, retries, tool output, and whether multiple agents/models are used. Never present them as precise billing forecasts.

### How to ask

Do not dump the three levels as an unexplained menu. Recommend one based on the task and explain the consequence.

Example:

```text
EFFORT RECOMMENDATION: Polished
Why: this is public-facing and portfolio-worthy, but the concept is already fairly clear; Studio would mainly buy broader creative exploration and extra critique loops.

Expected result:
- Standard: clean and correct, limited exploration/polish.
- Polished: stronger craft, targeted research, better responsive/edge-case QA. <- recommended
- Studio: multiple concepts/specialists and much deeper iteration; probably overkill here.

Rough total model tokens:
- Standard: ~15k-80k
- Polished: ~50k-250k
- Studio: ~150k-800k+

Which level do you want?
```

If the task is tiny but product-affecting, the interview may be only this one short confirmation plus any truly material question.

## Interview depth is adaptive

The requirement to interview does **not** mean every task gets a deep discovery workshop.

- Clear small product change → 1 short question/confirmation may be enough.
- One unresolved material decision → ask that decision + effort level.
- Several independent decisions → one frontier round + effort recommendation.
- Open-ended product/design/architecture task → interview deeply until the important frontier is closed, then confirm effort.

Do not use Studio-style interview depth for a Standard task unless ambiguity itself requires it.

## Step 1: classify mechanical bypass vs product work

Ask internally:

> Am I only executing an exact mechanical instruction, or am I choosing/altering something about the product or its implementation tradeoffs?

Mechanical examples that may bypass interview:

- `mkdir src/components src/hooks`;
- rename `foo.ts` to `bar.ts` exactly as requested;
- run the test suite;
- format these files with the project's formatter;
- copy this exact configuration into the specified location.

Product-affecting examples that require interview even when apparently simple:

- build/change a page or component;
- change behavior, copy, navigation, states, or visual hierarchy;
- add an endpoint or data model;
- choose an architecture/library with meaningful consequences;
- create a feature, automation, workflow, or public artifact;
- redesign/refactor where multiple valid outcomes exist.

Never use the bypass merely because the task is easy.

## Step 2: hypothesize and measure confidence

State a one-sentence best read plus confidence when the intent is not already explicit:

```text
HYPOTHESIS: You want X because Y.
CONFIDENCE: ~60% — missing: audience and success criterion.
```

If the request is already highly specific, skip verbose hypothesis ceremony and move directly to the smallest useful confirmation.

## Step 3: work the decision frontier

Treat the problem as a decision tree. Ask only questions whose answers can change the result.

### Mode A — single question

Use when answers chain or only one decision remains.

```text
Q: <focused decision>
RECOMMENDATION: <your best default and why>
```

### Mode B — frontier round

Use when two or more independent decisions are simultaneously answerable. Batch only independent questions.

Each question must include a recommended/default answer. The user should react to a considered proposal, not fill out a survey.

Facts vs decisions:

- **Facts**: inspect repo/docs/tools/live sources yourself.
- **Decisions/preferences**: ask the user when they materially affect the outcome.

## Step 4: include the effort decision in the interview

As soon as you know enough about the task to make a useful recommendation, include the effort-level question in the same interview flow.

Your recommendation must say:

- recommended level and why;
- what the result will roughly look like at Standard / Polished / Studio when those alternatives are relevant;
- rough total token envelope;
- likely research/specialist/iteration depth;
- what the user gains or gives up by moving up/down.

Do not recommend Studio simply because the task is design-related. Do not recommend Standard simply because it is cheaper. Recommend by marginal value.

The user must confirm the level before implementation. An explicit request such as `Studio`, `go all out`, or `keep this cheap/standard` counts as confirmation if it is unambiguous.

## Step 5: listen for stated preference vs real preference

Probe vague sophistication words such as `modern`, `clean`, `scalable`, `premium`, or `best practice` when they are standing in for an actual goal.

A useful probe is:

> If you did not have to justify this choice to anyone, what would you actually want?

Use it only when the user's answer appears convention-driven; do not ask it ceremonially.

## Step 6: restate and confirm

For meaningful tasks, restate the agreed intent before implementation:

```text
Outcome: ...
User/audience: ...
Success: ...
Constraints: ...
Out of scope: ...
Effort: Polished
Budget expectation: ~50k-250k total model tokens, rough/provider-dependent
```

Get explicit confirmation. For a tiny clear product change, a concise confirmation such as `Standard, this exact behavior, no redesign — yes?` is enough.

## Stop condition

Stop interviewing when:

- the meaningful decision frontier is closed;
- the effort level is confirmed;
- further answers are unlikely to materially alter the chosen result.

For open-ended/high-cost tasks, use the stronger test: can you reasonably predict how the user would answer the next few material questions? If not, continue.

Do not keep interviewing just to reach an arbitrary question count.

## Mid-task escalation

If execution reveals that the confirmed level is no longer realistic, do not silently burn a much larger token budget.

Ask before materially exceeding it:

```text
This turned out to be more coupled than expected.
Staying Standard means: <tradeoff>.
Moving to Polished likely adds roughly <token/time delta> and buys <specific benefit>.
Recommendation: Polished because <reason>.
Which do you want?
```

Correctness and safety are exceptions: do not knowingly ship unsafe/incorrect work merely to preserve a token budget. Explain the conflict and ask how to proceed when possible.

## Non-interactive contexts

Do not fake an interview in CI, scheduled jobs, autonomous loops, or other contexts without a live user. If a product-affecting task requires unresolved decisions or effort confirmation, surface it as a blocker instead of guessing.

## Interaction with other Agentit skills

- `idea-refine`: downstream of confirmed intent.
- `spec-driven-development`: writes the confirmed intent/requirements.
- `planning-and-task-breakdown`: plans only after interview/effort selection.
- `architect-orchestrator`: maps the confirmed effort level to topology, specialists, and iteration depth.
- `source-driven-development`: discovers facts; do not ask the user for facts this skill can verify.

## Anti-patterns

- starting product implementation before effort level is confirmed;
- bypassing interview because the product change looks easy;
- asking the user facts that tools/repo can answer;
- making every interview Studio-sized;
- recommending Studio by default for design;
- quoting token estimates as precise billing numbers;
- silently escalating from Standard into a multi-agent research marathon;
- treating `whatever you think` as effort confirmation when cost/quality tradeoffs are material;
- asking dependent questions in one giant batch;
- using an interview for exact mechanical chores.

## Verification checklist

- [ ] Task classified as mechanical bypass or product-affecting.
- [ ] Product-affecting tasks ran an interview before planning/implementation.
- [ ] Questions targeted decisions, not discoverable facts.
- [ ] Each meaningful question included a recommendation/default.
- [ ] Standard / Polished / Studio recommendation was made with consequence and rough token estimate.
- [ ] User explicitly confirmed the effort level.
- [ ] Final restate captured outcome, constraints/non-goals, and effort level when the task was meaningful.
- [ ] Execution stayed within the spirit of the confirmed level or asked before material escalation.
