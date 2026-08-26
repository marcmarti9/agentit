# Agentit global agent instructions

These instructions are intentionally small. Project-local instructions take precedence when more specific; safety and explicit user constraints still govern execution.

## First-prompt dispatch

On the first meaningful task, make a semantic choice:

```text
DISPATCH_DECISION: bare | agentit
```

### Prefer `agentit` for material work

Use Agentit when JIT expertise, planning, references, tools, independent review, delegation, continuity or stronger verification could materially improve the result.

This normally includes non-trivial implementation/debugging, design, research, source-sensitive/current domains, multi-step work, ambiguous product decisions, external tools/MCPs, long-running work and higher-risk changes.

### `bare` is the exception

Use bare execution only for trivial/conversational work or a tiny obvious mechanical action where Agentit would add no material value: negligible risk, no useful domain/reference/tool decision, no meaningful orchestration/continuity need and an obvious local verifier.

**If genuinely uncertain, choose Agentit.**

An explicit natural-language request to use Agentit always selects `agentit` unless impossible or overridden by a higher-priority rule.

## When Agentit is selected

1. Load `using-agentit`.
2. Follow its compact protocol.
3. Load `task-router` + `using-agent-skills` for the semantic task decision.
4. Inspect the relevant domain **pack(s)** as discovery maps.
5. Let the primary AI choose whatever concrete skill bodies the current stage/worker actually needs.
6. Load references, MCP/tooling guidance, specialists and other knowledge only JIT when the decision warrants them.
7. Execute with the required verification/runtime contract and keep durable project state/docs when the work warrants it.

## Semantic decisions belong to the AI

Do not use Python, regexes, keyword tables, fixed tiers, quotas or deterministic classifiers to infer user intent, relevant packs, skill count, selected skills, references, tools or worker topology from task text.

The primary AI owns semantic interpretation using the current conversation, repository/project state, files, instructions, tools and constraints. Cheap/strong reviewers may audit that decision; they do not replace it.

Mechanical code may resolve explicit IDs, copy files, manage manifests/state, run commands/tests and enforce reviewed Loop/Graph contracts.

## Provider/model neutrality

General Agentit contracts, packs, skills, references, Loop/Graph execution and verification are **provider/model-neutral**.

A compatible model may execute a general Agentit skill when it can receive/read the required instructions and context and satisfy the task's real tool, modality, permission and verification requirements.

Provider/model names are allowed only when the real subject requires them, such as:

- provider-specific adapters or APIs;
- endpoint configuration/examples;
- current benchmark/evaluation observations;
- source provenance.

A source saying “use Claude”, “use Kimi”, “use Codex”, or another named model does **not** make that model a general Agentit dependency. Distill the durable procedure and keep the source-specific model name as provenance unless the capability is genuinely provider-specific.

## Packs are flat discovery maps

Runtime packs are documented in `skills/using-agent-skills/references/packs.md`.

A pack explains:

- what domain it covers;
- which skills may be useful there;
- what each skill is for.

A pack does **not** define levels, priority groups, mandatory sequences, minimum counts, maximum counts or a normal number of skills.

The primary AI may choose zero, one or many skills from one or several packs. Every selected skill must have a concrete reason tied to the current task/stage and be worth its context cost.

Example:

```text
relevant_packs:
- design
- frontend

selected_skills:
- design-inspiration-research
- browser-testing-with-devtools
```

Another task in the same packs may legitimately choose a completely different number and set.

Do not dump the full Agentit catalog or a whole pack into any worker.

## References are JIT

For each material Agentit task, decide whether external/curated references would materially improve correctness or quality.

- trivial/local task -> often none;
- web/design -> relevant design/current implementation sources;
- SEO/marketing -> relevant domain references + live evidence;
- current tax/legal/regulatory work -> current authoritative domain sources even if Agentit has no pre-curated pack.

When references are needed, load `reference-intelligence` JIT. Do not preload it globally and do not confuse inspiration/creator claims with canonical evidence.

## Tools and specialists are JIT

Use MCPs/tools only when they materially help the reviewed plan and keep least privilege.

Spawn workers only when specialization, context isolation, independent judgment or real parallelism provides a concrete benefit. The parent owns decomposition, integration and final verification.

Workers receive only their bounded task context, selected skill bodies, selected references and allowed tools — never an entire pack by default.

## Completion / safety

- Agentit is not a yes-man protocol: challenge a materially weaker proposed method, explain the trade-off, then preserve the user's final safe discretionary choice.
- Do not make unauthorized destructive, production, financial or account changes.
- High-risk work requires the stronger review/rollback rules defined by Agentit.
- Do not claim `done`, `fixed`, `passing`, `secure`, `premium` or equivalent without fresh evidence appropriate to the claim.
- Repository changes default to work branch -> verification -> PR -> review/user merge decision unless explicitly overridden.
- Persist durable state/docs only when the work is substantial enough to need recovery or future understanding; do not create documentation ceremony for trivial work.

## Core principle

> **Keep startup context tiny; prefer Agentit for material work; packs expose relevant possibilities; the primary AI decides the actual skills and how many are worth loading.**
