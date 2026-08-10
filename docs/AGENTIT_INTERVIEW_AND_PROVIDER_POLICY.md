# Agentit interview, effort, continuity, and provider-neutral execution policy

Agentit owns the work protocol. Providers own only the execution primitive used to satisfy that protocol.

## 1. Product work interviews by default

Any task that creates or changes product behavior or a meaningful implementation decision must pass `interview-me` before planning or implementation.

This includes features, pages, components, UX, visual design, architecture, APIs, data models, workflows, copy, positioning, automations, and refactors where more than one materially different outcome is possible.

Interview may be skipped only for exact mechanical chores whose purpose is to save time and which do not encode a product decision: exact file/directory creation, moves/renames, specified command/test execution, deterministic formatting, or exact copying.

If unsure, interview.

Facts belong to the agent: inspect repo, docs, runtime, tools, and live sources. Decisions/preferences belong in the interview.

## 2. Batch every currently identifiable material question

Agentit optimizes for low conversational latency. After inspecting discoverable facts, the agent must assemble **all material user decisions it can currently identify** and ask them in one numbered batch.

Each question carries a recommendation/default. The Standard/Polished/Studio recommendation belongs in the same batch.

Preferred flow:

`inspect facts -> one comprehensive interview batch -> user answers -> persist confirmed state -> plan/build`.

A follow-up batch is allowed only when answers expose genuinely new material decisions that could not reasonably have been formulated beforehand. Do not drip-feed known questions one message at a time.

For tiny product changes, the batch may contain only one or two confirmations.

## 3. Every product interview selects an effort level

Canonical machine-readable catalog: `effort/levels.yaml`.

### Standard

Efficient production-quality execution. Minimal research, one agent by default, focused implementation, proportional testing/browser checks, and strong context discipline.

Typical rough total model-token envelope: **15k-80k**.

### Polished

Higher-quality execution with targeted research, stronger edge-case coverage, more visual/interaction polish, more iterations, and 0-2 specialists when they provide concrete value.

Typical rough total model-token envelope: **50k-250k**.

### Studio

Quality-first execution for flagship/high-ambition work. Deep discovery, broad relevant research, multiple concepts when useful, specialists/model diversity, independent critique, performance/browser loops, and extensive polish.

Typical rough total model-token envelope: **150k-800k+**.

These ranges are estimates across parent + delegated calls, not billing forecasts.

The agent must recommend a level and explain why, what lower/higher levels change, rough token envelope/relative cost, likely research/specialist/iteration depth, and what is gained/lost. The user may override.

## 4. Effort controls spend, not correctness

Standard/Polished/Studio control research, context, delegation, concept exploration, iteration, and review. They do not lower the correctness or safety floor.

If work becomes more complex than expected and materially exceeding the selected level would help, ask before escalating. Do not silently turn Standard into Studio.

## 5. Continuity is mandatory for product work

Chat/session memory is disposable. Product work must remain resumable after session loss, token/context exhaustion, provider/model switch, machine switch, crash, or long pause.

Canonical policy: `docs/PROJECT_CONTINUITY.md`.

Default project state file: `docs/agentit/STATE.md`, unless the project already has an equivalent canonical state document.

After interview confirmation and throughout execution, persist enough compact operational state for a fresh agent to recover:

- objective and rationale;
- confirmed intent/audience/success/constraints/non-goals;
- confirmed effort level;
- current status;
- durable product/technical/design decisions;
- important files/artifacts;
- current branch and PR;
- verification commands/results;
- next executable actions;
- open questions/blockers.

Update state after important decisions/milestones and before any handoff or expected/forced stop. Do not persist secrets, credentials, raw chain-of-thought, full transcripts, or giant tool dumps.

Before continuing prior work, read continuity state before asking the user to repeat decisions.

## 6. PR-first repository workflow

Repository mutation defaults to:

`work branch -> commits -> verification -> pull request -> review/user merge decision`.

Do not commit directly to or fast-forward the default branch and do not merge a PR automatically unless the user explicitly authorizes that exception for the task or project instructions explicitly require another workflow.

Continuity/documentation updates belong on the same work branch/PR as implementation.

## 7. Provider-neutral specialist contract

A specialist in `agents/catalog.yaml` is a logical capability bundle, not a Claude-specific subagent or Codex-specific worker.

Execution fallback:

1. native subagent/worker;
2. isolated delegated model/tool call;
3. separate fresh-context invocation;
4. parent executes with the same specialist skill bundle.

The contract remains equivalent: objective/done condition, role, effort level, task-scoped skills, allowed I/O/write ownership, constraints/risk, expected output, verification, stop condition, and continuity handoff where needed.

Multi-agent execution is an optimization, never a correctness dependency.

## 8. Cross-provider compatibility target

Agentit should remain usable with OpenAI, Anthropic, Google, xAI, and other compatible coding-agent environments. Shared policy must describe semantic capabilities, not require one vendor's terminology or API.

MCP/tool integrations are optional capabilities. Use an equivalent tool or report missing capability instead of breaking the shared workflow.

## 9. Non-interactive execution

CI, scheduled runs, autonomous loops, and other non-interactive contexts cannot fabricate user confirmation.

If a task qualifies only for mechanical bypass, proceed. If product-affecting work requires intent/effort confirmation not already supplied/documented, report a blocker instead of guessing.
