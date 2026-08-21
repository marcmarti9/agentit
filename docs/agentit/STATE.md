# Agentit state

**Updated:** 2026-08-21
**Status:** final verification
**Branch:** refactor/llm-native-routing
**PR:** https://github.com/marcmarti9/agentit/pull/24

## Goal

Remove programmatic natural-language routing from Agentit. The primary AI interprets each task from full context, creates a `TASK_DECISION`, and an independent second AI reviews that decision before material execution. Ordinary review uses the cheapest capable model/endpoint; high-consequence work additionally escalates to a stronger critic/judgment reviewer.

## Confirmed intent

- Audience: Agentit users and agents across providers.
- Success criteria: no Python/regex/keyword semantic router; no executable script decides task intent/category/risk/topology/skills/delegation from prompt text; cheap AI second opinion is the normal pre-execution check; stronger review remains mandatory when consequences justify it.
- Constraints: provider-neutral semantic tiers, bounded review loop, read-only reviewer, safety escalation, one-writer ownership, mandatory Loop/Graph acceptance for executable work, PR-first workflow.
- Non-goals: removing useful mechanical software such as profile installation, MCP/runtime state, test execution, manifests, continuity, capability inventory, Loop/Graph enforcement, or verification.

## Domain pack

- Pack: engineering (Agentit harness architecture)
- Craft depth: n/a (not design/visual work)
- Effort: structural refactor
- Topology: writer/reviewer for the architecture change; PR-first integration
- Strong independent review required: yes for large structural changes

## Current status

- Complete: semantic `route.py` removed; semantic decision validator removed; route trace/eval code removed; primary-model decision rubric rewritten; mandatory economy reviewer contract added; strong-review escalation documented; inventory decoupled from removed router; continuity rewritten around AI decisions rather than router output.
- Earlier review fixes complete: MCP manager accepts only explicit `stack_id` recommendations; MCP stack enablement has no free-text fallback; gateway tests cover the real tool path; continuity leaves undecided semantic fields unset; registry/inventory safety tests restored; reviewer verdict vocabulary unified to `CLEAR / CHALLENGE / ESCALATE`.
- Strong architecture review completed on PR #24. Findings were: stale canonical interview/provider policy, stale `reports/recommendations.md`, accidental weakening of the mandatory Loop/Graph receipt gate, and an awkward legacy MCP compatibility path.
- Strong-review fixes complete: active policy now matches the LLM-native architecture; recommendations were rewritten; Loop/Graph is explicitly mandatory for executable work with verifiable outcomes; the legacy `recommend_for_task` helper resolves exact stack IDs only and rejects arbitrary free text; architecture regression tests were added.
- CI #218 on intermediate HEAD `b8f8c0f1028bf8f2ccc985fc961a6d206703953a` found one expected-message mismatch in the MCP CLI test. That mismatch was fixed in commit `1308bcb3b9a2ee1d078c85876bba9e72d1427195` without changing the safety behavior.
- In progress: GitHub Actions verification on the final HEAD after this state update.
- Blocked: merge only until final HEAD CI is green.

## Decisions

- `TASK_DECISION` is made by the primary AI using conversation + project + tool context.
- A cheap independent AI reviewer returns `CLEAR`, `CHALLENGE`, or `ESCALATE` before material execution.
- `CLEAR` is not approval authority; `CHALLENGE` requires primary reconsideration and unresolved material disagreement escalates; `ESCALATE` requires a stronger independent reviewer.
- Prefer semantic tier `fast` for ordinary preflight and a different model family when similarly cheap.
- RISK_3/RISK_4, destructive/irreversible work, auth/payments/secrets/PII/production, significant migrations, and large structural plans additionally require a stronger `critic`/`judgment` review.
- Software may perform mechanical operations after the AI decision but may not infer semantic routing from natural-language keywords.
- Every executable unit with a verifiable outcome requires a Loop Contract and passed Loop Receipt; multi-node execution additionally requires a Graph Contract and passed Graph Receipt.
- MCP stack resolution is mechanical: the primary AI chooses a named `stack_id`; code resolves that explicit ID and never infers it from task text.
- The legacy `recommend_for_task` symbol is compatibility-only: exact known stack IDs resolve; arbitrary task text fails explicitly.
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
- `docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`
- `docs/MCP_CATALOG.md`
- `reports/recommendations.md`
- `router/profiles.py`, `router/continuity.py`, `router/inventory.py`, `router/mcp_catalog.py`, `router/mcp_runtime.py` (mechanical infrastructure only)
- `router/test_inventory_registry.py`, `router/test_mcp_runtime.py`, `router/test_continuity.py`
- `tests/test_architecture_policy.py`
- `mcp/gateway.py`
- PR #24

## Verification

- Earlier GitHub Actions CI #208 passed on HEAD `fe8fe7af17725602b51627f805bd76a5d0256a37` before the strong-review fixes.
- CI #218 correctly failed on one MCP CLI error-message expectation after the compatibility cleanup; all preceding runtime tests in that run passed except that assertion.
- The error wording was corrected while preserving exact-stack-only behavior and explicit free-text rejection.
- Final acceptance requires GitHub Actions success on the final PR HEAD after this state update.
- Architecture regression coverage now checks active policy for stale router contracts, the mandatory Loop/Graph receipt gate, and exact-stack-only legacy MCP compatibility.
- No executable prompt-classification eval suite remains by design.

## Next actions

1. Confirm GitHub Actions is green on the final PR HEAD.
2. Merge PR #24 as explicitly authorized by the user.
3. Verify `main` contains the merged refactor.

## Open questions / blockers

- Only final-head CI.

## Recovery

- Resume from PR #24 on `refactor/llm-native-routing`.
- Inspect the latest PR head and CI; if green, merge as already authorized.
- If implementation scope changes materially before merge, rebuild `TASK_DECISION` from current context and run the independent AI review again.
