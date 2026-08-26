# About Agentit

Agentit is an **open-source, provider-neutral reliability and just-in-time expertise layer for capable AI agents**.

It is not a coding model and does not try to replace the native reasoning, tool use or provider runtime of Codex, Claude Code, Gemini or another compatible host. Agentit adds a portable operating contract around them: model-owned task decisions, JIT skills/references/tools, bounded delegation, independent review, deterministic execution contracts, fresh verification, private resumable state, durable documentation and reviewable Git handoffs.

The [README](README.md) is the canonical public introduction and installation guide. This document explains the design identity behind it.

## Design identity

### AI judgment stays with the AI

Agentit deliberately does **not** use regexes, keyword scores or a Python classifier to infer natural-language intent, risk, topology, pack, skill count or the right tool from a prompt.

The active primary model sees the real conversation/project context and produces `TASK_DECISION`. Deterministic software then enforces the parts that are genuinely mechanical: manifests, capability resolution, permissions, runtime state, receipts, verification probes, continuity artifacts and safe configuration changes.

Independent models can review material decisions when fresh judgment materially improves reliability; stronger gates apply to high-consequence work.

### Orchestration must earn its cost

Agentit has no fixed `Architect -> Manager -> Supervisor -> Worker` pyramid.

Delegation is useful when it creates a concrete advantage such as specialist expertise, independent criticism, parallel read-only investigation, context isolation, independent alternatives or bounded implementation ownership. Tightly coupled work can remain direct. Multi-node work gets explicit ownership/dependencies through a Graph Contract rather than an invisible hierarchy.

The role documents and specialist catalog are optional capabilities/adapters, not mandatory runtime stages.

### Skills are available JIT, not sprayed into context

A globally discoverable Agentit installation exposes only the tiny core needed to decide whether Agentit is useful and, when selected, to discover the relevant semantic map. Profiles are installation/discovery conveniences; they are **not runtime context bundles**.

The primary AI chooses zero, one or many concrete skill bodies from one or more semantic packs according to the current task/stage. A skill is not considered used merely because its ID appears in a profile or catalog.

External ideas are curated rather than bulk-imported. Prefer strengthening an existing capability or adapting the smallest reusable upstream insight with provenance; promote new permanent surface area only when it earns its context and maintenance cost.

See [`docs/SKILL_CURATION.md`](docs/SKILL_CURATION.md) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Core layers

```text
first-prompt dispatch: bare | agentit
                 |
                 v
semantic TASK_DECISION
(packs, skills, references, tools, risk, complexity, topology, plan, verifier)
                 |
                 v
bounded independent review when warranted
                 |
                 v
JIT capability projection
(skills + references + tools/MCPs + workers + least privilege)
                 |
                 v
deterministic execution support
(Loop/Graph contracts + receipts + verification)
                 |
                 v
private continuity + durable docs + Git review
```

### Semantic policy

The primary AI owns task interpretation. Packs are maps, not levels. There is no generic `essential/standard/deep` pack depth, fixed skill count, activation powerword or programmatic natural-language router.

### JIT capabilities

Skills, Reference Intelligence, MCP/tool selection, model routing and specialist/worker contracts are loaded only when the reviewed task benefits from them. Workers receive bounded project instructions, selected skill bodies/references and a least-privilege capability envelope rather than the parent/global context dump.

### Mechanical execution

Executable work can use Loop Contracts with observable goals, verifiers, stop conditions, bounded attempts and escalation. Multi-node work uses Graph Contracts with explicit dependencies, handoff artifacts and write ownership. Deterministic runtime validates those explicit contracts; it does not decide what the user meant.

### Continuity and documentation

Substantial/resumable operational state defaults to ignored private files such as `.agentit/STATE.md`, `.agentit/checkpoints/` and other `.agentit/` runtime artifacts. It should survive session/provider/machine handoffs without turning transient working notes into public repository documentation.

Tracked Markdown is reserved for durable architecture, interfaces, decisions, operations, troubleshooting and verification knowledge introduced or materially changed by the work.

## Safety posture

Agentit's own managed operations are explicit and reversible where their contracts claim that behavior, but Agentit cannot retroactively sandbox credentials/tools that a host already exposed too broadly.

- canonical bootstrap and managed profile/MCP configuration are plan-first before apply;
- continuity/checkpoint commands intentionally write private project-local state;
- verification separates planning from probe execution/receipt creation;
- capability envelopes are least-privilege runtime contracts that host adapters must actually enforce;
- high-risk external/destructive/auth/production work follows stronger human and independent-review gates;
- provider credentials, machine secrets and mutable local state must never be committed.

See [SECURITY.md](SECURITY.md) and [`docs/CAPABILITIES.md`](docs/CAPABILITIES.md).

## Provider neutrality

The shared protocol and skills remain provider-neutral. Provider adapters are deliberately thin and may expose different mechanics or maturity. Named models/providers are valid in adapters, endpoint configuration, provenance and evaluation evidence—not as hidden requirements of general Agentit semantics.

The canonical Python bootstrap targets macOS and GNU/Linux; older shell compatibility paths have narrower portability.

## Evidence posture

Agentit is early-stage. Mechanical contracts can be implemented and tested deterministically; claims that Agentit universally improves quality, token use, latency, cost or reliability require controlled agent-level comparative evidence.

Public claims therefore distinguish:

- **implemented/tested contract** — backed by code/tests for the cited revision;
- **design hypothesis** — a reason the architecture may help;
- **comparative claim** — requires paired baseline/treatment agent runs.

See [`evals/evaluation-plan.md`](evals/evaluation-plan.md) and the tracked comparative-evaluation work.

## Open source

Agentit is licensed under the [Apache License, Version 2.0](LICENSE).

- [README](README.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)
