---
name: adversarial-idea-review
description: Red-teams an early idea, product, feature, business model, strategy, or go-to-market direction before commitment. Use whenever exploring or refining a non-trivial idea and the useful question is not only "could this work?" but "how would customers, competitors, operations, economics, adoption, support, or reality make this fail?" Pair with idea-refine before converging. Do not use as a substitute for code/artifact review after implementation; use doubt-driven-development or code-review-and-quality there.
---

# Adversarial Idea Review

## Purpose

An idea is not ready because it sounds coherent.

This skill tries to **break the idea before reality does**.

The job is not to produce negativity, perform contrarian theatre, or prove the author wrong. The job is to expose the cheapest available failure modes while change is still cheap, then turn the surviving insight into stronger product, scope, positioning, contracts, operations, pricing, adoption, and validation gates.

For early product exploration, this skill is a mandatory companion to `idea-refine`. Divergence without adversarial pressure creates attractive stories. Adversarial pressure without synthesis creates paralysis. Use both.

## When to Use

Use this skill when any of the following is true:

- exploring a new product, feature, market, workflow, business model, pricing model, or distribution strategy;
- comparing materially different product directions;
- deciding whether an idea deserves a spec, prototype, pilot, or investment;
- defining an MVP/MVR, first customer, design partner, go-live, or rollout;
- a proposal depends on customers changing behavior;
- a proposal creates recurring support, implementation, operations, or integration burden;
- a competitor, incumbent, substitute, internal user, procurement team, operator, partner, or regulator could invalidate the idea;
- the idea sounds unusually exciting and the room is converging too quickly.

### Mandatory pairing with `idea-refine`

If `idea-refine` is running on a non-trivial concept, run `adversarial-idea-review` **before Phase 2 finishes convergence and before a Recommended Direction is allowed to stand**.

Do not red-team every raw brainstorm fragment. First reduce the space to the serious candidate directions, then attack those candidates hard enough to change the recommendation if necessary.

## When NOT to Use

Do not use this skill for:

- executing a plan whose direction is already decided and the user only wants implementation;
- mechanical edits, formatting, migrations, or file operations;
- reviewing a finished code diff or artifact (`doubt-driven-development`, `code-review-and-quality`);
- generic security threat modeling when security is the primary question (`security-and-hardening`, `app-security-gate`);
- factual verification that should come from authoritative sources (`source-driven-development`, `reference-intelligence`);
- trivial ideas whose downside is negligible and reversible.

## Core Rule

**Attack first. Defend second. Recommend last.**

Do not start by writing why the idea is good. That anchors the review around preservation.

A proper adversarial pass must be allowed to conclude:

- `KILL` — the idea should not proceed in this form;
- `PIVOT` — the problem is real but the proposed solution/market/model is wrong;
- `PROCEED_WITH_GATES` — promising, but only if named assumptions or operational gates are proven;
- `PROCEED` — survives the attack with no material unresolved blocker.

`PROCEED` is not the default.

## Evidence Discipline

Adversarial analysis becomes dangerous when vivid anecdotes are presented as facts.

Tag material claims internally using this hierarchy:

- **FACT** — directly supported by a reliable source, observed system behavior, customer data, or an explicit contract;
- **SIGNAL** — repeated reviews, interviews, market behavior, or indirect evidence that suggests a pattern but does not prove its prevalence;
- **ANECDOTE** — one review, one customer, one story, one incident;
- **HYPOTHESIS** — a reasoned but unvalidated belief;
- **ASSUMPTION** — something the idea currently requires to be true.

Rules:

1. Never turn an anecdote into a percentage or market-wide claim.
2. Never turn a vendor claim into neutral evidence without labeling the source.
3. Separate "competitor lacks X" from "we have verified competitor lacks X".
4. If a claim materially affects pricing, market size, legal exposure, reliability, or a kill decision and can be researched, verify it before treating it as FACT.
5. If verification is unavailable, keep the uncertainty visible and make validation part of the gate.

## Process

Copy this checklist when running the skill:

```text
Adversarial idea review:
- [ ] 0. FRAME — candidate, user, buyer, success, constraints
- [ ] 1. ATTACK MAP — who/what can kill it
- [ ] 2. FAILURE TIMELINE — meeting → pilot → week 2 → month 3 → scale
- [ ] 3. ECONOMICS — value, price anchor, services trap, support burden
- [ ] 4. ADOPTION — behavior change, shadow workflows, veto players
- [ ] 5. COMPETITION — incumbent/substitute/copycat attack
- [ ] 6. OPERATIONS — implementation, integration, reliability, support
- [ ] 7. MOAT — what is real vs copyable
- [ ] 8. KILL GATES — evidence that must exist before scaling
- [ ] 9. DEFENSE — change product/scope/contract/GTM, not rhetoric
- [ ] 10. VERDICT — KILL / PIVOT / PROCEED_WITH_GATES / PROCEED
```

### Step 0 — FRAME

State the candidate in a form an adversary can attack:

```text
CANDIDATE:
TARGET USER:
ECONOMIC BUYER:
CURRENT ALTERNATIVE:
PROMISED OUTCOME:
WHY THEY WOULD SWITCH:
WHAT WE MUST OPERATE OR SUPPORT:
KNOWN CONSTRAINTS:
```

If buyer and user are different, name both. Many ideas fail because the user loves the workflow while the buyer purchases something else.

Do not invent missing constraints. If they are discoverable from the project or sources, inspect them. If they remain unknown, classify them as assumptions and continue with explicit uncertainty rather than silently filling them in.

### Step 1 — ATTACK MAP

Create the strongest plausible attacks from the actors and forces that matter.

At minimum consider:

1. **Low-cost substitute** — spreadsheet, email, WhatsApp, manual labor, generic SaaS, incumbent module.
2. **Full-suite incumbent** — "we already do this plus everything else."
3. **Specialist competitor** — deeper workflow, references, integrations, support, distribution.
4. **Copycat/partner** — can the differentiating feature be copied inside a larger platform?
5. **Economic buyer/procurement** — price anchors, risk, vendor maturity, switching cost, SLA, legal/security questions.
6. **Actual operator/user** — shortcuts, resistance, time pressure, workarounds, offline behavior, bad inputs.
7. **Implementation reality** — dirty data, integrations, migration, hardware/network, training, ownership.
8. **Support reality** — what happens at the worst plausible moment and who is expected to respond?
9. **Unit economics** — where recurring human work destroys the software margin.
10. **Scale** — what breaks at 10 customers, 10 sites, 10x volume, or 10x integrations?

For each attack, write the opponent's strongest one-sentence argument. Do not write a straw man.

Example shape:

```text
ATTACK: "Your €400/month product competes with a €25/month incumbent add-on."
WHY IT COULD LAND: buyer cannot distinguish accounting inventory from floor execution.
EVIDENCE LEVEL: SIGNAL / HYPOTHESIS / FACT
WHAT WOULD MAKE US LOSE: generic demo, feature-list positioning, no quantified floor pain.
```

### Step 2 — FAILURE TIMELINE

Attack the idea at different moments. A product can win the demo and still die in week two.

Run this timeline unless the domain calls for another:

#### First meeting

- Why would the buyer dismiss us in five minutes?
- What price anchor makes us look absurd?
- What credibility question exposes us?
- What existing tool makes "another login" feel unnecessary?

#### Pilot / onboarding

- Which data is dirty?
- Which integration becomes the real project?
- Which stakeholder was not in discovery?
- What must be true on day one that demos normally fake?

#### Week 2

- What shadow workflow returns under pressure?
- What exception makes users bypass the product?
- What causes trust to collapse?
- What manual support task starts repeating?

#### Month 3

- What degrades after the launch team leaves?
- Which custom request becomes "obviously included"?
- Which operational burden was hidden inside the sale?
- Which metric reveals that the workflow never truly moved?

#### Scale

- Which dependency, SLA, integration, support channel, customization, or human review queue fails non-linearly?
- Are we still selling software, or have we become a services bureau?

### Step 3 — ECONOMICS

Do not ask only "what would customers pay?" Attack the economics from both sides.

Check:

- buyer's comparison price and why that comparison may be wrong;
- value created or cost/risk removed;
- setup/implementation burden;
- recurring support burden;
- integrations and custom work;
- usage-based third-party costs;
- hardware/network/partner responsibilities;
- gross-margin killers hidden in "AI", review queues, onboarding, imports, or bespoke workflows;
- expansion economics by location, seat, volume, module, or outcome;
- whether the pricing model creates adversarial customer behavior.

Name the **services trap** explicitly when relevant:

```text
low recurring fee
+ unlimited custom work
+ informal support
+ integrations
+ data cleanup
+ manual review
= consultancy disguised as SaaS
```

If the model only works when founders silently subsidize implementation/support, classify that as a material risk, not hustle.

### Step 4 — ADOPTION

Software fails when the real workflow does not move.

Identify:

- user whose behavior must change;
- veto player who can sabotage adoption;
- shadow system likely to remain (Excel, paper, WhatsApp, old POS, old ERP, personal notes);
- pressure condition under which users bypass the intended flow;
- exceptions the product must absorb without a support call;
- training or champion requirement;
- measurable signal that the old workflow is genuinely off.

Prefer acceptance criteria such as:

```text
old workflow disabled for scope X by date Y
variance/error rate below threshold Z
no shadow export/write activity above threshold N
named operator/champion signs off
```

over "users liked the demo".

### Step 5 — COMPETITION

For each relevant rival or substitute, answer:

```text
They beat us when:
We beat them when:
They will attack us by saying:
Our one-sentence truthful response:
Deal we should walk away from:
```

Be willing to concede segments.

A strong strategy includes sentences such as:

> If the buyer needs X, competitor Y is the better fit and we should not pursue the deal.

Trying to win every comparison is not strategy.

### Step 6 — OPERATIONS

Attack the implementation and support model as if you were the customer relying on it during the worst normal day.

Check:

- migration/cutover;
- data ownership/export;
- offline/degraded mode;
- observability/status communication;
- error recovery and restartability;
- human review queues;
- integration ownership/source of truth;
- hardware/network boundaries;
- support channels and support hours;
- severity definitions;
- hypercare duration;
- what explicitly is **not** included in recurring support;
- what becomes a paid change request;
- conditions under which 24/7 or stronger SLA becomes economically supportable.

The defense must be a product, process, contract, partner, or scope decision. "We will work very hard" is not a defense.

### Step 7 — MOAT

Separate features from defensibility.

Classify each claimed differentiator:

- **commodity** — expected capability;
- **copyable feature** — useful wedge, not moat;
- **workflow advantage** — integrated sequence that is harder to copy well;
- **data advantage** — improves with proprietary/useful accumulated data;
- **distribution advantage** — channel, partner, community, reputation, installed base;
- **implementation advantage** — repeatable time-to-value / vertical defaults / migration playbook;
- **ecosystem advantage** — surrounding products/integrations create compounding value;
- **reference advantage** — public evidence with measured outcomes.

Do not call a feature a moat merely because incumbents have not built it yet.

If the moat currently depends on future customers, data, references, or ecosystem, say:

```text
MOAT STATUS: hypothetical until <evidence>
```

### Step 8 — KILL GATES

Every promising idea needs evidence that can kill or materially change it.

Define 3–7 gates. Examples:

- a design partner pays rather than accepting a free pilot;
- the real operator, not only the executive buyer, adopts the workflow;
- old system/Excel is turned off for a bounded scope;
- support load stays under a measurable threshold;
- implementation completes inside a target duration;
- gross margin survives real third-party/API/manual costs;
- users obtain the promised outcome with dirty real-world inputs;
- the integration/source-of-truth model survives reconciliation;
- a customer will act as a reference with measured outcomes.

A gate must be falsifiable. "Customer feedback is positive" is not a gate.

### Step 9 — DEFENSE

Only after the attacks are explicit, design defenses.

Defenses should preferentially change reality:

1. product behavior;
2. scope/non-goals;
3. implementation sequence;
4. validation/pilot contract;
5. support/SLA boundary;
6. pricing/metering;
7. integration ownership;
8. positioning/GTM;
9. partner model;
10. roadmap order.

Do not answer a product weakness with copy unless the weakness is genuinely only positioning.

For each material attack:

```text
ATTACK:
DEFENSE:
RESIDUAL RISK:
VALIDATION:
```

### Step 10 — VERDICT

Return a compact decision block:

```text
VERDICT: KILL | PIVOT | PROCEED_WITH_GATES | PROCEED

WHY:
- ...

TOP 3 WAYS THIS DIES:
1. ...
2. ...
3. ...

WHAT MUST BE TRUE:
- ...

WHAT WE SHOULD NOT BUILD / PROMISE:
- ...

NEXT CHEAPEST TEST:
- ...
```

If paired with `idea-refine`, feed this verdict back into convergence. The final Recommended Direction must incorporate the attacks and defenses; it must not append the red-team as an ignored disclaimer.

## Software/Product-Specific Add-on: Minimum Viable Replacement

When the idea replaces an existing operational workflow, prefer **Minimum Viable Replacement** over a demo-shaped MVP.

Ask:

> What is the smallest bounded scope in which the user can stop using the old workflow without creating an operational hole?

Then define:

- what must be true on cutover day;
- which exceptions must work;
- which old workflow is actually switched off;
- which capabilities are explicitly deferred;
- how rollback/recovery works;
- what evidence proves the replacement is real.

A beautiful demo that cannot replace a bounded real workflow is not a viable replacement.

## Output Quality Bar

A strong adversarial review should contain uncomfortable, decision-changing content.

It should make at least one of these happen when warranted:

- remove scope;
- change sequencing;
- change target customer;
- add a kill criterion;
- add a contractual/support boundary;
- change pricing assumptions;
- change integration ownership;
- concede a competitor segment;
- expose a fake moat;
- identify a design partner requirement;
- stop the idea entirely.

If the review ends with the exact plan it started with and only adds generic risks, assume the attack was too weak and run it again.

## Anti-Patterns

- **Red-team theatre:** dramatic language, no decision-changing attack.
- **Straw-man competitors:** attacking weaker versions of real alternatives.
- **Founder heroics as architecture:** treating unlimited availability/manual work as a plan.
- **Feature moat:** calling a copyable feature defensibility.
- **Anecdote laundering:** presenting one review as a market statistic.
- **Vendor-claim laundering:** presenting marketing claims as neutral evidence.
- **Support hand-wave:** "we'll handle it" without channel, hours, severity, or ownership.
- **Pilot-as-free-R&D:** customer extracts discovery/custom workflow without payment/reference/validation value.
- **MVP-as-demo:** shipping a visually convincing subset that cannot replace any real bounded workflow.
- **Infinite ICP:** refusing to say which customers should choose a competitor instead.
- **Critique without defense:** finding problems but not converting them into product/scope/contract/GTM changes.
- **Defense before attack:** rationalizing the current plan instead of testing it.

## Interaction with Other Skills

- **`idea-refine`** — mandatory partner for non-trivial ideation. It expands and converges; this skill tries to kill the serious candidates before convergence stands.
- **`interview-me`** — use first when target user, buyer, success criteria, or constraints are genuinely unknowable from available context.
- **`reference-intelligence` / `source-driven-development`** — use to verify claims that materially affect the attack or verdict.
- **`executive-strategy` / `executive-product`** — use when the idea has company-level portfolio, capital-allocation, market-entry, or product-strategy consequences.
- **`doubt-driven-development`** — later-stage adversarial review of a concrete decision/artifact; distinct from attacking an early idea/business model.
- **`spec-driven-development`** — only after the idea has survived enough attack to deserve precise requirements.

## Verification

Before the review is complete:

- [ ] Serious candidate directions were attacked before a recommendation stood
- [ ] Buyer, user, incumbent/substitute, operator, implementation, support, economics, and scale were considered where relevant
- [ ] At least one failure timeline beyond the demo/first meeting was explored
- [ ] FACT / SIGNAL / ANECDOTE / HYPOTHESIS / ASSUMPTION were not silently mixed
- [ ] The strongest competitor/substitute argument was stated without straw-manning
- [ ] At least one explicit deal/segment to walk away from was identified when relevant
- [ ] Services/support burden was tested for hidden margin destruction
- [ ] Claimed moat was separated from copyable features
- [ ] 3–7 falsifiable kill/validation gates were defined for material uncertainty
- [ ] Defenses changed product, scope, contract, operations, pricing, or GTM rather than merely changing rhetoric
- [ ] A bounded verdict was produced
- [ ] If paired with `idea-refine`, the final Recommended Direction incorporated the red-team findings rather than ignoring them
