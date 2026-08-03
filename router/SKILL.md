---
name: task-router
description: Classifies a task by risk, complexity, content type, skill budget, output profile, and safe context policy before execution. Use when choosing skills, subagents, or compression for a task.
---

# Conservative task router

Use the router as a planning aid, not as permission to execute. It is provider-neutral and deliberately does not load skill bodies, rewrite stdout, install hooks, call MCP servers, or reduce an inferred risk level. The default topology is one capable agent; a budget is not an instruction to spawn.

## Invocation

From the harness repository:

```bash
python3 router/route.py "describe the task"
python3 router/route.py --risk RISK_2 "describe the task"
```

The JSON result is a proposal. The active provider, project instructions, and explicit user request still have precedence. Inspect the repository before acting.

## Selection rules

1. Infer the highest applicable risk from the task and content. An explicit risk label may raise the level but never lower an inferred RISK_3 or RISK_4.
2. Select the smallest useful skill set. A registry entry is metadata; load its `SKILL.md` only after selection.
3. Use `TERSE_SAFE` only for low-risk, unambiguous progress or explanation output. Use `STANDARD` for ordinary work and `VERBOSE_ALLOWED` when precision or review matters.
4. Keep exact content for commands, pipes, redirects, diffs, errors, SQL, paths, IDs, hashes, numbers, credentials, schemas, migrations, and affected-file lists.
5. Use only exact deduplication by default. Reversible CCR may be considered for RISK_2 large outputs when the original is retained and retrieval is explicit.
6. For RISK_3 and RISK_4, retrieve original content before a decision if compressed content could influence it. For RISK_4 require backup evidence, dry run where possible, independent review, and a post-operation check.
7. Do not spawn an agent solely because the budget allows it. Delegation must have a bounded scope and a verification result.

## Adaptive execution

Prefer `direct` for focused or tightly coupled work, `probe` for isolated read-only investigation, `fan_out` only for genuinely independent packages, and `audit` for high-risk independent review. A delegated contract must declare objective, inputs, ownership, output artifact, verifier, stop condition, and escalation boundary. Use one writer per file or contract; parallel writers require isolated branches or worktrees.

## Provider adapters

The router output can be consumed by Codex CLI, Claude Code, or Antigravity/Gemini as a local JSON planning step. Do not assume that a model name is portable between providers. Provider-specific model selection belongs in the provider configuration, and an unavailable model must fail closed rather than silently downgrade a critical review.

## Non-goals

- No global shell interception.
- No semantic compression of source code or operational data.
- No automatic activation of hooks, MCP servers, proxies, or third-party installers.
- No replacement of full logs, errors, diffs, or migration plans with summaries.
