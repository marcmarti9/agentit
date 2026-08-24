# Adaptive Agent Architecture

## Overview

Agentit avoids fixed multi-tier hierarchies such as `Architect → Orchestrator → Supervisor → Worker` as mandatory process. A capable primary model owns the user relationship and semantic judgment, then chooses direct execution or a useful multi-node topology from the **actual task context**.

The historical role names (`architect`, `orchestrator`, `supervisor`, `worker`, `auditor`) are reusable capability scopes, not required checkpoints.

Agentit's architecture separates three concerns:

1. **Semantic decision policy** — the primary AI owns `TASK_DECISION`; an independent reviewer challenges material decisions.
2. **Loop Engineering** — deterministic runtime contracts govern bounded executable units.
3. **Graph Engineering** — deterministic runtime contracts govern dependencies, ownership, handoffs, and acceptance for multi-node work.

The boundary is deliberate: **LLMs interpret intent; deterministic code enforces state and invariants after the decision.** There is no heuristic/programmatic natural-language task router deciding risk, topology, skills, or delegation.

See [`NO_PROGRAMMATIC_ROUTER.md`](NO_PROGRAMMATIC_ROUTER.md) and [`LLM_NATIVE_DECISION_PROTOCOL.md`](LLM_NATIVE_DECISION_PROTOCOL.md).

## Why adaptive orchestration?

Fixed agent pyramids create avoidable failure modes:

1. **Context distortion** — requirements are repeatedly summarized across layers.
2. **Latency/coordination overhead** — handoffs cost time even when the work is tightly coupled.
3. **False decomposability** — file count or perceived difficulty gets mistaken for independent work.
4. **Authority ambiguity** — multiple writers or reviewers can silently assume ownership of the same decision/state.

Delegation is justified when it creates a concrete benefit such as:

- independent exploration of materially different approaches;
- context isolation for large source/reference sets;
- specialist expertise or tool access;
- safe parallelism with disjoint ownership;
- fresh independent review/critique;
- read-only investigation that protects the primary model's context.

A small task can stay direct. A large task can also stay direct when its decisions are too tightly coupled to split safely.

## Semantic decision layer

Before material execution, the primary AI creates `TASK_DECISION` from the conversation, repository, files, tools, constraints, and prior state. It includes at least the intended outcome, known facts, material unknowns, risk/reversibility, useful skills/tools, proposed topology, ownership boundaries, implementation plan, and verification strategy.

An independent reviewer returns `CLEAR`, `CHALLENGE`, or `ESCALATE`. High-consequence work or unresolved disagreement gets stronger independent review.

The AI may select `direct`, `probe`, `fan_out`, `pipeline`, `writer_reviewer`, `audit`, or a custom DAG when justified. The runtime does **not** infer that topology from prompt text.

## Loop Engineering

Every executable unit with a verifiable outcome has a bounded Loop Contract:

```text
observable goal → action → fresh evidence → verifier → accept / retry / escalate
```

A loop declares before execution:

- observable goal;
- verifier;
- stop condition;
- bounded attempt budget;
- escalation boundary.

The default runtime budget is two total attempts unless the semantic decision explicitly justifies another bounded value. A retry needs new evidence or a meaningfully different strategy. Never weaken a verifier to manufacture a pass.

Example:

```bash
python3 ~/code/agentit/router/runtime_cli.py loop-init \
  --state .agentit/runtime/loops/<node-id>.json \
  --goal "<observable goal>" \
  --verifier "<verifier>" \
  --stop "<stop condition>"
```

After attempts are recorded, acceptance requires:

```bash
python3 ~/code/agentit/router/runtime_cli.py loop-check \
  --state .agentit/runtime/loops/<node-id>.json
```

Narrative worker success is not acceptance; a passed Loop Receipt is.

## Graph Engineering

When the chosen topology contains more than one execution node, Agentit materializes a DAG before spawning work.

Each node defines:

- stable ID and objective;
- dependency IDs;
- explicit read/write ownership;
- expected handoff artifacts;
- its own Loop Contract.

Graph initialization/validation:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-init \
  --spec .agentit/runtime/graph-spec.json \
  --state .agentit/runtime/graph.json
```

The runtime rejects cycles, unknown/self dependencies, unsafe paths, and overlapping write ownership before execution. Only nodes returned by `graph-ready` may start.

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-ready \
  --state .agentit/runtime/graph.json
```

A completed node must provide its accepted Loop Receipt and required artifacts. Blocked/escalated work is represented explicitly rather than silently routed around.

Final multi-node acceptance requires:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-check \
  --state .agentit/runtime/graph.json
```

The resulting Graph Receipt must be backed by current node receipts.

## Supported topology patterns

| Pattern | Good fit | Ownership |
|---|---|---|
| `direct` | tightly coupled or small work | primary model owns execution |
| `probe` | read-only investigation | no write ownership |
| `fan_out` | independent research/modules/concepts | disjoint writers or read-only nodes |
| `pipeline` | ordered stages with explicit handoffs | one stage owns each output |
| `writer_reviewer` | implementation needing fresh critique | one writer, reviewer read-only |
| `audit` | security/high-impact independent review | auditor read-only |
| custom DAG | multi-package or dependency-heavy work | explicit dependency + ownership graph |

These are vocabulary for the AI's decision, not a deterministic classifier table.

## Structural design alternatives

When a task changes an expensive-to-reverse public interface, module seam, persistence model, protocol, service boundary, or migration strategy, Agentit compares at least two materially different designs before implementation.

Alternatives should differ in seam/ownership/failure model—not merely naming. Compare interface simplicity, hidden complexity, locality of change, testability, operational risk, reversibility, migration cost, and fit with existing conventions.

Independent workers can generate alternatives when fresh context helps. The primary model judges and records the chosen direction.

## Worker Context Contract

Every delegated spawn must pass through the Worker Context Contract (`router/worker_context.py` / `agentit worker build|render`). Fresh context without project rules is not useful isolation.

A worker context projects only what the worker needs:

1. objective and explicit scope/completion criteria;
2. relevant project instruction files such as `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, or `GEMINI.md` when present;
3. task-scoped skill **bodies**, not the whole catalog;
4. safe user preferences when applicable;
5. risk/constraints supplied by the parent decision;
6. allowed read/write paths and artifact references;
7. expected output/evidence, verifier, stop condition, and loop identity;
8. required/preferred capabilities resolved against the actual host inventory.

Directive precedence:

```text
safety > explicit user instruction > project instruction > preferences > defaults
```

Workers must not silently drop project instructions, receive unrelated secrets, or perform commits/pushes/deployments/external mutations outside their authorized scope.

## Ownership rules

- **Single writer per shared path/state.** Parallel writers require disjoint ownership or isolated branches/worktrees.
- **Read-only critics remain read-only.** A reviewer should not mutate the thing it is independently judging unless the parent explicitly changes its role.
- **Parent owns integration.** Worker summaries are evidence inputs, not authority over final acceptance.
- **No nested-agent explosion.** Additional delegation from workers needs an explicit reason and compatible ownership, rather than being a default cascade.

## Risk and review

`RISK_0..RISK_4` is selected by the primary AI and challenged by the independent reviewer. Deterministic runtime code does not infer risk from keywords.

High-consequence areas commonly include destructive operations, production changes, auth, payments, secrets, PII, difficult-to-reverse migrations, and major structural architecture. These require stronger review and more demanding verification/rollback evidence.

## Public visual work

Public landing/homepage/company/brand/storefront work is design-primary when visual direction is material. Studio-level greenfield/total redesign work commonly benefits from:

1. recommendation-led product interview;
2. independent live reference research;
3. materially different design concepts;
4. explicit design-direction selection;
5. one implementation owner;
6. fresh independent visual critique;
7. desktop/mobile runtime verification.

Concept competition must produce different visual/narrative theses, not palette swaps.

## Stop delegating when

- branches are no longer independent;
- coordination cost exceeds specialist/context benefit;
- writers would contend for the same state;
- the remaining work is one tightly coupled integration decision;
- another worker would add hierarchy without new evidence or capability.

## Canonical references

- [`NO_PROGRAMMATIC_ROUTER.md`](NO_PROGRAMMATIC_ROUTER.md)
- [`LLM_NATIVE_DECISION_PROTOCOL.md`](LLM_NATIVE_DECISION_PROTOCOL.md)
- [`RUNTIME_ENGINEERING.md`](RUNTIME_ENGINEERING.md)
- [`CAPABILITIES.md`](CAPABILITIES.md)
- [`PROJECT_CONTINUITY.md`](PROJECT_CONTINUITY.md)
- [`../skills/architect-orchestrator/SKILL.md`](../skills/architect-orchestrator/SKILL.md)
