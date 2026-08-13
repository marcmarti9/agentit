---
name: task-router
description: Classify risk, topology, skills, and context before execution. Public visual surfaces are design-primary.
---

# Intelligent task router

The router is a planning aid, never permission to lower risk or skip project/user instructions. Keep safety, reversibility and verification from the base route.

## Hard routing correction: public visual surfaces

A landing page, homepage, corporate/brand website, marketing site, portfolio, storefront, campaign site, or a complete visual redesign is **design-primary**, even when implementation is React/Next/CSS and even if a generic heuristic calls it `frontend` or `marketing`.

For public visual work:

- use the `design` domain pack;
- a greenfield public surface or total visual redesign defaults to **Studio** unless the user explicitly chooses a leaner craft depth;
- interview deeply before planning;
- research live visual references before committing to art direction;
- produce a concrete `DESIGN_DIRECTION` before code;
- use independent research/concept/critique workers when they improve context isolation or creative diversity;
- require browser evidence on desktop and mobile before claiming visual success.

Normal staged shape for greenfield/total redesign:

`interview -> reference research -> concept/direction -> implementation -> independent visual critique -> browser verification`

Research/concept branches may fan out inside that pipeline. Do not collapse to single-agent merely because one agent could technically do everything.

## Skill activation contract

A skill ID in `skills_available`, `load_now`, a profile, or a worker payload is **not proof the skill is active**. Before relying on a skill, the model doing that stage must actually read its `SKILL.md` body (or receive the body in projected context). Keep a load receipt containing skill ID/path/hash when the host supports it.

If a worker prompt only contains names such as `design-taste-frontend` but not the bodies and the provider does not natively resolve them, load/embed those bodies before spawn. Never pretend an unopened skill influenced the work.

## Design quality floor

Greenfield/total public work should normally load by stage:

- research: `design-inspiration-research`;
- direction: `design-taste-frontend` + `impeccable-design`;
- implementation: `frontend-ui-engineering` + `emil-design-eng`;
- critique: `impeccable-design` + `design-taste-frontend` + browser verification.

The design critic must reject wrapper-only cardification, repeated section silhouettes, generic hero/card/CTA templates, and a final design that cannot explain how reference research changed its decisions.

## Delegation

Delegation requires benefit, not magic words. Valid benefits include independent packages **and also**:

- reading large documentation/reference sets without polluting the parent context;
- exploring several visual/reference hypotheses independently;
- concept competition;
- fresh-context critique;
- using a cheaper/faster worker for volume reading while a stronger parent keeps judgment and synthesis.

A strong parent model should not serially consume every document just to preserve a single-agent topology. Provider-specific model names are configuration; route by semantic capability tier.

## General rules

1. Inferred risk is a floor; explicit labels may raise it, never lower it.
2. Select the smallest **useful** skill set, not the smallest possible set. Art direction is useful/required for public visual work.
3. Prefer `direct` for tightly coupled work, `probe` for read-only investigation, `fan_out` for independent branches, `pipeline` for dependent stages, `writer_reviewer` for implementation + independent review, and `audit` for critical review.
4. One writer per file unless isolated branches/worktrees make ownership safe.
5. Large structural/high-impact plans require an independent critic.
6. Preserve exact commands, diffs, errors, SQL, paths, IDs, hashes, schemas and operational evidence.
7. PostgreSQL-specific guidance requires an actual Postgres/Supabase signal; generic database work must inspect the stack first.
8. `skills_available` means discoverable/compatible, not loaded. `skills_recommended_missing` means relevant but unavailable.
9. `subagents.recommended` is advisory; there are no hard min/max agent quotas.
10. Verify actual runtime/rendered behavior before completion claims.
