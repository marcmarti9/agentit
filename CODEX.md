# Codex adapter

`AGENTS.md` is Agentit's canonical provider-neutral operating contract. Follow it first; use this file only for Codex-specific execution details.

- Make the semantic `bare | agentit` dispatch from the actual task context. No activation phrase is required.
- Keep the primary/parent agent responsible for task interpretation, integration, verification, and the user-facing answer.
- Use Codex subagents only when specialization, context isolation, independent review, or real parallelism materially helps. A fixed multi-agent chain is never required.
- Before delegating, project a bounded Worker Context Contract: objective, scope, selected skill bodies, selected references, tools/permissions, ownership, expected handoff, verifier, and stop condition.
- One writer owns each shared file or mutable resource unless isolation is explicit.

## Optional Codex worker profiles

`.codex/agents/` contains optional convenience profiles for installations where the named models are available:

- `terra_worker` — balanced bounded execution worker.
- `luna_worker` — GPT-6 Luna, execution-only under GPT-6.1 Sol or GPT-6 Sol.

Before selecting Luna, read [its delegation contract](docs/CODEX_SETUP.md). Sol must supply decided steps, bounded paths, acceptance checks and escalation conditions, then inspect the actual result. Luna must not own architecture, product/security decisions, open-ended implementation/research, independent review or supervision. Context size and writing volume are not selection criteria. This limit also applies to explicit model overrides and differently named roles; an unavailable profile does not waive it.

They are adapters, not Agentit dependencies. If a profile/model is unavailable, use a host-native worker and project the same Agentit worker contract instead. Model availability and the primary model configuration are machine-local concerns and belong in the user's Codex configuration.

Agentit installation and updates should use the portable bootstrap path documented in the README. Legacy shell helpers may exist for compatibility, but they are not part of the semantic task-routing contract.
