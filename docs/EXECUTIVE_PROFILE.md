# Executive profile

Agentit's `executive` profile adds a provider-neutral executive operating layer for company-level decisions without weakening the repository's cold-session JIT architecture.

It is materially informed by [Sente Labs / OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive), an Apache-2.0 project that uses a single Executive orchestrator with domain specialists, company context, retrieval/memory, parallel consultation and an evaluation layer. Agentit adopts the durable operating ideas rather than vendoring OpenExecutive's application/runtime stack.

## Architectural rule

The profile may be broad. **Runtime context must remain narrow.**

```text
executive profile installed
        │
        │ discovery availability only
        ▼
executive pack inspected
        │
        │ semantic possibilities only
        ▼
primary AI selects exact skill(s)
        │
        ├─ executive-finance
        ├─ executive-strategy
        ├─ executive-legal
        └─ ...only when justified
        ▼
optional bounded specialist workers
        │
        ▼
single parent synthesis
```

A fresh execution session still begins with exactly:

```text
using-agentit
+ task-router
+ using-agent-skills
```

No executive skill is global/core. Installing `executive` does not activate its skill bodies, references, workers or tools. Every new task must make a fresh semantic selection.

## Why this differs from simply embedding OpenExecutive

OpenExecutive is a full executive-agent application. Agentit is a provider-neutral reliability/JIT expertise layer that wraps capable agents.

Vendoring the full OpenExecutive runtime would introduce assumptions Agentit does not need, including a particular application architecture, provider/model defaults, UI/backend stack and persistence implementation. Instead Agentit extracts the reusable behavior:

- one accountable executive synthesis;
- deep domain specialist procedures;
- model-owned specialist selection;
- parallel fan-out when independent analysis earns its cost;
- company-specific context rather than generic answers;
- durable prior decisions/initiatives when available;
- explicit authority and escalation boundaries;
- source/evidence discipline;
- evaluation and failure-mode thinking.

Agentit deliberately does **not** require Anthropic/Claude, FastAPI, Next.js, ChromaDB, SQLite, Honcho or OpenExecutive itself.

## Skills

The profile exposes these JIT executive skill bodies:

| Skill | Responsibility |
|---|---|
| `executive-orchestration` | cross-functional routing, bounded fan-out, conflict resolution and single executive synthesis |
| `executive-strategy` | positioning, market choice, moat, strategic options, build/buy/partner and sequencing |
| `executive-finance` | cash, unit economics, scenarios, capital allocation, pricing economics and ROI |
| `executive-people` | role design, hiring, compensation, performance, retention and org design |
| `executive-legal` | contract/IP/employment/privacy/regulatory framing, jurisdiction and counsel escalation |
| `executive-operations` | bottlenecks, process, automation, vendor risk, capacity and operating metrics |
| `executive-marketing` | ICP, positioning, funnel/channel economics, GTM, brand/demand and retention linkage |
| `executive-product` | customer problems, PMF, prioritization, sequencing, make/buy and evidence gates |
| `executive-board` | board/investor narrative, variance, risks, governance and explicit asks |
| `executive-chief-of-staff` | triage, decision queue, ownership, follow-up and operating cadence |

The profile also exposes relevant existing Agentit capabilities such as specialist routing, source/reference intelligence, context engineering, planning, adversarial review, durable documentation, verification, interviewing and the deeper marketing operating skill. They remain JIT too.

## Company-context contract

Executive work should be anchored to reliable context that is actually relevant to the decision. Depending on the task, this can include:

- business model and customer;
- stage/scale;
- financial constraints;
- current priorities and deadlines;
- product/channel performance;
- team and decision authority;
- prior durable decisions;
- live market/regulatory evidence.

Missing context is not permission to fabricate. The agent should recover discoverable facts through approved sources/tools, state assumptions when safe, and ask only when an unresolved fact is genuinely decision-blocking.

## Specialist routing

The primary AI owns semantic routing. There is no programmatic executive keyword classifier.

For a single-domain question, the parent can load one specialist skill and answer directly.

For a genuinely cross-functional decision, `executive-orchestration` may use `specialist-agent-routing` to spawn bounded workers. Workers receive only:

```text
role / question
relevant company slice
selected executive skill body
selected evidence/references
tools / permissions
expected handoff
verification / stop condition
```

The parent remains the only integrator/final writer. It does not paste specialist outputs together or average disagreements; it resolves them against assumptions, evidence, company constraints and authority.

## Evidence model

Executive conclusions should distinguish:

1. verified internal/company facts;
2. current external facts with provenance;
3. estimates and model assumptions;
4. general benchmarks/heuristics;
5. specialist judgment.

Benchmarks in the specialist skills are explicitly heuristics. A remembered SaaS, org-design or board-practice threshold does not become a universal rule.

Current market, competitor, legal, tax, regulatory, compensation or platform claims use current authoritative/credible sources whenever they materially determine the decision.

## Memory and continuity

OpenExecutive implements persistent company and department memory. Agentit keeps the behavior provider-neutral:

- inspect available durable project/company records when relevant;
- reuse prior **decisions and facts**, not prior session skill/tool activation;
- update durable business/decision documentation for substantial ongoing work when useful and authorized;
- keep private operational continuity separate from durable project knowledge;
- never claim a memory capability the current host/project does not actually provide.

## Authority

Executive intelligence does not imply executive authorization.

The user/project policy still controls real actions. Spending, hiring/firing, legal positions, production changes, public/external communications and other consequential mutations follow Agentit's normal review, permission and rollback rules.

The specialist skills may prepare recommendations, models, drafts or decision material without claiming authority to commit the company.

## Relationship to operational skills

Executive skills decide at the business-function level. Existing Agentit skills can perform deeper execution when selected.

Examples:

```text
executive-marketing
  -> decides ICP, positioning, channel priority and economics
  -> marketing-and-growth executes deeper campaign/CRO/content work when useful

executive-product
  -> decides problem, evidence gate, priority and sequencing
  -> spec-driven-development turns a decided direction into implementation requirements

executive-operations
  -> decides process/automation/vendor intervention
  -> engineering/release skills implement and verify technical changes
```

This avoids both extremes: a shallow “CEO prompt” and a monolithic executive context dump.

## Verification

Mechanical regression tests protect these invariants:

- global core remains exactly the three navigation skills;
- `executive` exists only as installation/discovery availability;
- every executive skill is discoverable through the profile and `all`;
- executive specialist catalog entries reference real skill bodies;
- no executive skill silently enters global core;
- executive pack documentation keeps installation distinct from activation.

Agent-quality claims require stronger evidence than mechanical tests. OpenExecutive's own LLM-as-judge evals are useful design evidence but not independent proof that Agentit's adaptation improves every agent. Agentit's paired real-agent evaluation policy remains the standard for comparative performance claims.

## Provenance

See `THIRD_PARTY_NOTICES.md` for OpenExecutive attribution and license notes. Agentit does not claim drop-in compatibility with OpenExecutive.