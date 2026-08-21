---
name: task-router
description: AI-native Agentit task-decision protocol. The primary model owns semantic classification and strategy; a cheap second model only audits the decision, with strong-model escalation for high risk or unresolved disagreement.
---

# AI-native task decision protocol

Agentit has **no programmatic semantic router**.

Do not call Python, regexes, keyword tables, scoring code, decision validators or any other deterministic classifier to work out what the user means. The active primary model has the richest task context and owns the semantic decision.

The purpose of this skill is not to route the model. It gives the primary model a mandatory, repeatable decision framework and adds independent AI auditing without handing decision ownership to a weaker model.

## 1. Inspect before deciding

Use all materially available context:

- exact current request;
- relevant earlier conversation;
- repository/project state;
- files and docs already inspected;
- user and project instructions;
- available tools/capabilities;
- known environment and deployment state;
- unresolved assumptions.

A follow-up such as “fix it” must be interpreted from context, not from those two words.

## 2. The primary model owns `TASK_DECISION`

The model currently responsible for the task is the **decision owner**. Do not delegate semantic classification or execution strategy to a cheaper reviewer merely to save tokens.

Before executing material work, the primary model determines at least:

- `intent`: what outcome the user is actually asking for;
- `known_facts`: evidence already established;
- `unknowns`: assumptions that could materially change the plan;
- `category/domain_pack`: engineering, frontend, design, backend, data, product, writing, release, research, etc.;
- `complexity`: trivial, bounded, substantial, structural;
- `risk`: `RISK_0..RISK_4` with reasoning;
- `reversibility`: how easily the action can be undone;
- `external_effects`: production, network, account, financial, data or other side effects;
- `skills`: smallest useful knowledge bodies to load;
- `tools`: only tools that materially help;
- `topology`: `direct`, `probe`, `fan_out`, `pipeline`, `writer_reviewer` or `audit`;
- `workers`: useful specialist roles, if any;
- `parallelism`: why concurrent work is or is not useful;
- `plan`: concrete execution stages;
- `verification`: evidence needed before claiming success;
- `safety`: backup/rollback/dry-run/post-check requirements when applicable.

The primary model may keep this structure internal when showing it would add noise, but it must actually make the decision.

Use the **same rubric**, not the same answer. Context can legitimately change the classification.

## 3. Risk rubric

`RISK_0` — read-only explanation, research or inspection with no meaningful mutation.

`RISK_1` — local, small, clearly reversible mutation with negligible blast radius.

`RISK_2` — meaningful but bounded implementation/product change.

`RISK_3` — auth/security, payments, secrets, PII, significant data/schema work, infrastructure, external side effects, or another boundary where a bad decision has serious consequences.

`RISK_4` — destructive production action, plausible data loss, irreversible/high-blast-radius operation, or comparable consequence.

An explicit safety/risk requirement can raise the floor; confidence does not lower it.

## 4. Topology rubric

`direct` — one execution owner is clearer and delegation adds no concrete benefit.

`probe` — investigate/read first, then decide.

`fan_out` — two or more genuinely independent branches benefit from isolation or parallel work.

`pipeline` — dependent stages with explicit handoffs.

`writer_reviewer` — one implementation owner plus independent review.

`audit` — inspection/critique is the primary task.

Do not force multi-agent because a task is large. Do not force single-agent because one strong model could technically do everything. Delegate when independence, specialization, context isolation, breadth, latency or fresh judgment actually helps.

## 5. Mandatory cheap-model audit

Before the primary model executes material changes, send the proposed `TASK_DECISION` to an independent read-only audit model.

For ordinary tasks choose the **cheapest model that is competent to audit the bounded proposal**, typically semantic tier `fast`. When practical and similarly cheap, prefer a different model family from the primary model.

This model is a **critic, not a router and not a decision owner**. It must not replace the primary model's classification, assign an authoritative alternative category/risk/topology, or silently rewrite the plan. Its job is to find reasons the primary should reconsider or escalate.

Give it:

- exact user request and material constraints;
- relevant facts already established;
- proposed `TASK_DECISION`;
- this protocol or the bounded rules needed to audit it.

Use the detailed contract in `references/economy-reviewer.md`.

The audit returns:

```text
AUDIT: CLEAR | CHALLENGE | ESCALATE
FINDINGS:
- ...
SUGGESTED_CHECKS:
- ...
CONFIDENCE: low | medium | high
```

It must actively look for:

- misunderstood intent;
- risk possibly classified too low;
- missing production/auth/payment/PII/destructive implications;
- unjustified assumptions;
- wrong or excessive skills/tools;
- missing useful delegation or pointless delegation;
- unsafe parallel writers/shared state;
- dependency mistakes;
- weak verification;
- missing rollback/backup/post-check;
- a plan shaped by prompt words rather than the actual problem.

`CLEAR` means the auditor found no material objection. It is not a correctness guarantee.

`CHALLENGE` means the primary model must reconsider the findings. The primary remains the decision owner: it may revise the decision or retain it with an explicit reason grounded in evidence. If material disagreement remains after reconsideration, escalate instead of letting the cheap model arbitrate.

`ESCALATE` means the auditor found uncertainty or consequence that deserves a stronger independent model. Do not let the cheap model resolve that dispute itself.

Ordinary audit/reconsideration is bounded to two cycles. If disagreement still matters, escalate to a stronger critic or surface the uncertainty rather than looping.

## 6. Strong-model arbitration

A cheap auditor is useful for catching omissions, but it is not trusted as the final judge when consequences or disagreement are substantial.

Use an independent `critic`/`judgment` tier model when:

- `RISK_3` or `RISK_4`;
- the cheap auditor returns `ESCALATE`;
- a material `CHALLENGE` remains unresolved after primary reconsideration;
- destructive or hard-to-reverse data work is involved;
- auth, payments, secrets, PII or production migrations are involved;
- a large structural architecture/product plan is about to be committed to;
- another explicit safety boundary requires stronger judgment.

The strong critic reviews the primary decision plus the cheap auditor's findings. It does not become the implementation owner, but for these cases it acts as the **independent judgment gate**: material execution waits until critical objections are resolved, the plan is revised, or required user input is obtained.

For destructive data operations require verified backup, rollback plan and post-check. For `RISK_4`, use a preview/dry-run whenever technically meaningful.

For high-ambition public visual work, use independent design critique plus browser/rendered evidence.

If a separate model cannot be spawned, use an isolated fresh context with the same bounded audit contract when possible. For high-risk work, do not pretend a same-context self-review is equivalent to independent judgment; record the limitation and take the conservative path or request the missing review/user decision.

## 7. Skills are chosen by the primary AI

Profiles and metadata are knowledge inventories, not a classifier.

The primary model decides which skills are relevant after inspecting the actual task. Neither the cheap auditor nor a script owns this selection. The auditor may challenge an obviously missing or excessive skill choice, but the primary model resolves it.

A skill is not “used” merely because its ID appears somewhere: the stage model must read its `SKILL.md` or receive provider-native injection of the same body.

Choose the smallest useful set. Domain-specific guidance requires real evidence that the domain applies. For example, PostgreSQL-specific guidance needs actual PostgreSQL/psql/Supabase context, not the word “database” alone.

## 8. Public visual surfaces

A landing page, homepage, brand/company website, portfolio, storefront, campaign site or total visual redesign is design-primary even if the implementation language is React/CSS/etc.

Greenfield or total public redesign normally follows:

`interview -> live reference research -> direction/concept -> implementation -> independent visual critique -> desktop/mobile browser verification`

Do not reduce a design problem to a frontend keyword.

## 9. What remains deterministic

Mechanical programs may still copy files, manage manifests, run tests, persist state or execute explicitly chosen tooling. They must not interpret natural-language intent or decide the semantic task plan.

The boundary is:

> **Primary AI decides; cheap AI audits; strong AI arbitrates when needed; software performs mechanical operations afterward.**

## Non-goals

- no `route.py`;
- no semantic `decision_contract.py`;
- no regex/keyword risk inference;
- no executable router evals pretending to benchmark language understanding;
- no script that chooses category/topology/skills from prompt text;
- no cheap model acting as the semantic decision owner;
- no cheap-model disagreement being treated as authoritative arbitration;
- no blind trust in one model when a cheap second opinion is available;
- no safety downgrade because any model sounds confident.