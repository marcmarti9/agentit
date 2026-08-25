# Reference Intelligence integration points

This branch makes reference use a contextual, enforceable part of Agentit rather than an optional prompt convention.

## Decision layer

- `skills/task-router/SKILL.md` requires explicit `reference_plan.mode = none | catalog | live | mixed` for material tasks.
- Semantic source selection remains owned by the primary AI.
- Missing catalog coverage is not a reason to rely on model memory; `live` discovery is used for current domain-specific sources.

## Audit layer

- `skills/task-router/references/economy-reviewer.md` challenges unjustified `none`, stale/current-source gaps, creator claims promoted to facts, overload, cloning, and dependency/license mistakes.

## Knowledge layer

- `skills/reference-intelligence/SKILL.md` defines authority roles, curated packs, live-domain discovery, extraction, provenance, and completion checks.
- `references/catalog.yaml` provides curated seed references/packs.

## Runtime verification layer

- `router/verify.py` accepts only explicit AI-selected reference mode/sources.
- A non-`none` apply run requires inspected-source evidence and optional required provenance.
- Missing reference evidence makes the verification receipt blocking-failed, so done-like claims cannot pass the anti-greenwash gate.

## Regression layer

- `router/test_reference_catalog.py` locks the activation/audit/verification contract.
- `router/test_verify.py` verifies that reference mode is never inferred from task text and that selected-but-unread references block the receipt.

## User-facing behavior

The user does not need to paste or remind Agentit about references. Agentit decides contextually whether they matter; loads only relevant ones; discovers authoritative live sources for uncovered domains; and can prove that selected references were actually used before completion.
