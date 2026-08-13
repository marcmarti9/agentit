---
name: task-router
description: Classify risk, topology, skills, and context before execution. Public visual surfaces are design-primary.
---

# Intelligent task router

The router is a provider-neutral planning aid, never permission to execute, lower risk, mutate tooling, or skip user/project instructions. Its JSON is advisory; the active provider and explicit instructions still win.

## Invocation

```bash
python3 router/route.py "describe the task"
python3 router/route.py --risk RISK_2 "describe the task"
```

Inspect the repository/target environment before acting.

## Hard routing correction: public visual surfaces

A landing page, homepage, corporate/brand website, marketing site, portfolio, storefront, campaign site, or complete visual redesign is **design-primary**, even when implementation is React/Next/CSS and even if a generic heuristic labels it `frontend` or `marketing`.

For public visual work:

- use the `design` domain pack;
- greenfield public surfaces and total visual redesigns recommend **Studio** unless the user chooses a leaner depth;
- run the deep `interview-me` path before planning;
- research live references before art direction;
- create a concrete `DESIGN_DIRECTION` before code;
- use independent research/concept/critique workers when isolation or diversity helps;
- require browser evidence on desktop and mobile before visual-success claims.

Normal greenfield/total shape:

`interview -> reference research -> concept/direction -> implementation -> independent visual critique -> browser verification`

Research/concept branches may fan out inside that pipeline. Do not collapse to direct only because one model could technically perform every step.

## Output contract

- `skills_available`: recommended skills that are discoverable/compatible.
- `skills_recommended_missing`: relevant recommendations that cannot currently be used.
- `skills`: legacy alias of `skills_available`.
- `signals`: evidence used by routing heuristics.
- `confidence`: uncalibrated signal strength; `confidence_calibrated` remains false without reviewed labels.
- `rejected_topologies`: why alternatives were not selected.
- `applied_preferences`: safe project/user preferences to apply.
- `jit_profile_recommendations`: missing profiles worth project-local activation.
- `topology`: `direct`, `probe`, `fan_out`, `pipeline`, `writer_reviewer`, or `audit`.
- `subagents.recommended`: soft guidance; no hard max/min quota.
- `domain_pack`, `skill_budget`, `craft_depth` (visual only), `spend`, `token_estimate`, `parallelism`, `critic_required`, `multi_agent_pushback`: execution guidance.

## Skill activation contract

A skill ID in router output, a profile, or a worker payload is **not proof the skill is active**. Before a stage relies on a skill, the model doing that stage must actually read its `SKILL.md` body or receive it through demonstrable provider-native injection. Keep a small ID/path/hash load receipt when the host supports it.

If a worker only sees names such as `design-taste-frontend` and the provider does not resolve those names automatically, load/embed the corresponding bodies before work. Never claim an unopened skill shaped the result.

Greenfield/total public work normally loads by stage:

- research: `design-inspiration-research`;
- direction: `design-taste-frontend` + `impeccable-design`;
- implementation: `frontend-ui-engineering` + `emil-design-eng`;
- critique: `impeccable-design` + `design-taste-frontend` + browser verification.

## Selection rules

1. Infer risk from the requested action/environment, not keyword mentions alone. Explicit risk may raise but never lower inferred risk.
2. Select the smallest **useful** skill set. For a public visual surface, art direction is useful/required rather than optional polish.
3. Use terse output only for low-risk unambiguous work; preserve enough detail for review when precision matters.
4. Keep exact content for commands, pipes, redirects, diffs, errors, SQL, paths, IDs, hashes, credentials, schemas, migrations and affected-file lists.
5. Exact deduplication is safe by default; do not semantically compress decision-critical material without retrieval.
6. RISK_3/4 use fuller evidence/independent review; RISK_4 also needs the stronger operational gates defined by the base router.
7. Delegation needs scope/ownership/verifier, but **context isolation, research breadth, concept diversity and fresh critique are legitimate benefits**.
8. PostgreSQL-specific guidance requires a real PostgreSQL/psql/Supabase signal. Generic/SQLite work must not receive Postgres-specific advice.
9. Large structural/high-impact plans require an independent critic.
10. Verify actual runtime/rendered behavior before completion claims.

## Delegation

Valid reasons include independent files/domains, read-only investigation, large documentation/reference sets, independent visual hypotheses, concept competition, fresh critique, or using a more efficient worker for volume reading while a stronger parent preserves context for judgment/synthesis.

Provider-specific model names belong in provider configuration. Portable routing talks about semantic capability tiers.

## Skill visibility profiles

The repository keeps all skill bodies in `skills/`; global installation remains intentionally bounded to the `core` profile. Add opt-in families project-locally rather than dumping the entire catalog into every context:

```bash
./agentit enable design --project .
./agentit enable design --project . --apply
./agentit status --project .
./agentit disable design --project . --apply
```

`profiles.yaml` is visibility policy; `registry.yaml` is routing/inventory metadata. A registry entry does not mean its body was loaded.

## Adaptive execution

Prefer `direct` for tightly coupled work, `probe` for read-only investigation, `fan_out` for independent branches, `pipeline` for dependent stages, `writer_reviewer` for one implementation owner + independent review, and `audit` for critical review. One writer per file/shared state unless isolated branches/worktrees give explicit ownership.

The design critic should reject wrapper-only cardification, repeated section silhouettes, generic hero/card/CTA templates, and research that cannot explain any final design decision.

## Provider adapters

Codex/Claude/Gemini/other hosts may implement workers and skill loading differently. Do not assume model names or skill injection are portable. Missing critical review/skill context should fail visibly rather than silently downgrade. If native subagents are unavailable, use an isolated delegated call/fresh context or load the same scoped skill bundle into the parent.

## Non-goals

- no global shell interception;
- no automatic activation of unrelated tooling;
- no full-catalog context dumps;
- no replacement of exact errors/diffs/operational evidence with lossy summaries;
- no forced multi-agent and no forced single-agent.
