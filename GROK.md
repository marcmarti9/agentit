# Grok adapter

`AGENTS.md` is Agentit's canonical provider-neutral operating contract. Follow it first; use this file only for Grok-specific execution details.

- Make the semantic `bare | agentit` dispatch from the actual task context. No activation phrase is required.
- Keep the primary/parent agent responsible for task interpretation, integration, verification, and the user-facing answer.
- **Cold start & Core skills**: Global skill discovery in `~/.grok/skills/` contains ONLY the 3 bootstrap core skills:
  1. `using-agentit`
  2. `task-router`
  3. `using-agent-skills`
- **Just-In-Time (JIT) skill loading**: When a task needs non-core expertise (e.g. `debugging-and-error-recovery`, `frontend-ui-engineering`, `marketing-and-growth`), inspect `references/packs.md` and load the specific `SKILL.md` body directly from `~/.agentit/runtime/skills/<skill-name>/SKILL.md` (or the project repository `skills/<skill-name>/SKILL.md`). Do NOT install all skills globally into `~/.grok/skills/`.
- Use Grok subagents only when specialization, context isolation, independent review, or real parallelism materially helps.
- Before delegating, project a bounded Worker Context Contract: objective, scope, selected skill bodies, selected references, tools/permissions, ownership, expected handoff, verifier, and stop condition.
- One writer owns each shared file or mutable resource unless isolation is explicit.
- High-risk work follows Agentit's review, rollback, and post-check rules.
- Local MCP servers can be configured in `~/.grok/config.toml` under `[mcp_servers.*]` with their `enabled` state managed per task.
