# LLM-native decision protocol

Agentit does not use executable natural-language routing.

The architecture deliberately separates three reasoning roles:

1. the **primary model decides** from the full task context;
2. a **cheap independent model audits** the proposal for omissions and reasons to reconsider/escalate;
3. a **strong independent critic/judgment model arbitrates** high-risk or materially disputed cases before execution.

The cheap model is not the router and is never the owner of semantic classification.

## Primary decision ownership

The active primary model considers at least:

- the user's actual intent and desired outcome;
- facts already established from conversation/project/tool context;
- material unknowns and assumptions;
- domain/category and complexity;
- risk and reversibility;
- production, account, financial, data or other external effects;
- useful skills and tools;
- topology and delegation benefit;
- workers/specialists and ownership boundaries when useful;
- dependency order;
- execution plan;
- verification evidence;
- backup, dry-run, rollback and post-check needs where relevant.

It then owns the resulting `TASK_DECISION`. Do not demote this work to a cheaper worker just because the decision can be represented compactly.

The same rubric is applied consistently, but the result remains context-sensitive. A follow-up such as “fix it” is interpreted from the context that gives “it” meaning rather than from those words in isolation.

## Cheap audit

For ordinary material work, use the cheapest independent model/endpoint that is still competent to audit the bounded `TASK_DECISION`, typically semantic tier `fast`. When similarly cheap, a different model family from the primary model is preferable because diversity makes the second opinion more useful.

The auditor is read-only. Give it only the bounded context needed to judge the proposal:

- exact request and material user/project constraints;
- relevant facts already established;
- proposed `TASK_DECISION`;
- applicable Agentit rules.

It must not replace the decision. It only checks for misunderstood intent, risk possibly classified too low, missing constraints, unjustified assumptions, poor skill/tool choice, unnecessary or missing delegation, unsafe parallel ownership, dependency mistakes, weak verification, and reasons to escalate.

It returns:

```text
AUDIT: CLEAR | CHALLENGE | ESCALATE
FINDINGS:
- ...
SUGGESTED_CHECKS:
- ...
CONFIDENCE: low | medium | high
```

`CLEAR` means no material objection was found.

`CHALLENGE` means the primary model must reconsider the finding. The primary may revise its decision or retain it with explicit evidence-based reasoning.

`ESCALATE` means a stronger independent model should review before execution. If a material challenge remains unresolved after primary reconsideration, escalate rather than letting the cheap model arbitrate.

Ordinary audit/reconsideration is bounded to two cycles.

## Strong arbitration

Use an independent `critic` or `judgment` tier model when:

- `RISK_3` or `RISK_4`;
- the cheap auditor returns `ESCALATE`;
- material disagreement survives primary reconsideration;
- destructive or difficult-to-reverse operations are involved;
- authentication/authorization/session boundaries are involved;
- payments/billing/financial effects are involved;
- secrets or credentials are involved;
- PII or sensitive data is involved;
- production infrastructure/deployments are involved;
- significant data/schema migrations are involved;
- a large structural architecture/product plan is about to be committed to.

The strong critic reviews the primary `TASK_DECISION` and relevant audit findings. It does not become the implementation owner, but for these cases it is the independent judgment gate: material execution waits until critical objections are resolved, the decision is revised, or required user input is obtained.

For destructive data work, require a verified backup, rollback plan and post-check. For `RISK_4`, use a preview/dry-run whenever technically meaningful.

## Software boundary

Programs may still perform mechanical work after the AI has made and reviewed the decision: copy files, manage manifests, persist runtime state, invoke explicitly selected tools, run tests and checks, or enforce mechanical ownership/dependency constraints.

Programs may **not** parse the user's natural language to choose semantic intent, category, risk, topology, skill relevance or delegation.

The boundary is:

> **Primary AI decides; cheap AI audits; strong AI arbitrates when needed; software performs mechanical operations afterward.**

## Canonical files

- `skills/task-router/SKILL.md` — mandatory primary-model decision rubric.
- `skills/task-router/references/economy-reviewer.md` — cheap independent audit contract.
- `skills/using-agentit/SKILL.md` — end-to-end operating protocol.
- `docs/NO_PROGRAMMATIC_ROUTER.md` — architecture boundary.

There is intentionally no `route.py`, semantic `decision_contract.py`, prompt-regex router, or executable language-classification eval suite.
