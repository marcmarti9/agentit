---
name: executive-finance
description: Turn company financial data, unit economics, cash constraints and investment choices into explicit scenarios and executive decisions without pretending heuristics are universal rules.
---

# Executive Finance

Use this skill for cash/runway, budgeting, pricing economics, unit economics, profitability, capital allocation, fundraising framing, ROI and financial trade-offs.

The job is not to recite finance concepts. The job is to **anchor the decision to the numbers and make the trade-off explicit**.

## Establish the financial model

Use reliable company data where available. Depending on the question, inspect:

- revenue and growth by product/channel/customer segment;
- gross margin and contribution margin;
- fixed and variable operating costs;
- cash balance, burn and working-capital needs;
- receivables/payables/inventory timing;
- CAC, retention, expansion, LTV and payback where meaningful;
- pricing, discounts, commissions and marketplace/platform fees;
- headcount and vendor commitments;
- debt, tax or financing constraints;
- expected cost, benefit, timing and downside of the proposed action.

Do not invent missing financials. Derive only what the inputs support and label assumptions.

## Scenario discipline

For consequential decisions, model materially different cases rather than hiding uncertainty in one point estimate:

- base case;
- downside / stress case;
- upside case when it changes the decision.

Show the assumptions that drive each scenario. Prefer a simple transparent model over false precision.

## Useful heuristics

These are starting points, not universal acceptance criteria. Re-check industry/stage/channel context before applying them.

- LTV:CAC around `3:1` is often treated as a healthy SaaS reference point; the components and cash timing matter more than the ratio alone.
- SaaS CAC payback below roughly 12 months is commonly strong, while longer periods demand confidence in retention and financing capacity.
- Burn multiple, Rule of 40, NRR and gross-margin benchmarks can be useful for recurring-revenue companies but are often meaningless for different business models.
- Runway should be evaluated against the time needed to reach the next credible milestone **plus financing/process risk**, not a magical month count.
- A profitable channel on gross margin can still destroy cash through returns, payment timing, inventory, commissions or support burden.
- The right ROI denominator is the real incremental cash/resources committed, including implementation and maintenance, not only the vendor invoice.

If a benchmark is central to the recommendation, use current authoritative/credible comparable evidence rather than relying on a remembered threshold.

## Decision method

1. Define the decision and financial constraint.
2. Build the smallest model that can change the answer.
3. Separate historical facts from forecasts and assumptions.
4. Identify the dominant economic lever or bottleneck.
5. Compare scenarios and opportunity cost.
6. Stress the downside and liquidity impact.
7. Recommend the action, maximum acceptable exposure and revisit trigger.
8. State what data should be measured next.

## Capital allocation

Evaluate spend against:

- expected incremental contribution/cash flow;
- time to impact and payback;
- confidence/evidence quality;
- strategic option value;
- reversibility;
- opportunity cost;
- liquidity/runway impact;
- ongoing support/maintenance burden.

Do not optimize percentage ROI while ignoring absolute impact, or absolute growth while ignoring survival.

## Pairing with other executive skills

Use other specialists only when they can materially change the financial conclusion:

- `executive-strategy` for strategic value/options;
- `executive-marketing` for funnel/channel assumptions;
- `executive-product` for adoption/retention assumptions;
- `executive-operations` for implementation and working-capital reality;
- `executive-legal` for financing, contractual, tax or regulatory boundaries.

## High-stakes boundary

For specific tax treatment, securities rules, regulated financial activity, legal structure or binding accounting treatment, use current jurisdiction-appropriate authoritative sources and qualified professional review where required. This skill provides executive financial framing; it does not manufacture professional sign-off.

## Output contract

Return the decision with:

- key financial facts;
- assumptions;
- scenario table/model when useful;
- cash/runway or margin impact;
- recommendation and exposure limit;
- sensitivity / what would reverse the decision;
- metric and date/event for review.

## Failure modes

Avoid:

- vanity revenue without margin/cash analysis;
- historical averages masking cohort/channel differences;
- LTV models built on immature retention;
- ROI that excludes implementation/maintenance cost;
- confusing accounting profit with cash availability;
- generic startup benchmarks applied to unrelated businesses;
- financial precision unsupported by input quality.

## Provenance

Original Agentit guidance materially informed by the finance specialist design and decision heuristics in Sente Labs' OpenExecutive (Apache-2.0). See `THIRD_PARTY_NOTICES.md`. Agentit remains provider-neutral and does not inherit OpenExecutive's model configuration.