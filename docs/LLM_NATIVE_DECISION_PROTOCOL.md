# LLM-native decision protocol

Agentit does not use executable natural-language routing.

The primary AI interprets the task from the full context available to it and creates a `TASK_DECISION`. Before material execution, a second AI reviews that proposal. This review is part of the operating protocol, not an optional quality pass.

## Primary decision

The primary model considers at least:

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

The same rubric is applied consistently, but the result remains context-sensitive. A follow-up such as “fix it” is interpreted from the context that gives “it” meaning rather than from those words in isolation.

## Economy review

For ordinary material work, use the cheapest capable independent model/endpoint available to review the proposed `TASK_DECISION`. Prefer a semantic `fast` tier. When similarly cheap, a different model family from the primary model is preferable because diversity makes the second opinion more useful.

The reviewer is read-only. Give it only the bounded context needed to judge the proposal:

- exact request and material user/project constraints;
- relevant facts already established;
- proposed `TASK_DECISION`;
- applicable Agentit rules.

It returns `APPROVE`, `REVISE` or `BLOCK` and actively checks for misunderstood intent, risk classified too low, missing constraints, unjustified assumptions, poor skill/tool choice, unnecessary or missing delegation, unsafe parallel ownership, dependency mistakes and weak verification.

Ordinary review is bounded to two revision cycles. After that, choose a conservative route or surface the unresolved uncertainty rather than looping indefinitely.

## Strong review

The economy reviewer is the default preflight check, but high-consequence work also requires a stronger independent `critic` or `judgment` tier review.

Examples:

- `RISK_3` or `RISK_4`;
- destructive or difficult-to-reverse operations;
- authentication/authorization/session boundaries;
- payments/billing/financial effects;
- secrets or credentials;
- PII or sensitive data;
- production infrastructure/deployments;
- significant data/schema migrations;
- large structural architecture/product plans.

For destructive data work, require a verified backup, rollback plan and post-check. For `RISK_4`, use a preview/dry-run whenever technically meaningful.

## Software boundary

Programs may still perform mechanical work after the AI has made and reviewed the decision: copy files, manage manifests, persist runtime state, invoke explicitly selected tools, run tests and checks, or enforce mechanical ownership/dependency constraints.

Programs may **not** parse the user's natural language to choose semantic intent, category, risk, topology, skill relevance or delegation.

The boundary is:

> **AI decides; another AI reviews; software performs mechanical operations after the decision.**

## Canonical files

- `skills/task-router/SKILL.md` — mandatory primary-model decision rubric.
- `skills/task-router/references/economy-reviewer.md` — cheap independent reviewer contract.
- `skills/using-agentit/SKILL.md` — end-to-end operating protocol.
- `docs/NO_PROGRAMMATIC_ROUTER.md` — architecture boundary.

There is intentionally no `route.py`, semantic `decision_contract.py`, prompt-regex router, or executable language-classification eval suite.
