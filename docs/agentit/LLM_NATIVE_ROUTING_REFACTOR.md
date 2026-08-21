# Agentit task-decision refactor: AI decides, AI reviews

## Goal

Remove programmatic natural-language routing from Agentit.

A capable language model should not be placed behind a hand-maintained keyword/regex classifier that sees less context than the model itself. The primary AI now owns task interpretation and planning, and another AI provides the pre-execution check.

## Architecture

```text
user request + full conversation/project/tool context
        ↓
primary AI creates TASK_DECISION
        ↓
cheap independent AI reviewer
        ↓
CLEAR / CHALLENGE / ESCALATE
        ↓
strong critic too when consequences are high
        ↓
execute reviewed plan
        ↓
fresh verification
```

## Removed responsibilities from code

Executable code does not infer from natural language:

- intent;
- semantic category/domain;
- task risk;
- topology;
- skill relevance;
- whether delegation is useful;
- which specialist should handle the problem.

Those judgments belong to the AI that can see the actual context.

The refactor removes the semantic `route.py`, semantic decision validator, route traces, router-specific tests and executable prompt-classification evals.

## Mandatory economy review

Before material execution, the primary AI sends its proposed `TASK_DECISION` to the cheapest capable independent reviewer available. The normal target is a semantic `fast` tier model/endpoint; when similarly cheap, model-family diversity is preferred.

The reviewer is deliberately read-only and adversarial. It checks whether the primary model misunderstood the task, underestimated risk, forgot constraints, selected the wrong tools/skills, delegated badly, created unsafe parallel ownership/dependencies, or proposed inadequate verification.

It returns `CLEAR`, `CHALLENGE` or `ESCALATE`. `CLEAR` is not approval authority; it only means no material objection was found. `CHALLENGE` requires primary reconsideration, and `ESCALATE` sends the decision to a stronger independent reviewer.

## Strong-review escalation

A cheap second opinion is useful even for routine work, but it is not sufficient for high-consequence decisions. `RISK_3/RISK_4`, destructive or irreversible work, auth/payments/secrets/PII/production, significant migrations and large structural plans additionally require a stronger independent `critic`/`judgment` tier review.

## What code may still do

Mechanical code is still useful for mechanical jobs after the AI has decided what to do:

- copy/install skill files;
- manage manifests and configuration;
- persist continuity/runtime state;
- execute explicitly selected tools;
- run tests/checks;
- track attempt budgets, dependencies and write ownership;
- produce verification receipts.

That code is execution infrastructure, not a language-understanding router.

## Canonical policy

- `skills/task-router/SKILL.md`
- `skills/task-router/references/economy-reviewer.md`
- `skills/using-agentit/SKILL.md`
- `docs/NO_PROGRAMMATIC_ROUTER.md`
