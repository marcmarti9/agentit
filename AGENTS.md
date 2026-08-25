# Agentit global agent instructions

These are intentionally small. Project-local instructions take precedence when more specific; safety and explicit user constraints still govern execution.

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
4. Choose a domain **pack** and `essential | standard | deep` discovery depth.
5. Load only the concrete skill bodies the current stage/worker needs.
6. Load references, MCP/tooling guidance, specialists and other skills only JIT when the decision warrants them.
7. Execute with the required verification/runtime contract and keep durable project state/docs when the work warrants it.

## Semantic decisions belong to the AI

Do not use Python, regexes, keyword tables or deterministic classifiers to infer user intent, pack/depth, relevant skills, references, tools or worker topology from task text.

The primary AI owns semantic interpretation using the current conversation, repository/project state, files, instructions, tools and constraints. Cheap/strong reviewers may audit that decision; they do not replace it.

Mechanical code may resolve explicit IDs, copy files, manage manifests/state, run commands/tests and enforce reviewed Loop/Graph contracts.

## Packs are not context bundles

Runtime packs are documented in `skills/using-agent-skills/references/packs.md`.

`pack + depth` defines a candidate search scope. It never means “load every skill in this pack”. A spawned worker receives only its selected skill bodies and bounded task context.

Example:

```text
pack: design
depth: deep
selected_skills:
- design-inspiration-research
- scrollytelling-web
- browser-testing-with-devtools
```

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

## Completion / safety

- Do not make unauthorized destructive, production, financial or account changes.
- High-risk work requires the stronger review/rollback rules defined by Agentit.
- Do not claim `done`, `fixed`, `passing`, `secure`, `premium` or equivalent without fresh evidence appropriate to the claim.
- Repository changes default to work branch -> verification -> PR -> review/user merge decision unless explicitly overridden.
- Persist durable state/docs only when the work is substantial enough to need recovery or future understanding; do not create documentation ceremony for trivial work.

## Core principle

> **Keep startup context tiny; prefer Agentit for material work; spend tokens on the domain knowledge the actual task needs, not on the framework itself.**
