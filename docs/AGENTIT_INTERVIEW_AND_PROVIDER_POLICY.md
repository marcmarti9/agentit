# Agentit interview, effort, and provider-neutral execution policy

Agentit owns the work protocol. Providers own only the execution primitive used to satisfy that protocol.

## 1. Product work interviews by default

For Agentit, any task that **creates or changes product behavior or a meaningful implementation decision** must pass `interview-me` before planning or implementation.

This includes features, pages, components, UX, visual design, architecture, APIs, data models, workflows, copy, positioning, automations, and refactors where more than one materially different outcome is possible.

The interview can be tiny. A clear low-complexity change may need only one confirmation. The requirement is alignment, not ceremony.

### Mechanical bypass

Interview may be skipped only for exact mechanical chores whose purpose is to save time and which do not encode a product decision, for example:

- create explicitly named directories/files;
- exact move/rename operations;
- run a specified command or test;
- deterministic formatting;
- copy exact content to a known destination.

If unsure whether the task is mechanical, treat it as product-affecting and interview.

Facts belong to the agent: inspect the repo, docs, runtime, connected tools, or live sources. Decisions/preferences belong in the interview.

## 2. Every product interview selects an effort level

Canonical machine-readable catalog: `effort/levels.yaml`.

The user must explicitly confirm one of three levels before implementation:

### Standard

Efficient production-quality execution. Minimal research, one agent by default, focused implementation, proportional testing/browser checks, and strong context discipline.

Typical rough total model-token envelope: **15k-80k**.

### Polished

Higher-quality execution with targeted research, stronger edge-case coverage, more visual/interaction polish, more iterations, and 0-2 specialists when they provide concrete value.

Typical rough total model-token envelope: **50k-250k**.

### Studio

Quality-first execution for flagship/high-ambition work. Deep discovery, broad relevant research, multiple concepts when useful, specialists/model diversity, independent critique, performance/browser loops, and extensive polish.

Typical rough total model-token envelope: **150k-800k+**.

These ranges are estimates across the parent plus delegated calls, not precise billing forecasts. Actual usage depends on task size, provider, model, tool output, context, retries, and implementation complexity.

### Recommendation requirement

The agent does not ask `Standard, Polished or Studio?` without guidance. It recommends one and explains:

- why it fits the task;
- what the result should look like at each relevant level;
- rough token envelope / relative cost;
- expected research, specialist, and iteration depth;
- what is gained or lost by moving up/down.

The user may override the recommendation.

Studio is not automatically recommended for design. Standard is not automatically recommended for cheap/simple work. The criterion is marginal value from additional effort.

## 3. Adaptive interview depth

Mandatory interview does not mean mandatory long interview.

- clear small product change: one short confirmation may be enough;
- one material unknown: ask it plus effort level;
- several independent unknowns: one frontier round;
- open-ended product/design/architecture task: deeper interview until the material frontier is closed.

Questions should carry a recommendation/default so the user can react quickly.

Stop when meaningful decisions are resolved, the effort level is confirmed, and further answers are unlikely to change the result materially.

## 4. Effort controls spend, not correctness

Standard/Polished/Studio control how much research, context, delegation, concept exploration, iteration, and review Agentit spends.

They do not lower the correctness or safety floor.

If the work becomes more complex than expected and materially exceeding the selected level would be useful, ask before escalating. Explain the expected added token/time cost and specific benefit.

Do not silently turn Standard into Studio. Do not knowingly ship unsafe or incorrect work merely to preserve the selected budget.

## 5. Provider-neutral specialist contract

A specialist in `agents/catalog.yaml` is a logical capability bundle, not a Claude-specific subagent or Codex-specific worker.

The parent chooses the best available execution mode:

1. native subagent/worker from the current provider/client;
2. isolated delegated model/tool call;
3. separate fresh-context invocation;
4. direct execution in the parent with the specialist skill bundle.

The specialist contract remains equivalent:

- objective and done condition;
- role (`implementer`, `probe`, `reviewer`);
- confirmed effort level;
- task-scoped skills;
- allowed inputs/write ownership;
- constraints/risk;
- expected output schema;
- verification and stop condition.

Do not assume provider-specific names or APIs in shared Agentit policy.

## 6. Cross-provider compatibility target

Agentit should remain usable with OpenAI, Anthropic, Google, xAI, and other compatible coding-agent environments.

Graceful degradation is required. If native delegation is unavailable, the parent applies the same specialist capability directly. Multi-agent execution is an optimization, never a correctness dependency.

Likewise, MCP/tool integrations are optional capabilities. Use an equivalent available tool or report the missing capability explicitly rather than breaking shared orchestration.

## 7. Non-interactive execution

CI, scheduled runs, autonomous loops, and other non-interactive contexts cannot fabricate user confirmation.

If a task qualifies only for mechanical bypass, proceed. If product-affecting work requires intent/effort confirmation that is not already explicitly supplied, report a blocker instead of guessing.
