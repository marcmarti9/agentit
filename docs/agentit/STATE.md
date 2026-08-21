# Agentit state

**Updated:** 2026-08-21
**Status:** in review
**Branch:** refactor/llm-native-routing
**PR:** https://github.com/marcmarti9/agentit/pull/24

## Goal

Remove programmatic natural-language routing from Agentit. The primary AI interprets each task from full context, creates a `TASK_DECISION`, and an independent second AI reviews that decision before material execution. Ordinary review uses the cheapest capable model/endpoint; high-consequence work additionally escalates to a stronger critic/judgment reviewer.

## Confirmed intent

- Audience: Agentit users and agents across providers.
- Success criteria: no Python/regex/keyword semantic router; no executable script decides task intent/category/risk/topology/skills/delegation from prompt text; cheap AI second opinion is the normal pre-execution check; stronger review remains mandatory when consequences justify it.
- Constraints: provider-neutral semantic tiers, bounded review loop, read-only reviewer, safety escalation, one-writer ownership, PR-first workflow.
- Non-goals: removing useful mechanical software such as profile installation, MCP/runtime state, test execution, manifests, continuity, capability inventory, or verification.

## Domain pack

- Pack: engineering (Agentit harness architecture)
- Craft depth: n/a (not design/visual work)
- Effort: structural refactor
- Topology: writer/reviewer for the architecture change; PR-first integration
- Strong independent review required: yes for large structural changes

## Current status

- Complete: semantic `route.py` removed; semantic decision validator removed; route trace/eval code removed; primary-model decision rubric rewritten; mandatory economy reviewer contract added; strong-review escalation documented; README/AGENTS/using-agentit updated; inventory decoupled from removed router; stale route hooks removed from profile CLI; continuity rewritten around AI decisions rather than router output.
- In progress: final CI verification and cleanup of stale active documentation/references.
- Blocked: none known.
- Not started: merge decision after CI passes.

## Decisions

- `TASK_DECISION` is made by the primary AI using conversation + project + tool context.
- A cheap independent AI reviewer returns `APPROVE`, `REVISE`, or `BLOCK` before material execution.
- Prefer semantic tier `fast` for ordinary preflight and a different model family when similarly cheap.
- RISK_3/RISK_4, destructive/irreversible work, auth/payments/secrets/PII/production, significant migrations, and large structural plans additionally require a stronger `critic`/`judgment` review.
- Software may perform mechanical operations after the AI decision but may not infer semantic routing from natural-language keywords.
- Reviews are bounded; ordinary review does not loop indefinitely.

## Important files and artifacts

- `skills/task-router/SKILL.md`
- `skills/task-router/references/economy-reviewer.md`
- `skills/using-agentit/SKILL.md`
- `AGENTS.md`
- `docs/NO_PROGRAMMATIC_ROUTER.md`
- `docs/LLM_NATIVE_DECISION_PROTOCOL.md`
- `router/profiles.py`, `router/continuity.py`, `router/inventory.py` (mechanical infrastructure only)
- PR #24

## Verification

- GitHub Actions runs are the acceptance gate for the refactor.
- Runtime/utility tests must pass after deleting router-dependent modules.
- Script tests, shell syntax, registry YAML, settings JSON, profile catalog, and capability catalog must pass.
- No executable prompt-classification eval suite remains by design.

## Next actions

1. Wait for the latest PR #24 CI run and inspect failures if any.
2. Search active docs/code for stale `route.py`, `agentit trace`, `decision_contract.py`, or deterministic-routing claims and remove applicable references.
3. Leave PR #24 open for the merge decision once CI is green.

## Open questions / blockers

- None currently.

## Recovery

- Resume from PR #24 on `refactor/llm-native-routing`.
- Read this file, inspect the latest PR head/CI, then continue Next actions.
- If the implementation scope changes materially, rebuild `TASK_DECISION` from current context and run the independent AI review again before executing the changed plan.
