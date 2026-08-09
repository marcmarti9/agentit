# Agentit interview + provider-neutral execution policy

Agentit owns the work protocol. Providers own only the execution primitive used to satisfy that protocol.

## Interview gate

For any non-trivial task, the parent agent must decide whether the request is sufficiently specified before planning or implementation.

Use `interview-me` when missing decisions could materially change architecture, scope, UX, visual direction, success criteria, constraints, audience, risk, or cost. The goal is not to ask questions by habit; the goal is to avoid silently committing to expensive assumptions.

Rules:

- Look up facts in the repo/tools instead of asking the user.
- Ask the user for decisions, preferences, and tradeoffs that cannot be inferred safely.
- Interview as much as needed for a high-confidence result when the task is expensive to reverse or the user explicitly asks for the best possible outcome.
- Prefer one sharp question at a time when answers are dependent; use a frontier round for several independent unresolved decisions.
- Attach a recommended/default answer so the user can react instead of inventing from scratch.
- Stop when further questions are unlikely to change the implementation materially.
- Do not block trivial/mechanical work with ceremonial interviews.

For high-ambition design work, interview dimensions should include when relevant: brand personality, audience, conversion/information goal, desired emotional effect, references to embrace/avoid, content/assets, appetite for unusual interaction, performance/device constraints, accessibility expectations, and how much visual risk is acceptable.

## Provider-neutral specialist contract

A specialist in `agents/catalog.yaml` is a logical capability bundle, not a Claude-specific subagent or a Codex-specific worker.

The parent agent chooses the best available execution mode in this order:

1. native subagent/worker capability offered by the current provider/client;
2. an isolated delegated model/tool call available through the host environment;
3. a separate fresh-context invocation if the environment supports it;
4. direct execution in the parent with the specialist's skill bundle loaded.

The specialist contract remains the same regardless of provider:

- objective and done condition;
- role (`implementer`, `probe`, `reviewer`);
- task-scoped skills;
- allowed inputs and write ownership;
- constraints and risk;
- expected output schema;
- verification and stop condition.

Do not assume provider-specific names such as Claude subagents, Codex workers, Gemini agents, Grok workers, or any particular tool API in shared Agentit policy. Provider-specific adapters may map these concepts locally, but shared skills and catalogs should describe capabilities semantically.

## Cross-provider compatibility target

Agentit should remain usable with model families and clients from OpenAI, Anthropic, Google, xAI, and other providers that can read repository instructions and execute normal coding-agent workflows.

Graceful degradation is required: if a provider cannot spawn a specialist, the parent must still be able to apply the same specialist skill bundle directly. Multi-agent execution is an optimization, never a correctness dependency.

Likewise, MCP/tool references are optional capabilities. A task must either use an equivalent available tool or explicitly report the missing capability; shared reasoning and skill selection must not fail merely because one provider lacks a particular integration.
