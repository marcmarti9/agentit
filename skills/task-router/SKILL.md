---
name: task-router
description: LLM-native Agentit decision protocol. The agent classifies every task from full context; code only validates deterministic invariants.
---

# LLM-native decision protocol

Agentit does **not** use a keyword/regex router to understand user intent.
The active model is the semantic router.

Before executing any task, classify it using the same rubric below. Use the
**full available context**: conversation, repository state, files, tools,
provider capabilities, user instructions and project rules. Do not classify a
follow-up such as “fix it” from that string alone when prior context explains
what “it” is.

The protocol is mandatory; the exact answer is contextual. Same rubric does not
mean same classification.

## Mandatory decision

Before action, determine:

- `intent`: explain | investigate | review | implement | design | document | operate
- `category`: explanation | research | bug | testing | engineering | frontend | design | backend | database | security | marketing | documentation | release
- `complexity`: trivial | bounded | substantial | structural
- `risk`: RISK_0..RISK_4
- `reversible`: true | false | null
- `topology`: direct | probe | fan_out | pipeline | writer_reviewer | audit
- `domain_pack`: engineering | frontend | design | backend | data | product | writing | release | research
- whether this is a public visual surface
- whether it is greenfield / a total visual redesign
- design craft depth when applicable: Standard | Polished | Studio
- whether the task is a destructive data operation
- smallest useful skills to load
- useful specialists, if any
- required/preferred capabilities
- delegation benefit and useful parallelism
- verification gates
- whether an independent critic is required
- concrete evidence/signals supporting the decision
- short reasons for the classification

The host may keep this decision internal when exposing it would only add noise,
but it must actually make the decision before execution.

## Risk rubric

`RISK_0` — read-only explanation/analysis with no meaningful mutation.

`RISK_1` — local, trivial, easily reversible change with very small blast radius.

`RISK_2` — meaningful but bounded engineering/product change.

`RISK_3` — sensitive boundary such as auth, security, payments, PII,
significant migration/infrastructure, or comparable consequences.

`RISK_4` — destructive, production, data-loss, irreversible, or otherwise
high-blast-radius operation.

Explicit user/project risk policy is a floor. Never lower it.

## Topology rubric

`direct` — one coherent execution owner; delegation adds no concrete benefit.

`probe` — read-only investigation should happen before implementation/judgment.

`fan_out` — at least two genuinely independent branches benefit from isolated
parallel work.

`pipeline` — dependent stages need explicit handoffs.

`writer_reviewer` — one implementation owner plus independent review is justified
by error cost.

`audit` — the main job is independent inspection/critique rather than writing.

Multi-agent is an optimization, not a ritual. Use it for independence,
specialization, context isolation, research breadth or fresh review. Do not use
it merely because the task is long, and do not avoid it merely because one model
could technically do everything.

## Deterministic hard gates

The structured decision can be checked with `router/decision_contract.py`.
Python validates; Python does not reinterpret the prompt.

Hard invariants:

1. RISK_3/RISK_4 require independent review.
2. RISK_4 requires a dry-run/preview where technically meaningful, rollback plan,
   and post-check.
3. Destructive data operations require RISK_4 and a verified backup.
4. Structural work requires an independent critic.
5. `fan_out` requires at least two independent branches and a concrete reason.
6. `direct` means one execution owner.
7. Public visual surfaces are design-primary and require browser/rendered evidence.
8. Greenfield/total public visual redesign defaults to Studio unless the user
   explicitly chooses a leaner depth.

## Skill selection and loading

The model decides which skills are relevant. Registry code may only verify that
a requested ID exists and is actually loadable.

A skill name in a decision is **not evidence the skill was used**. Before a stage
relies on a skill, read that skill's `SKILL.md` body or use a provider-native
mechanism that demonstrably injects the same content. Missing skills must be
surfaced or replaced deliberately; never pretend an unopened skill shaped the
work.

Select the smallest useful set. PostgreSQL-specific guidance requires actual
Postgres/psql/Supabase evidence. Similar domain-specific constraints should be
resolved from real context, not prompt substrings.

## Public visual surfaces

Landing pages, homepages, public company/brand sites, portfolios, storefronts,
campaign sites and total visual redesigns are design-primary.

For ambitious greenfield/total public visual work, the normal shape remains:

`interview -> live reference research -> concept/direction -> implementation -> independent visual critique -> desktop/mobile browser verification`

Do not let a generic “frontend” implementation label erase the design problem.

## Structured decision shape

Provider adapters may materialize the internal decision as JSON. The canonical
schema is enforced by `router/decision_contract.py`; conceptually:

```json
{
  "schema_version": 1,
  "intent": "implement",
  "category": "engineering",
  "complexity": "bounded",
  "risk": "RISK_2",
  "reversible": true,
  "topology": "direct",
  "domain_pack": "engineering",
  "public_visual": false,
  "greenfield_or_total_redesign": false,
  "craft_depth": null,
  "craft_depth_overridden": false,
  "destructive_data_operation": false,
  "skills": [],
  "specialists": [],
  "capabilities": {"required": [], "preferred": []},
  "delegation": {"parallelism": 1, "reason": ""},
  "verification": {
    "tests_required": true,
    "browser_required": false,
    "independent_review": false,
    "dry_run_required": false,
    "backup_required": false,
    "rollback_plan_required": false,
    "post_check_required": false
  },
  "critic_required": false,
  "evidence_signals": [],
  "reasons": ["short evidence-based reason"]
}
```

## CLI boundary

`python3 router/route.py "task"` now emits a **decision request**, not a semantic
classification. This exists for adapters/debugging and makes the ownership
boundary explicit.

To validate a host-model decision:

```bash
python3 router/route.py --decision decision.json
```

Do not call the CLI as a substitute for reasoning. The active agent already has
more context than a standalone prompt string and should classify the task itself.

## Non-goals

- no prompt-keyword risk inference;
- no regex intent classifier;
- no deterministic guess of category/topology from natural language;
- no forced single-agent or forced multi-agent;
- no claim that IDs equal loaded skill bodies;
- no safety downgrade because the model is confident.
