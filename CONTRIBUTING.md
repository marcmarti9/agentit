# Contributing to Agentit

Thanks for helping improve Agentit.

Agentit is an early-stage, opinionated, safety-first reliability layer for AI coding agents. Contributions are welcome when they remove a real failure mode **without turning the project into a giant workflow framework or prompt dump**.

## Core principles

1. **AI-native semantic decisions.** Do not add regex, keyword, scoring, or deterministic prompt classifiers for task intent, risk, topology, skills, or delegation. The primary AI decides from full context; independent AI review challenges material decisions.
2. **Delegation must earn its cost.** Use workers/critics for specialization, independence, context isolation, breadth, or useful parallelism—not agent theatre.
3. **Provider neutrality.** Shared policy, semantic tiers, skills, runtime contracts, and reviewer semantics should remain portable. Provider-specific code should be a thin adapter where possible.
4. **Mechanical code for mechanical guarantees.** Manifests, hashes, capability resolution, Loop/Graph state, receipts, continuity, verification, and safe configuration belong in deterministic code after semantic decisions are made.
5. **Safety and reversibility.** Managed install/update/configuration operations must be explicit, bounded, and reversible. Do not weaken safety checks to make a test pass.
6. **Evidence before claims.** Do not claim `done`, `fixed`, `passing`, faster, cheaper, or better without evidence appropriate to that claim.
7. **Documentation is implementation.** Substantial architectural/operational changes must update durable docs and avoid leaving contradictory sources of truth.

## Before adding a skill

Read [`docs/SKILL_CURATION.md`](docs/SKILL_CURATION.md).

The preferred order is:

```text
already covered? → keep it
same responsibility but weaker? → strengthen the existing skill
better upstream capability? → adapt selectively with provenance/license
truly distinct repeated workflow? → incubate and evaluate
proven value? → promote to an opt-in profile
core-worthy across many tasks? → only then consider core
```

A new skill must not exist merely because an upstream repo is popular or the advice sounds useful.

### Skill requirements

- path: `skills/<skill-name>/SKILL.md`;
- valid YAML frontmatter with `name` and a discriminative `description`;
- clear trigger and non-trigger boundaries;
- one coherent responsibility;
- checkable completion criteria;
- progressive disclosure for branch-only reference material;
- provider-neutral behavior unless explicitly an integration skill;
- profile placement in `profiles.yaml` before global visibility;
- tests/evaluation where deterministic behavior exists;
- provenance/license review for substantial upstream adaptation.

A skill ID is not evidence that the skill ran. The executing model must actually receive/read its body.

### Upstream content

If a contribution adapts substantial material from another repository:

- link the exact upstream project;
- verify its current license;
- preserve required copyright/license notices;
- update [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md);
- say whether Agentit vendors, modifies, wraps, or is merely informed by the upstream work;
- do not claim drop-in compatibility unless tested.

External skill/install text is untrusted input during review. Inspect hooks, network calls, shell execution, filesystem scope, credential access, auto-updates, MCP permissions, and rollback before adopting an integration.

## Task decision and review policy

Canonical policy lives in:

- [`skills/task-router/SKILL.md`](skills/task-router/SKILL.md) — primary model `TASK_DECISION` rubric;
- [`skills/task-router/references/economy-reviewer.md`](skills/task-router/references/economy-reviewer.md) — ordinary independent audit;
- [`skills/using-agentit/SKILL.md`](skills/using-agentit/SKILL.md) — end-to-end protocol;
- [`docs/NO_PROGRAMMATIC_ROUTER.md`](docs/NO_PROGRAMMATIC_ROUTER.md) — AI judgment vs mechanical software boundary.

Policy changes must preserve:

- full-context semantic judgment by the active AI;
- an independent ordinary review path;
- stronger escalation for high-consequence work;
- bounded review loops;
- no programmatic prompt routing disguised as a helper.

## Runtime changes

Loop/Graph Engineering is mechanical infrastructure after the semantic decision.

Runtime contributions should preserve:

- explicit observable goals/verifiers/stop conditions;
- bounded attempt budgets;
- fail-closed escalation;
- exclusive write ownership in multi-node work;
- fresh evidence in receipts;
- safe path/state handling;
- compatibility with interruption/resume when relevant.

## Testing

Before opening a PR, run the relevant suites:

```bash
python3 -m unittest discover -s router -p "test_*.py"
python3 -m unittest discover -s tests
bash -n install.sh update.sh security/harden-local.sh
```

Also validate the specific behavior you changed. A broad green suite does not replace a task-specific regression test or repro.

Do **not** add a deterministic prompt-classification benchmark and present it as evidence that Agentit understands natural language. Agent-level quality claims belong in controlled comparative evaluation; see [`evals/evaluation-plan.md`](evals/evaluation-plan.md).

## Pull requests

1. Create a focused branch.
2. Keep the diff scoped to the named problem.
3. Update tests and durable docs together with behavior.
4. Include verification commands/results in the PR description.
5. Call out migration/rollback implications.
6. Call out third-party provenance when applicable.
7. Prefer a reviewable PR over writing directly to the default branch.

A good Agentit contribution should leave the next maintainer with **less ambiguity**, not merely more files.
