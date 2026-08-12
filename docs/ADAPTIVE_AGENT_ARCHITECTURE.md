# Adaptive Agent Architecture

## Overview & Core Principles

This system departs from rigid, multi-tier hierarchical delegation models (e.g., Architect → Orchestrator → Supervisor → Worker). Instead, it operates on **intelligent orchestration**: a capable main agent handles tasks directly when that is best, and instantiates multi-agent topologies when justified by context isolation, real parallelism, domain specialization, independent verification/critique, or risk boundaries — without hard min/max subagent quotas and without requiring powerwords.

The historical role names (`architect`, `orchestrator`, `supervisor`, `worker`, `auditor`) are preserved for capability scoping, but represent transient functions rather than mandatory pipeline checkpoints.

The architecture combines three complementary engineering layers:

1. **Harness & Context Engineering**: Environment permissions, tool availability, git worktrees, and context window optimization.
2. **Loop Engineering**: Local execution loops governing how an individual agent plans, acts, collects empirical evidence, verifies, and halts.
3. **Graph Engineering**: Multi-agent connection topologies governing dependencies, artifact handoffs, parallel execution, and recovery strategies.

Graph engineering does not replace the heuristic task router. The router evaluates incoming tasks to determine whether a single execution loop or a multi-node graph is required.

---

## Why Move Away From Fixed Hierarchies?

Fixed hierarchical multi-agent pyramids introduce three major failure modes in software engineering:

1. **Context Bloat & Distortion**: Instructions and context are repeatedly re-summarized across agent layers, degrading fidelity and wasting tokens.
2. **Latency & Overhead**: Unnecessary agent handoffs introduce significant round-trip latency for tightly coupled tasks.
3. **Misaligned Decomposability**: High file counts or complex requirements are often conflated with true task independence. Tightly coupled edits across multiple files are faster and safer when owned by a single agent with a coherent plan.

Multi-agent collaboration provides net-positive value strictly under four conditions:
- **Independent Exploration**: Exploring separate technical approaches without shared state.
- **Context Isolation**: Reading large documentation sets or log outputs that would contaminate the main working context.
- **Permission & Tool Boundaries**: Running execution steps under isolated sub-permissions or isolated git worktrees.
- **Independent Verification**: Performing adversarial code reviews or security audits with fresh, unbiased context.

---

## Layer 1: Loop Engineering

Every execution unit runs inside a local, bounded loop:

```
[ Verifiable Goal ] ──► [ Action ] ──► [ Empirical Evidence ] ──► [ Verification ] ──► [ Converge / Halt ]
```

A valid execution loop must declare before starting:
- **Observable Completion Criteria**: Exact measurable outcome.
- **Verifier Engine**: Automated test suite, linter, type-check, empirical command output, or structured diff.
- **Minimal Persistent State**: Key decisions and milestone artifacts.
- **Recovery & Fallback Strategy**: Action plan upon verification failure.
- **Iteration Ceiling**: Maximum loop count (default: 1 automatic retry after a failure).
- **Escalation Boundary**: Explicit condition for returning control to the primary agent or human operator.

### Loop Execution Rules

- **Single Auto-Retry**: A worker is allowed a maximum of one automatic correction attempt following a verifiable test/build failure.
- **Evidence-Based Retries**: A second retry requires fresh empirical evidence or an alternative implementation strategy.
- **Bounded Objectives**: Never use open-ended goals such as "continue until perfect".
- **Writer/Reviewer Separation**: Writer and reviewer roles must be separated when independent context outweighs coordination cost.
- **Verifier Integrity**: If a verifier fails to detect progress, fix the verifier before proceeding with code changes.

---

## Layer 2: Graph Engineering

When a task naturally decomposes into separate work units, the workflow is structured as a Directed Acyclic Graph (DAG). Each node represents a bounded loop containing:

- Specific objective and inputs.
- Defined file read/write scope and ownership.
- Expected output artifact or schema.
- Automated verifier and stop condition.

Edges in the graph represent verified artifact dependencies or completion signals.

```
                         ┌───────────────────────┐
                         │   Primary Architect   │
                         └───────────┬───────────┘
                                     │ (Plan & Decompose)
                         ┌───────────┴───────────┐
                         │   Task DAG Router     │
                         └───────────┬───────────┘
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           ▼                         ▼                         ▼
┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐
│  Worker A (Module) │    │  Worker B (Module) │    │  Worker C (Tests)  │
└──────────┬─────────┘    └──────────┬─────────┘    └──────────┬─────────┘
           │                         │                         │
           └─────────────────────────┼─────────────────────────┘
                                     ▼
                         ┌───────────────────────┐
                         │  Join & Verification  │
                         └───────────────────────┘
```

### Graph Governance

- **Deterministic DAGs**: Prefer linear pipelines and parallel fan-outs. Cycles are strictly restricted to bounded local repair loops around a verifier.
- **Single-Writer Rule**: Exactly one agent owns write permissions for any given file or contract at a time. Parallel writers must work in isolated git worktrees or branches.
- **Runtime Precedence**: While LLMs may propose routing, the runtime engine enforces dependency ordering, ownership boundaries, and maximum iteration caps.

---

## Supported Topologies

| Topology | Best For | Ownership Rule |
|---|---|---|
| **Direct** | Focused, small, or tightly coupled edits | Primary agent owns plan, code, & testing |
| **Plan + Direct** | Sequential multi-step implementations | Single owner with milestone checkpoints |
| **Probe** | Read-only investigation, bug location | Read-only access; returns evidence |
| **Fan-Out / Fan-In** | Truly independent modules/files | One owner per isolated file/artifact |
| **Pipeline** | Sequential stage dependencies | Each stage consumes validated artifacts |
| **Writer + Reviewers** | Implementation requiring fresh review | Single writer; reviewers read-only |
| **Orchestrated DAG** | Multi-package features with complex graph | Explicit artifact contracts & worktrees |
| **Independent Audit** | High-risk (security, auth, migrations) | Read-only auditor with fresh context |

---

## Delegation Contract

Every delegated spawn **must** pass through the Worker Context Contract runtime
(`router/worker_context.py` / `agentit worker build|render`). Fresh context
without projecting project instructions is **fresh negligence** (see GSD #671
class failures).

### Required projection (auditable)

Before spawning a worker, produce an auditable `worker_context` object:

1. Objective and explicit scope / completion criteria.
2. Project instruction files discovered at the repo root (and optional work subdir):
   `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `GEMINI.md`.
3. Task-scoped active skills only — never the full global catalog.
4. Applied user preferences (safe style keys only; no secrets).
5. Risk classification and mandatory constraints (`no commits` / `no pushes` /
   `no external changes` unless explicitly authorized).
6. Allowed read/write paths and recoverable artifact URIs.
7. Expected output format, verification command, stop / escalation conditions.

Precedence when directives conflict:

```text
safety > explicit user instruction > project instruction > preferences > defaults
```

### Forbidden

- Silently dropping project instructions for a “clean” subagent.
- Dumping every global skill into the worker.
- Forwarding secrets unrelated to the task.
- Commits, pushes, or external changes unless the contract authorizes them.

*Subagents do NOT receive full conversation history or unrelated documentation.*
Large logs or outputs are persisted to disk and passed via file references.

Build / inspect:

```bash
agentit worker build "Add settings page" security-and-hardening,frontend-ui-engineering
agentit worker render "Review auth diff"
python3 router/worker_context.py build --project . --objective "..." --skill security-and-hardening
```

---

## Operational Budgets & Limits

- **Default posture**: intelligent — stay solo when coupled; spawn when structure shows benefit.
- **No hard min/max subagent caps**: router `subagents.recommended` is advisory only.
- **Critic gate**: large structural plans require an independent critic before implementation commitment.
- **Nesting Depth**: 1 level deep by default (subagents do not spawn sub-subagents).
- **Single Writer**: 1 writer per file, module, or shared contract.
- **Failure Escalation**: 1 automatic retry per worker failure before escalating back to coordinator.
- **Craft depth**: Standard/Polished/Studio applies to design/visual work only.
- **Skill budget**: always_core + task `load_now` only; never the full catalog.

---

## Risk & Quality Assurance Levels

Verification requirements scale with inferred task risk:

- **Low Risk (RISK_1)**: Focused implementation checks by primary agent.
- **Medium Risk (RISK_2)**: Relevant unit/integration tests and diff review by primary agent.
- **High Risk (RISK_3 / RISK_4)**: Mandatory automated test suites, diff inspection, and independent read-only audit.

*High-risk areas include: Authentication, secrets, RLS policies, destructive DB migrations, financial calculations, core domain logic, and public API contracts.*

---

## References

- Anthropic, *How we built our multi-agent research system*.
- Anthropic, *Effective context engineering for AI agents*.
- OpenAI, *How OpenAI uses Codex* & *Symphony*.
- Google, *Subagents have arrived in Gemini CLI*.
- Microsoft, *Multi-agent patterns* & *Orchestrator and subagent pattern*.
- Ruan et al., *AOrchestra: Automating Sub-Agent Creation for Agentic Orchestration*, 2026.
- Sarker et al., *GraphBit: A Graph-based Agentic Framework for Non-Linear Agent Orchestration*, 2026.
- Qi et al., *LLM-as-Code Agentic Programming for Agent Harness*, 2026.
- Xu et al., *Discovering Hierarchical Software Engineering Agents via Bandit Optimization*, ICLR 2026.
- Park et al., *Capable language models can outgrow the benefits of collaboration*, Nature Machine Intelligence, 2026.