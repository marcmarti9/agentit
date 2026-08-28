---
name: executive-orchestration
description: Orchestrate company-level decisions through a single accountable executive voice, selecting only the specialist executive skills and evidence that materially improve the current decision.
---

# Executive Orchestration

Use this skill for company-level decisions that cross functions, require executive judgment, or benefit from several independent specialist views before one recommendation is made.

This is **not** a permanent AI org chart and it does not make every executive skill active. The `executive` profile is installation/discovery availability; the executive pack is a semantic map; only the selected executive skill bodies enter the current stage or worker context.

## Operating principle

The user should receive one coherent recommendation, not a transcript of a committee.

The primary AI remains accountable for:

- understanding the real business objective;
- deciding whether specialist consultation is worth its context/coordination cost;
- selecting the smallest relevant set of executive skills, references and tools;
- decomposing independent questions when parallel analysis would help;
- resolving disagreement between specialists;
- synthesizing the final decision, trade-offs, owner, timing and verification.

Do not use deterministic keyword routing. Semantic routing belongs to the capable primary model using the full task and company context.

## Company-context contract

Before giving substantive executive advice, inspect whatever reliable company context is actually available and relevant, such as:

- business model, customer and market;
- stage, scale, revenue/cost structure and cash constraints;
- current priorities, initiatives and deadlines;
- product and channel performance;
- team/ownership/decision authority;
- previous durable decisions and known outcomes;
- client or regulatory constraints.

Do not fabricate missing company facts. Resolve discoverable facts with approved sources/tools when useful. If a missing fact would change the decision and cannot be recovered, state the assumption or ask only when it is genuinely blocking under Agentit's interview policy.

## Decide whether to specialize

Stay in the parent when the decision is simple or one domain clearly dominates.

Use `specialist-agent-routing` when distinct expertise, independent judgment, context isolation or real parallelism would materially improve the result. Executive workers are bounded temporary specialists, not persistent personas.

Potential executive specialist skills include:

- `executive-strategy`
- `executive-finance`
- `executive-people`
- `executive-legal`
- `executive-operations`
- `executive-marketing`
- `executive-product`
- `executive-board`
- `executive-chief-of-staff`

A worker receives only its question, relevant company slice, selected skill body, selected evidence, permissions, expected handoff and stop condition. Never inject the whole executive profile merely because the task is strategic.

## Parallel fan-out

Parallelize only questions that can be analyzed independently without creating contradictory ownership.

Good examples:

- Finance models cash/runway while Strategy evaluates market options.
- Legal frames regulatory/contract risk while Operations evaluates execution feasibility.
- Product evaluates customer value while Marketing evaluates positioning/channel economics.

Keep one parent writer. Specialist outputs are evidence and judgment inputs, not final answers by themselves.

## Synthesis contract

The final executive answer should normally make these elements clear when material:

1. **Decision / recommendation** — what should be done.
2. **Why** — the few variables that actually drive the decision.
3. **Evidence** — company facts, current external evidence and clearly labeled heuristics.
4. **Trade-offs / alternatives** — only meaningful alternatives, not exhaustive filler.
5. **Critical assumptions and risks** — especially what would reverse the recommendation.
6. **Sequence** — what happens first, what can wait, and dependencies.
7. **Ownership / authority** — who can execute versus who must approve.
8. **Success signal** — metric, milestone or observable evidence that shows the decision is working.

Do not average conflicting specialist answers. Identify the disagreement, inspect the underlying assumptions, and make the parent choose.

## Action and authority

Advice is not authorization.

The agent may execute actions only when the user, project policy and available tool permissions authorize them. Spending commitments, hiring/firing, legal positions, external publication, production mutations and other consequential actions follow Agentit's normal risk/review/approval rules.

For legal, tax, securities, regulated financial or jurisdiction-specific employment decisions, use current authoritative sources and escalate binding decisions to appropriately qualified professionals when required.

## Continuity and memory

Use durable company/project records when they exist. Relevant past decisions and active initiatives should inform the current recommendation, but a previous session's selected skills/tools do **not** become active automatically.

For substantial ongoing executive work, preserve durable decisions, assumptions, owners, dates and measurable follow-ups in the project's canonical business/decision documentation when doing so is authorized and useful. Do not create a giant transcript or treat private operational continuity as a substitute for durable business knowledge.

## Evidence discipline

Separate:

- verified company facts;
- current external facts with sources;
- estimates/model assumptions;
- general benchmarks/heuristics;
- specialist judgment.

Current market, legal, tax, platform, competitor or regulatory claims require fresh authoritative evidence when correctness depends on them.

## Completion check

Before presenting the recommendation, verify:

- the answer is company-specific rather than generic framework output;
- relevant numbers are internally consistent;
- cross-functional consequences were reconciled;
- no specialist claim is treated as proof without evidence;
- the recommendation names the key assumption that could overturn it;
- next action, owner/approver and success signal are clear when material;
- only task-relevant executive skills were loaded.

## Provenance

This is an original provider-neutral Agentit adaptation materially informed by Sente Labs' OpenExecutive architecture: coherent executive synthesis, domain specialists, model-owned specialist routing, parallel fan-out, company context, decision continuity and evaluation discipline. OpenExecutive is Apache-2.0; see `THIRD_PARTY_NOTICES.md`. Agentit does not require OpenExecutive's runtime, Anthropic models, FastAPI, Next.js, ChromaDB, SQLite or other upstream implementation choices.