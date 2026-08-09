---
name: architect-orchestrator
description: Choose direct work or bounded delegation after interview and effort selection. Use for coupling, parallelism, specialist agents, or independent review.
---

# Adaptive Agent Architecture

## Core rule

Agentit is **interview-first for product work, efficient by default, and effort-aware**.

Before choosing topology:

1. classify mechanical bypass vs product-affecting work;
2. product-affecting work must pass `interview-me`;
3. the user confirms an effort level from `effort/levels.yaml`: `standard`, `polished`, or `studio`;
4. choose topology and context spending consistent with that level.

Use one capable agent by default. Add agents only when context isolation, parallelism, specialization, permissions, creative diversity, or independent verification provide concrete benefit greater than coordination overhead.

## Effort-aware orchestration

Effort level controls **how much exploration and coordination is justified**, not whether correctness matters.

### Standard

- default topology: direct;
- subagents: zero by default, usually at most one clearly valuable specialist;
- research: only when facts/current information are needed;
- concept alternatives: none or one direct approach;
- verification: focused, proportional;
- optimize strongly for context/token efficiency.

### Polished

- direct remains preferred, but 0-2 specialists are normal when useful;
- targeted research and approach comparison are allowed;
- independent reviewer/probe can be worthwhile;
- several critique/fix cycles are reasonable;
- spend more context where it produces visible quality or risk reduction.

### Studio

- quality dominates token thrift;
- 2-5 specialists/fan-out can be justified, never ceremonial;
- broad relevant research, model diversity, concept competition, and independent critique are allowed;
- implementation may run repeated visual/performance/review loops until remaining gains are marginal;
- still keep one writer per shared file/state and avoid pointless agent chatter.

Typical rough total model-token envelopes from `effort/levels.yaml`: Standard ~15k-80k, Polished ~50k-250k, Studio ~150k-800k+. These are estimates, not quotas or guarantees.

If execution wants to materially exceed the confirmed level, the Architect must ask before escalating unless safety/correctness requires extra work.

## Mechanical bypass

Purely mechanical tasks with no product decision may skip interview and effort selection: exact mkdir/file creation, exact rename/move, deterministic formatting, running explicitly requested commands/tests, copying exact content.

Do not call a task mechanical merely because it is small. Any choice about behavior, UX, architecture, copy, API, data model, or product outcome is product-affecting.

## Provider-neutral execution model

Agentit defines semantic roles and contracts, not branded orchestration primitives. A Specialist is not inherently a Claude subagent, Codex worker, Gemini agent, Grok worker, or any other provider-specific construct.

Use the best execution primitive available:

1. native subagent/worker support;
2. isolated delegated model/tool invocation;
3. separate fresh-context invocation;
4. direct parent execution with the same specialist skill bundle.

Objective, skills, constraints, allowed I/O, expected output, verification, and stop condition remain equivalent. Multi-agent execution is an optimization, never a correctness dependency.

Shared policy must remain usable across OpenAI, Anthropic, Google, xAI, and future compatible coding-agent clients.

## Roles

Roles are capabilities, not a mandatory org chart:

- **Architect**: user-facing owner, router, decision maker, final integrator.
- **Orchestrator**: coordinates a real DAG when multiple packages genuinely require it.
- **Worker**: bounded executor with strict context and ownership.
- **Specialist**: temporary domain expert from `agents/catalog.yaml`.
- **Auditor/Reviewer**: independent/read-only quality or risk challenge.

## Specialist catalog

When a specialist is useful:

1. choose a role whose domain/triggers fit;
2. project only its listed skills plus minimum task context;
3. map its mode to the available provider execution primitive;
4. require its output contract;
5. return control to the Architect for integration and verification.

Do not create a specialist when loading the same skill in the parent is cheaper and equally effective.

## Routing modes

1. **Direct** — focused/tightly coupled work.
2. **Plan + direct** — broad but sequential work.
3. **Probe** — isolated read-only investigation.
4. **Specialist probe** — bounded domain expert.
5. **Fan-out/fan-in** — independent searches/concepts/packages.
6. **Pipeline** — ordered packages with explicit handoffs.
7. **Writer + reviewers** — one writer, independent reviews.
8. **Design competition** — multiple independent creative concepts, explicit jury, then implementation.
9. **Orchestrated DAG** — several dependent packages with distinct ownership.
10. **Audit** — high-risk gate/arbitration.

Effort-level constraints:

- Standard: normally Direct / Plan+Direct / one Probe.
- Polished: any bounded topology when benefit is clear; avoid large fan-out.
- Studio: full topology set available when justified.
- Design competition is normally Studio-only unless user explicitly requests equivalent exploration.

## Delegation test

Before spawning, evaluate:

- independence;
- coupling/shared mutable state;
- context-isolation benefit;
- real parallel speedup;
- distinct tools/expertise;
- creative diversity;
- independent risk reduction;
- coordination/integration cost;
- whether the confirmed effort level justifies the spend.

If no concrete advantage, stay single-agent.

## Design competition

Use when Studio-level creative concept quality is a major success criterion.

1. interview and confirm intent/effort;
2. shared evidence/reference brief;
3. 2-3 independent concepts, ideally genuinely different in thesis/interaction rather than cosmetic variants;
4. explicit evaluation by brand fit, originality, clarity, usability, feasibility, performance, and memorability;
5. choose one or a justified hybrid;
6. implement;
7. independent visual/performance critique.

Prefer model diversity when available and useful. Do not majority-vote.

## Worker Context Contract

Delegated contexts must receive equivalent semantics regardless of provider:

- objective, scope, done condition;
- optional specialist id;
- confirmed effort level;
- projected project instructions;
- task-scoped skills only;
- safe preferences;
- risk/constraints;
- allowed inputs/write ownership;
- artifact references;
- expected output;
- verification;
- stop/escalation boundary.

Precedence: `safety > explicit user instruction > project instruction > preferences > defaults`.

Never dump the full parent conversation or entire skill catalog into a child. Large outputs should return as artifacts/references plus a compact receipt.

## Concurrency and isolation

- default subagents: zero;
- Standard: usually 0, maximum 1 specialist unless exceptional;
- Polished: usually 0-2;
- Studio: usually 2-5 only where useful;
- default child depth: one generation;
- one writer per file/shared state;
- parallel writers need isolated branches/worktrees;
- the Architect owns user communication and integration.

## Verification by risk and effort

Correctness floor is independent of effort level.

- Low risk: focused checks.
- Medium risk: relevant tests + Architect diff review.
- High risk: mandatory tests plus independent audit where possible; otherwise explicit second-pass audit and disclose limitation.
- Visual Standard: basic rendered check.
- Visual Polished: desktop/mobile/states/interactions.
- Visual Studio: full responsive/motion/accessibility/performance critique and repeated browser loops.

## Mid-task effort escalation

If new complexity makes the confirmed level unrealistic, pause before materially expanding token/agent/research spend.

Explain:

- what staying at the current level means;
- recommended new level;
- rough additional token/time cost;
- specific quality/risk benefit.

Then ask the user to confirm. Safety/correctness may force additional work; disclose that rather than silently cutting corners.

## Model policy

Choose models by capability and role, not provider prestige:

- strongest available judgment: architecture, creative direction, arbitration, hard reviews;
- strong coding model: primary implementation;
- fast/cheap capable model: bounded execution, extraction, variants, browser iterations, repetitive QA;
- different model family: useful for creative diversity/adversarial review.

The effort level controls how often expensive models/context are justified. Standard should not escalate by habit; Studio may use strong models where judgment meaningfully improves the result.

## Anti-patterns

- starting product work without interview + effort confirmation;
- treating `design` as automatically Studio;
- silently turning Standard into a multi-agent research marathon;
- fixed Architect→Orchestrator→Supervisor→Worker bureaucracy;
- one agent per job title;
- spawning the whole specialist catalog;
- assuming one provider's subagent API is required;
- several writers on shared state;
- huge context dumps to workers;
- unbounded correction loops;
- expensive models for mechanical work;
- Studio-level concept competition for routine maintenance.
