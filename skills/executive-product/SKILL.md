---
name: executive-product
description: Make executive product decisions about customer problems, roadmap, product-market fit, sequencing, make/buy and investment using evidence rather than feature voting.
---

# Executive Product

Use this skill for product strategy, roadmap prioritization, customer discovery, product-market fit, platform-versus-feature investment, make/buy decisions and high-level product trade-offs.

The core question is **which customer problem is worth solving now, why, and what evidence should earn the next investment?**

## Problem before solution

Establish:

- target user/customer;
- job/problem and current workaround;
- frequency/severity/urgency;
- evidence from behavior, usage, support, sales or research;
- business outcome tied to solving it;
- constraints/dependencies;
- riskiest assumption in the proposed solution.

A feature request is evidence of a request, not automatic evidence of the underlying problem or priority.

## Product-market fit signals

Use multiple signals rather than one vanity metric. Depending on the business, useful evidence includes:

- cohort retention that stabilizes rather than decays toward zero;
- repeat purchase / renewal;
- expansion or NRR;
- organic/referral pull;
- strong willingness-to-pay / low sales friction among best-fit customers;
- meaningful “very disappointed without it” survey results;
- high-frequency usage for products where frequency is expected;
- customer behavior that persists after incentives end.

The often-cited Sean Ellis `40% very disappointed` threshold can be a useful reference for some products, not a universal PMF certificate. Segment quality and retention behavior matter.

## Prioritization

Use a forcing function, not stakeholder volume.

Consider:

- customer impact / problem severity;
- strategic fit;
- revenue/retention/risk leverage;
- evidence strength;
- reach;
- effort and opportunity cost;
- dependencies;
- reversibility;
- learning value.

RICE, ICE or opportunity scoring can structure the conversation. Do not let a computed score hide weak assumptions or false precision.

## Cheapest evidence first

Before expensive implementation, ask what is the cheapest honest test of the riskiest assumption:

- customer interviews/observations;
- prototype/usability test;
- manual concierge process;
- landing/offer test;
- instrumentation/cohort analysis;
- limited rollout;
- technical spike.

The point is not to avoid building. It is to avoid paying full price to learn something that could have been disproved cheaply.

## Platform / infrastructure investment

Invest in platform/infrastructure when evidence shows it is constraining product velocity, reliability, economics, security or strategic options.

Do not build generalized infrastructure merely because it feels architecturally elegant. Name the blocked capabilities and expected leverage.

## Make / buy / partner

Evaluate:

- differentiation / strategic control;
- time to capability;
- integration and switching cost;
- data/IP/control requirements;
- reliability/security/compliance;
- total cost and maintenance burden;
- vendor roadmap/dependency risk.

Pair with `executive-strategy`, `executive-finance`, `executive-operations` or `executive-legal` when those dimensions can change the answer.

## Discovery cadence

Separate what users **say** from what they **do**. Continuous customer contact is valuable, but the right frequency depends on product/stage/team. Preserve raw evidence and synthesis separately when possible.

## Decision method

1. Define customer problem and desired business outcome.
2. Inspect behavioral and qualitative evidence.
3. Name the riskiest assumption.
4. Compare materially different solutions, including doing nothing/manual/buy.
5. Choose the cheapest evidence that can change the decision.
6. Sequence investment based on evidence and dependency.
7. Set adoption/retention/revenue/quality success signal and review point.
8. Kill, reshape or expand based on evidence rather than sunk cost.

Use `spec-driven-development` when a decided product direction needs explicit implementation requirements; this skill is for the executive judgment before/during that decision.

## Failure modes

Avoid:

- roadmap by loudest stakeholder;
- solution-first discovery;
- feature count as progress;
- PMF claims based only on signups/downloads;
- infrastructure investment with no demonstrated constraint;
- RICE/ICE scores with fabricated precision;
- continuing features that do not earn their maintenance cost;
- acquisition spend masking poor retention.

## Provenance

Original Agentit guidance materially informed by the product specialist design and product-decision heuristics in Sente Labs' OpenExecutive (Apache-2.0). See `THIRD_PARTY_NOTICES.md`.