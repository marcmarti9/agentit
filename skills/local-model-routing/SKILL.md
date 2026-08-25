---
name: local-model-routing
description: Select and route work across compatible local or remote models by observed capability, task fit, tools, context, reliability, privacy, latency and cost. Use when model choice materially affects execution quality or efficiency.
---

# Compatible model routing

> The skill ID is retained as `local-model-routing` for compatibility. Its policy applies to **local and remote compatible models**.

Agentit does not have a preferred model brand. Model names are observations and endpoint identities, not architectural dependencies.

A general Agentit skill or workflow may be executed by any compatible model that can receive the required instructions/context and satisfy the task's tool, modality, permission and verification requirements.

Provider/model names may appear when they are genuinely needed for:

- a provider-specific adapter or API contract;
- machine-local endpoint configuration;
- an example configuration;
- a current benchmark/evaluation observation;
- source provenance.

They must **not** be promoted from a source article or benchmark into a general rule such as “use Claude”, “use Kimi”, “use Codex”, or “model X is always best”.

Canonical capability catalog: `models/capabilities.yaml`.

## Capability roles

Agentit uses semantic capability roles rather than vendor rankings:

| Tier | Typical roles |
|---|---|
| judgment | architecture, difficult trade-offs, arbitration |
| coding | primary implementation, multi-file integration |
| fast | bounded workers, extraction, variants, repetitive QA |
| critic | independent review / adversarial judgment |

These tiers describe **what an endpoint has demonstrated it can do**, not prestige or price.

## Model-selection contract

When model choice materially matters, define the role before selecting an endpoint.

```text
ROLE CONTRACT
objective:
required quality / acceptance criteria:
required tools / function calling:
required context:
required modalities:
privacy / locality constraints:
latency sensitivity:
cost sensitivity:
risk / consequence of failure:
independence requirement:
```

Then inspect the compatible endpoints actually available.

A model is a candidate only if it can satisfy the hard requirements. Among candidates, choose based on evidence relevant to the actual task rather than a universal leaderboard.

## Evidence hierarchy for routing

Use evidence in roughly this order when available:

1. **Task/project verifier evidence** from representative work in the real harness.
2. **Small machine/provider capability probes** for tools, context, modalities and reliability.
3. **Current official model/provider documentation** for hard capabilities and limits.
4. **Representative external benchmarks** as priors about likely strengths.
5. **Anecdotes/social comparisons** as hypotheses worth testing, not routing law.

A public benchmark is useful evidence about the benchmark. It is not proof that one model is universally better for the user's repository, prompt harness, tools or workload.

## Representative head-to-head evaluation

If two or more plausible endpoints exist and the choice has meaningful quality/cost/latency consequences, prefer a small representative comparison instead of debating brands from memory.

### 1. Build representative tasks

Choose tasks that resemble the real workload:

- repo bug fix;
- frontend implementation from a reference;
- MCP/tool sequence;
- long-context synthesis;
- research task;
- visual judgment task;
- whatever the actual role requires.

Do not benchmark only the task a preferred model is known to win.

### 2. Keep the harness comparable

Where technically possible keep constant:

- task instructions;
- tool access and permissions;
- relevant context/files;
- stopping conditions;
- verifier;
- retry policy.

Record material differences when providers require different harness behavior.

### 3. Prefer objective verification

Use executable or inspectable acceptance criteria first:

- tests/build/verifier pass;
- required artifact produced;
- correct tool calls;
- factual checks;
- browser/runtime behavior;
- task-specific rubric with observable criteria.

For subjective quality, use an independent reviewer when useful. Reduce judge bias by hiding model identity and swapping answer order when practical. Repeat trials when variance is material.

### 4. Measure useful system metrics

Do not optimize only raw model price or one benchmark score. Useful measures can include:

```text
accepted task success
success without human rescue
correct tool-use rate
refusal / truncation / malformed-output rate
latency median / tail latency
input + output tokens
cost per attempt
cost per ACCEPTED result
number of retries
context pressure
```

A cheap model that requires four retries can be more expensive than a stronger first-pass model. A slower high-quality model can still be wrong for an interactive worker. Measure the system outcome.

### 5. Keep insufficient evidence explicit

If the comparison is noisy or too small, say so.

Do not manufacture a winner from:

- one cherry-picked task;
- one subjective screenshot;
- one judge with obvious position/style bias;
- a provider's own benchmark alone;
- a social post without the underlying setup.

Use `insufficient evidence` or keep the current safe default until better evidence exists.

## Dynamic routing

Different roles in the same Agentit graph may use different models.

Example:

```text
primary implementation -> endpoint A
fast extraction workers -> endpoint B
visual alternative -> endpoint C
independent critic -> endpoint D
```

This is allowed because Agentit owns the **protocol**, not the model brand.

Prefer a genuinely independent model family for critic vs writer when useful and affordable, but do not force diversity when it materially reduces competence or violates constraints.

## Local models

Local models remain first-class when they meet the role contract.

Example preference shape:

```yaml
local_models:
  enabled: true
  endpoints:
    - id: local-coding
      base_url: http://127.0.0.1:11434/v1
      model: <configured-model>
      tier: coding
      tools: true
      context_tokens: 32768
```

Before relying on a local endpoint, check on the current machine:

- required tool/function calling actually works;
- projected context fits;
- a small representative probe succeeds;
- latency is acceptable;
- required modalities exist.

Do not assume OpenAI-compatible HTTP syntax implies feature parity.

## Re-evaluation triggers

Model routing can become stale quickly. Re-evaluate a material route when:

- model/version changes;
- provider/harness/tool-calling behavior changes;
- task distribution changes;
- context requirements change;
- price/latency constraints materially change;
- repeated verifier failures contradict the stored assumption.

Persist durable routing learnings with scope, evidence and date. Do not turn yesterday's winner into a permanent universal rule.

## Provenance: Ori Silver Kimi K3 vs Fable 5 bookmark

Bookmarked source reviewed 2026-08-25:

- https://x.com/OriSilver/status/2092225524210827424 — creator head-to-head comparison of Kimi K3 and Fable 5 whose surprising result is useful as a **prompt to evaluate model/task fit**, not as authoritative proof of a universal winner.

Corroborating context inspected:

- Moonshot's Kimi K3 evaluation table compares Kimi K3 with several frontier models and shows different leaders across different benchmarks.
- External/provider benchmark work comparing Kimi K3 and Fable 5 demonstrates the usefulness of workload routing, but provider-published accuracy/cost claims remain vendor evidence rather than universal truth.

The durable lesson Agentit carries forward is:

> **Benchmark models for the role you actually need, in the harness you actually use, and route by accepted outcomes rather than brand loyalty.**

## Anti-patterns

- hard-code one vendor/model as the Agentit default for all work;
- convert a Claude/Fable/Kimi/Codex-specific source example into a general requirement;
- “local always” regardless of demonstrated capability;
- send high-consequence arbitration to an unproven weak model silently;
- pick a model from leaderboard rank without checking tools/context/task fit;
- optimize nominal token price instead of cost per accepted result;
- route from a single anecdotal head-to-head;
- declare one model universally best from a small benchmark;
- assume a provider-compatible API means behavioral/tool parity;
- keep a stale route after model/harness changes.

## Completion check

Before relying on a material model route, be able to answer:

```text
What role are we selecting for?
What are the hard compatibility requirements?
What evidence supports this endpoint for this workload?
What verifier measures success?
What are the latency/cost/privacy trade-offs?
Is the evidence strong enough to prefer it, or should the result remain uncertain?
When should this routing assumption be re-tested?
```
