---
name: task-router
description: Classify risk, topology, skills, and context before execution. Use to route a task; not as permission to run it.
---

# Intelligent task router

Use the router as a heuristic planning aid, never as permission to execute. It is provider-neutral and deliberately does not execute the task, load skill bodies, rewrite stdout, install hooks, call MCP servers, or reduce an inferred risk level.

It recommends a topology and an **advisory** specialist budget with **no hard min/max caps**. Spawn only when structure or ordinary language shows benefit. Craft depth (standard/polished/studio) is design/visual only. Token estimates are project-aware. No powerwords beyond natural Agentit activation. A human must review critical operations before execution.

## Invocation

From the harness repository:

```bash
python3 router/route.py "describe the task"
python3 router/route.py --risk RISK_2 "describe the task"
```

The JSON result is a proposal. The active provider, project instructions, explicit user request, and human authorization still have precedence. Inspect the repository and target environment before acting.

## Output contract

- `skills_available` contains only recommended skills whose catalog state, observed path, and essential dependencies are compatible.
- `skills_recommended_missing` contains relevant recommendations that are not usable under those checks.
- `skills` is a legacy alias for `skills_available`; it never contains missing recommendations.
- `signals` lists the human-readable evidence used by the deterministic heuristic.
- `confidence` is an uncalibrated signal-strength score; `confidence_calibrated` is
  `false` until reviewed labels exist.
- `rejected_topologies` explains why the other execution shapes were not selected.
- `applied_preferences` exposes active user preferences (`preferred_language`, `testing_framework`, `ui_styling`). Agents should apply these preferences unless they conflict with project requirements or safety rules.
- `jit_profile_recommendations` lists missing profiles recommended for the task. Agents may auto-activate them via `./agentit enable <profile> --project . --apply` when JIT mode is active.
- `topology` can be `direct`, `probe`, `fan_out`, `pipeline`, `writer_reviewer`, or
  `audit`. `subagents.recommended` is soft guidance (`hard_cap: false`, `max: null`).
- `domain_pack`, `skill_budget`, `craft_depth` (design only), `spend`, `token_estimate`,
  `parallelism`, `critic_required`, and `multi_agent_pushback` guide intelligent execution.

`registry.yaml` is portable operational policy, not a machine inventory. It uses only `${HOME}` and `${REPO_ROOT}` path templates. Generate an ignored, per-machine observation with `python3 -m router.inventory`; executable versions may remain unobserved.

## Selection rules

1. Infer risk from the requested action and target environment, not from a keyword mention alone. Explanation or documentation about backups, production, credentials, or permissions does not request that operation. An explicit risk label may raise the level but never lower any inferred risk.
2. Select the smallest useful skill set. A registry entry is metadata; load its `SKILL.md` only after selection.
3. Use `TERSE_SAFE` only for low-risk, unambiguous progress or explanation output. Use `STANDARD` for ordinary work and `VERBOSE_ALLOWED` when precision or review matters.
4. Keep exact content for commands, pipes, redirects, diffs, errors, SQL, paths, IDs, hashes, numbers, credentials, schemas, migrations, and affected-file lists.
5. Use only exact deduplication by default. Reversible CCR may be considered for RISK_2 large outputs when the original is retained and retrieval is explicit.
6. For RISK_3 and RISK_4, retrieve original content before a decision if compressed content could influence it and require human review. For RISK_4 also require backup evidence, a dry run where possible, independent review, and a post-operation check.
7. Do not spawn solely because a number is non-zero; do not refuse solely because single-agent is traditional. Delegation needs scope, ownership, and a verifier. Large structural plans set `critic_required`.
8. Select `supabase-postgres-best-practices` only when the request includes a PostgreSQL signal such as Postgres, PostgreSQL, `psql`, or Supabase. A SQLite task is still a database task but must not receive Postgres-specific guidance; if no database engine is known, return `inspect_database_stack` in `routing_advice`.

## Skill visibility profiles

The repository keeps all skill bodies in `skills/`, but `install.sh` copies only
the 12-skill `core` profile (includes `using-agentit` + `verification-gauntlet`)
to provider-global directories. Use the plan-first helper to add an opt-in
profile to a project without overwriting or removing unmanaged files:

```bash
./agentit enable supabase --project .
./agentit activate supabase --project .  # alias
./agentit enable supabase --project . --apply
./agentit status --project .
./agentit disable supabase --project . --apply
```

`profiles.yaml` is the installation visibility policy. `registry.yaml` remains
the compact routing/inventory metadata and does not imply that every repository
skill should be globally discoverable.

For an older global install, use the explicit migration flag below. It only removes
unmodified byte-identical non-core copies after creating a backup:

```bash
bash install.sh --provider codex --apply --prune-on-demand
```

## Adaptive execution

Prefer `direct` for tightly coupled work, `probe` for read-only investigation, `fan_out` for independent packages/paths/domains (ordinary language is enough), `pipeline` for staged research→implement, and `audit` for high-risk review. One writer per file; parallel writers need worktrees/branches.

## Provider adapters

The router output can be consumed by Codex CLI, Claude Code, or Antigravity/Gemini as a local JSON planning step. Do not assume that a model name is portable between providers. Provider-specific model selection belongs in the provider configuration, and an unavailable model must fail closed rather than silently downgrade a critical review.

## Non-goals

- No global shell interception.
- No semantic compression of source code or operational data.
- No automatic activation of hooks, MCP servers, proxies, or third-party installers.
- No replacement of full logs, errors, diffs, or migration plans with summaries.
