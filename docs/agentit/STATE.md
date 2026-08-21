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
- Review fixes complete: MCP manager now accepts only explicit `stack_id` recommendations; MCP stack enablement no longer falls back to free-text routing; gateway tests exercise the real tool path; continuity no longer invents semantic defaults before `TASK_DECISION`; mechanical registry/inventory safety tests restored; reviewer verdict vocabulary unified to `CLEAR / CHALLENGE / ESCALATE`; stale router wording removed from active skill docs.
- Verification complete: GitHub Actions CI run #206 passed on commit `073da66242a5a82d9cc4c0dd428e3800f4d68378`, including runtime/utility tests, script tests, shell syntax, registry/settings/profile/capability validation and the new regression coverage.
- Blocked: independent strong architecture review is still required by Agentit's own policy before merge; the previous Copilot review attempt failed because its quota was exhausted.
- Not started: merge decision after strong review.

## Decisions

- `TASK_DECISION` is made by the primary AI using conversation + project + tool context.
- A cheap independent AI reviewer returns `CLEAR`, `CHALLENGE`, or `ESCALATE` before material execution.
- `CLEAR` is not approval authority; `CHALLENGE` requires primary reconsideration and unresolved material disagreement escalates; `ESCALATE` requires a stronger independent reviewer.
- Prefer semantic tier `fast` for ordinary preflight and a different model family when similarly cheap.
- RISK_3/RISK_4, destructive/irreversible work, auth/payments/secrets/PII/production, significant migrations, and large structural plans additionally require a stronger `critic`/`judgment` review.
- Software may perform mechanical operations after the AI decision but may not infer semantic routing from natural-language keywords.
- MCP stack resolution is mechanical: the primary AI chooses a named `stack_id`; code resolves that explicit ID and never infers it from task text.
- Missing semantic continuity fields remain `(unset)` until supplied by an AI decision rather than defaulting to engineering/direct/no-review.
- Reviews are bounded; ordinary review does not loop indefinitely.

## Important files and artifacts

- `skills/task-router/SKILL.md`
- `skills/task-router/references/economy-reviewer.md`
- `skills/using-agentit/SKILL.md`
- `skills/using-agent-skills/SKILL.md`
- `AGENTS.md`
- `docs/NO_PROGRAMMATIC_ROUTER.md`
- `docs/LLM_NATIVE_DECISION_PROTOCOL.md`
- `docs/MCP_CATALOG.md`
- `router/profiles.py`, `router/continuity.py`, `router/inventory.py`, `router/mcp_catalog.py`, `router/mcp_runtime.py` (mechanical infrastructure only)
- `router/test_inventory_registry.py`, `router/test_mcp_runtime.py`, `router/test_continuity.py`
- `mcp/gateway.py`
- PR #24
- GitHub Actions CI #206: success on `073da66242a5a82d9cc4c0dd428e3800f4d68378`

## Verification

- GitHub Actions CI #206: **success**.
- Runtime and utility tests: passed.
- Script tests: passed.
- Shell syntax: passed.
- Registry YAML, settings JSON, profile catalog and capability catalog validation: passed.
- Gateway regression coverage proves explicit named-stack recommendation works and task-text input does not silently route.
- Continuity regression coverage proves undecided semantic fields remain visibly unset and explicit AI decision fields persist.
- Registry/inventory regression coverage includes duplicate IDs, invalid states/schema, malformed/missing YAML, portable-root traversal, symlink escape and malformed provider metadata.
- No executable prompt-classification eval suite remains by design.

## Next actions

1. Obtain the required independent strong architecture review.
2. If that review raises material findings, fix them and rerun CI.
3. Leave PR #24 open for the user merge decision once strong review is green.

## Open questions / blockers

- Independent strong architecture review still required before merge.

## Recovery

- Resume from PR #24 on `refactor/llm-native-routing`.
- Read this file, inspect the latest PR head/CI, then continue Next actions.
- If the implementation scope changes materially, rebuild `TASK_DECISION` from current context and run the independent AI review again before executing the changed plan.
