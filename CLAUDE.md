# Claude Code adapter

`AGENTS.md` is Agentit's canonical provider-neutral operating contract. Follow it first; use this file only for Claude Code-specific execution details.

- Make the semantic `bare | agentit` dispatch from the actual task context. No activation phrase is required.
- Keep the primary/parent agent responsible for task interpretation, integration, verification, and the user-facing answer.
- Use Claude Code subagents when specialization, context isolation, independent review, or real parallelism materially helps. Do not force a fixed agent hierarchy.
- Agent files under `agents/` are optional role adapters. Select only a role that fits the reviewed task plan.
- Before delegating, build a bounded Worker Context Contract: objective, scope, selected skill bodies, selected references, tools/permissions, ownership, expected handoff, verifier, and stop condition.
- One writer owns each shared file or mutable resource unless isolation is explicit.
- High-risk work follows Agentit's review, rollback, and post-check rules.
- Machine-local models, plugins, MCP servers, endpoints, permissions, and credentials belong in local Claude configuration, not in this repository.

If Claude Code cannot provide an independent worker required by the plan, degrade visibly: use the parent with the same bounded skills for ordinary delegation, or stop/escalate when genuine independence is a safety requirement.
