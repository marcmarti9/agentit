# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/version-v0.3.2--stable-green.svg)](https://github.com/marcmarti9/agentit/releases)

**Agentit is a provider-neutral operating protocol for capable AI coding agents.** It lets the primary model understand a task from real project context, independently review the decision before material execution, load only the knowledge and tools that matter, delegate when useful, execute through verifiable runtime contracts, document durable system knowledge, and ship repository changes through pull requests by default.

Agentit is designed to remain portable across OpenAI, Anthropic, Google, xAI and compatible future agent environments. Provider-specific workers are execution primitives; the shared protocol is the product.

## Activation

There is one activation concept: tell the agent to use Agentit naturally in your language.

```text
usa agentit
use agentit
utilise agentit
```

There are no additional powerwords and no keyword/regex classifier in front of the model. The active primary AI owns semantic understanding from the full conversation, repository, files, tools, constraints and prior state.

## End-to-end lifecycle

For substantial work, Agentit follows this lifecycle:

```text
inspect facts and existing project state
        ↓
primary AI creates TASK_DECISION
        ↓
cheap independent decision audit
        ↓
CLEAR / CHALLENGE / ESCALATE
        ↓
strong independent review when consequences are high
        ↓
interview unresolved product decisions when needed
        ↓
load the smallest useful skills and tools
        ↓
persist continuity state
        ↓
execute directly or delegate through Loop / Graph contracts
        ↓
document architecture, components, contracts, decisions and failures
        ↓
verify with fresh evidence + runtime receipts + documentation-drift check
        ↓
branch → commits → pull request → user/reviewer merge decision
```

Small mechanical tasks stay small. Agentit does not create multi-agent theatre or process for its own sake.

## 1. Primary AI owns the decision

Agentit deliberately has **no programmatic natural-language router**. A script does not know the conversation history, what “fix it” refers to, the current repository state or which constraints were already agreed.

The primary model therefore owns `TASK_DECISION`, including:

- intended outcome and known facts;
- material unknowns;
- domain/category and complexity;
- `RISK_0..RISK_4` with rationale;
- reversibility and external effects;
- required skills and tools;
- execution topology;
- specialist ownership boundaries;
- implementation/investigation plan;
- verification strategy;
- backup, dry-run, rollback and post-check requirements when relevant.

Canonical policy: [`skills/task-router/SKILL.md`](skills/task-router/SKILL.md) and [`docs/NO_PROGRAMMATIC_ROUTER.md`](docs/NO_PROGRAMMATIC_ROUTER.md).

## 2. Independent decision review

Before material execution, Agentit asks a second AI to challenge the proposed task decision.

Ordinary work uses the cheapest capable independent model or endpoint, preferably a semantic `fast` tier. It returns:

```text
AUDIT: CLEAR | CHALLENGE | ESCALATE
FINDINGS:
- ...
SUGGESTED_CHECKS:
- ...
CONFIDENCE: low | medium | high
```

The reviewer is not the router and does not take ownership from the primary model. `CHALLENGE` forces reconsideration; unresolved disagreement or `ESCALATE` moves to a stronger independent critic.

Strong review is mandatory for high-risk work such as destructive operations, production changes, auth, payments, secrets, PII, significant migrations, difficult rollback and large structural architecture decisions.

See [`skills/task-router/references/economy-reviewer.md`](skills/task-router/references/economy-reviewer.md) and [`docs/LLM_NATIVE_DECISION_PROTOCOL.md`](docs/LLM_NATIVE_DECISION_PROTOCOL.md).

## 3. Interview only when product decisions are actually missing

For product-affecting work, Agentit inspects discoverable facts first. If material choices still cannot be inferred safely, it asks them in one consolidated batch and recommends sensible defaults.

The purpose is to avoid both silent invention and twenty-message interrogations.

Design work can use **Standard / Polished / Studio** craft depth. Those levels apply to visual/design ambition, not to every engineering task.

See [`skills/interview-me/SKILL.md`](skills/interview-me/SKILL.md) and [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md).

## 4. Skills, tools and delegation are selected just in time

Agentit loads the smallest useful knowledge set instead of dumping a full skill catalog into context. A skill counts as used only when its body is actually loaded or injected into the executing model.

Delegation is equally adaptive. Use another worker when independence, parallel investigation, specialist expertise, context isolation, critique or bounded cheap execution creates real value. Stay single-agent when it does not.

`agents/catalog.yaml` defines reusable specialist roles. `profiles.yaml` groups capabilities into profiles such as `core`, `frontend`, `design`, `backend`, `supabase`, `product`, `writing`, `release` and `research`.

Capability resolution is explicit and least-privilege: specialists declare stable capability IDs and the host maps them to actually available MCPs, apps, CLIs or local tools. Missing capabilities are not silently assumed.

See [`docs/CAPABILITIES.md`](docs/CAPABILITIES.md), [`agents/catalog.yaml`](agents/catalog.yaml) and [`profiles.yaml`](profiles.yaml).

## 5. Runtime acceptance: Loop and Graph

Agentit's runtime is mechanical enforcement after the AI has made and reviewed the semantic decision.

### Loop Contract

Every executable unit with a verifiable outcome defines:

- observable goal;
- verifier;
- stop condition;
- bounded attempt budget;
- escalation boundary.

A direct executable task is accepted only after fresh verifier evidence and a passed **Loop Receipt**.

### Graph Contract

Genuinely multi-node work materializes a DAG before spawning. Dependencies, write ownership, handoff artifacts and node Loop Contracts are explicit. Final acceptance requires a passed **Graph Receipt** backed by current node receipts.

The runtime tracks execution state; it never interprets natural-language intent.

See [`docs/RUNTIME_ENGINEERING.md`](docs/RUNTIME_ENGINEERING.md).

## 6. Continuity: sessions are disposable

Chats, providers and machines can disappear. Substantial work therefore keeps a compact canonical state file at:

```text
docs/agentit/STATE.md
```

or an existing project-equivalent source of truth.

It records the current objective, constraints, status, durable decisions, branch/PR, important artifacts, latest verification, blockers and next executable actions. It does **not** store secrets, transcripts or private chain-of-thought.

A fresh agent should be able to resume without making the user reconstruct the previous session.

See [`docs/PROJECT_CONTINUITY.md`](docs/PROJECT_CONTINUITY.md).

## 7. Durable documentation is part of the implementation

`STATE.md` explains **where the work is now**. It does not replace permanent documentation explaining **how the system works and why**.

For substantial repository work, Agentit must keep the relevant Markdown documentation aligned with the implementation:

- overall architecture, layers, boundaries and end-to-end flows;
- responsibilities and behavior of non-trivial components;
- APIs, schemas, events, files, invariants and compatibility contracts;
- durable non-obvious decisions and their consequences;
- operational lifecycle, jobs, persistence, retries, fallbacks and observability;
- troubleshooting paths from symptom → likely cause → evidence → corrective action → verification;
- commands and tests that reproduce the relevant verification.

When a project lacks a documentation structure, the recommended shape is:

```text
docs/
  ARCHITECTURE.md
  components/
  decisions/
  OPERATIONS.md
  TROUBLESHOOTING.md
  agentit/
    STATE.md
```

Existing canonical docs should be reused rather than duplicated. Important decisions can use ADR-style records. Private chain-of-thought is never persisted; only concise rationale, evidence, alternatives and consequences needed by future maintainers.

Substantial work is not complete until Agentit checks for **documentation drift**. If the code and docs disagree, the task is still unfinished.

See [`docs/DOCUMENTATION_CONTRACT.md`](docs/DOCUMENTATION_CONTRACT.md).

## 8. Verification before claims

Agentit separates confidence from evidence. No `done`, `fixed`, `passing`, `premium` or equivalent claim is accepted without fresh evidence appropriate to the claim and the applicable runtime receipt.

Examples:

- code change → relevant tests/runtime checks + Loop Receipt;
- bug fix → reproduction before and verification after;
- visual change → rendered/browser evidence at relevant viewport sizes;
- migration → pre/post evidence + rollback readiness;
- high-risk change → strong independent review + operational checks;
- multi-node work → Graph Receipt backed by node Loop Receipts;
- substantial repository work → documentation-drift check.

```bash
agentit verify "task summary" --project .
agentit verify "task summary" --project . --apply
```

## 9. Git ownership

Repository changes default to:

```text
work branch → commits → verification → pull request → review/user merge decision
```

Agentit does not write directly to `main`/`master` or auto-merge unless explicitly authorized for the current task.

## Design intelligence

The `design` profile combines structured UI/UX intelligence, live inspiration research, art direction, implementation guidance, motion/spatial skills and independent critique without loading all of them by default.

Notable skills include:

- `ui-ux-pro-max-intelligence` — JIT structured UI/UX intelligence;
- `design-inspiration-research` and `design-trend-researcher` — live evidence;
- `design-taste-frontend` and `impeccable-design` — direction and critique;
- `emil-design-eng` — interaction/motion quality;
- GSAP and Three.js specialists for scroll and spatial experiences;
- Figma workflow support when the official integration is available.

The upstream UI/UX dataset is treated as an intelligence source, not as an automatic creative director. Attribution lives in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Install

```bash
git clone https://github.com/marcmarti9/agentit.git ~/code/agentit
cd ~/code/agentit
bash install.sh --provider all --with-guides --apply
ln -sf ~/code/agentit/agentit ~/.local/bin/agentit
```

Enable project profiles only when needed:

```bash
agentit enable design --project . --apply
agentit status --project .
agentit disable design --project . --apply
```

MCP runtime helpers:

```bash
agentit mcp status
agentit mcp enable context7 --apply
agentit mcp enable-stack developer_core --apply
```

## Testing

```bash
python3 -m unittest discover -s router -p "test_*.py"
python3 -m unittest discover -s tests
```

The suite covers mechanical runtime, profiles, capabilities, MCP behavior, continuity, verification, registry/inventory safety and worker-context behavior. It intentionally does not pretend that deterministic prompt classification can benchmark the semantic judgment of the active AI.

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | Global portable Agentit rules |
| `skills/using-agentit/` | End-to-end activation playbook |
| `skills/task-router/` | AI-native task decision and reviewer contracts |
| `skills/` | JIT knowledge modules |
| `agents/` | Portable specialist catalog |
| `router/` | Mechanical Loop/Graph/runtime tooling |
| `profiles.yaml` | Profile composition |
| `effort/` | Design craft-depth configuration |
| `docs/` | Architecture, policy, continuity and runtime documentation |
| `.codex/agents/` | Bounded Codex worker profiles |

## Documentation map

| Document | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | global agent playbook |
| [`docs/NO_PROGRAMMATIC_ROUTER.md`](docs/NO_PROGRAMMATIC_ROUTER.md) | boundary between AI judgment and mechanical software |
| [`docs/LLM_NATIVE_DECISION_PROTOCOL.md`](docs/LLM_NATIVE_DECISION_PROTOCOL.md) | primary decision + second-model review |
| [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md) | interview and provider semantics |
| [`docs/PROJECT_CONTINUITY.md`](docs/PROJECT_CONTINUITY.md) | resumable project-state contract |
| [`docs/DOCUMENTATION_CONTRACT.md`](docs/DOCUMENTATION_CONTRACT.md) | mandatory durable system documentation contract |
| [`docs/RUNTIME_ENGINEERING.md`](docs/RUNTIME_ENGINEERING.md) | Loop/Graph execution contracts |
| [`docs/CAPABILITIES.md`](docs/CAPABILITIES.md) | capability resolution and least privilege |
| [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md) | MCP catalog/runtime |
| [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md) | orchestration topologies and specialist contracts |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | upstream attribution |

## License

Licensed under the [Apache License, Version 2.0](LICENSE). Third-party integrations retain their applicable notices in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
