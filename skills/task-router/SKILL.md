---
name: task-router
description: AI-native Agentit task-decision protocol. The primary model classifies from full context and a second model reviews the decision before execution.
---

# AI-native task decision protocol

Agentit has **no programmatic semantic router**.

Do not call Python, regexes, keyword tables, scoring code, decision validators or any other deterministic classifier to work out what the user means. The active model already has richer context than a standalone script and owns the semantic decision.

The purpose of this skill is not to route the model. It gives the model a mandatory, repeatable thinking framework and a second-model review loop.

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

## 2. Primary model creates `TASK_DECISION`

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

The model may keep this structure internal when showing it would add noise, but it must actually make the decision.

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

## 5. Mandatory second-model preflight review

Before the primary model executes material changes, send its `TASK_DECISION` to an independent reviewer.

For ordinary tasks choose the **cheapest capable model/endpoint available**. Prefer semantic tier `fast`; when practical and similarly cheap, prefer a different model family from the primary model.

This reviewer is read-only. It does not execute the task and does not need broad tool access.

Give it:

- exact user request and material constraints;
- relevant facts already established;
- proposed `TASK_DECISION`;
- this protocol or the bounded rules needed to judge it.

Use the detailed contract in `references/economy-reviewer.md`.

The reviewer returns:

```text
VERDICT: APPROVE | REVISE | BLOCK
ISSUES:
- ...
REQUIRED_CHANGES:
- ...
CONFIDENCE: low | medium | high
```

It must actively look for:

- misunderstood intent;
- risk classified too low;
- missing production/auth/payment/PII/destructive implications;
- unjustified assumptions;
- wrong or excessive skills/tools;
- missing useful delegation or pointless delegation;
- unsafe parallel writers/shared state;
- dependency mistakes;
- weak verification;
- missing rollback/backup/post-check;
- a plan shaped by prompt words rather than the actual problem.

`REVISE` means the primary agent updates the decision and re-runs review when the change is material. Ordinary review is bounded to two revisions; after that, choose a conservative path or surface the unresolved uncertainty.

`BLOCK` means do not execute until the missing evidence/user decision/safety issue is resolved.

## 6. Strong-review escalation

The cheap reviewer runs for ordinary preflight, but it is not the only reviewer when consequences are high.

- `RISK_3/RISK_4` -> add an independent `critic`/`judgment` tier review.
- destructive or hard-to-reverse data work -> `RISK_4`, verified backup, rollback plan and post-check.
- auth, payments, secrets, PII, production migrations -> strong independent review.
- large structural architecture plan -> strong critic before implementation commitment.
- high-ambition public visual work -> independent design critique plus browser/rendered evidence.

If a separate model cannot be spawned, use an isolated fresh context with the same review contract. If that is also unavailable, perform an explicit adversarial self-review and disclose the lack of independence in the working record.

## 7. Skills are chosen by the AI

Profiles and metadata are knowledge inventories, not a classifier.

The primary model decides which skills are relevant after inspecting the actual task. A skill is not “used” merely because its ID appears somewhere: the stage model must read its `SKILL.md` or receive provider-native injection of the same body.

Choose the smallest useful set. Domain-specific guidance requires real evidence that the domain applies. For example, PostgreSQL-specific guidance needs actual PostgreSQL/psql/Supabase context, not the word “database” alone.

## 8. Public visual surfaces

A landing page, homepage, brand/company website, portfolio, storefront, campaign site or total visual redesign is design-primary even if the implementation language is React/CSS/etc.

Greenfield or total public redesign normally follows:

`interview -> live reference research -> direction/concept -> implementation -> independent visual critique -> desktop/mobile browser verification`

Do not reduce a design problem to a frontend keyword.

## 9. What remains deterministic

Mechanical programs may still copy files, manage manifests, run tests, persist state or execute explicitly chosen tooling. They must not interpret natural-language intent or decide the semantic task plan.

The rule is simple:

> **AI decides; software performs mechanical operations after the decision.**

## Non-goals

- no `route.py`;
- no semantic `decision_contract.py`;
- no regex/keyword risk inference;
- no executable router evals pretending to benchmark language understanding;
- no script that chooses category/topology/skills from prompt text;
- no blind trust in one model when a cheap second opinion is available;
- no safety downgrade because either model sounds confident.