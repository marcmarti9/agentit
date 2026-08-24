# Evaluation plan

## Purpose

Evaluate Agentit without confusing **mechanical contract correctness** with **agent quality**.

Agentit intentionally has no deterministic natural-language router. Therefore a prompt-classification benchmark is not a valid proxy for whether the active AI understood a task. The evaluation surface is split into two layers:

1. **Mechanical/runtime evaluation** — deterministic code can and should be tested automatically.
2. **Agent-level comparative evaluation** — claims that Agentit improves real coding outcomes require controlled runs against a baseline agent.

## A. Mechanical/runtime contract

CI and local tests should cover at least:

- profile resolution and project-local activation;
- invalid YAML/catalogs and unknown skill IDs fail closed;
- path traversal and symlink rejection;
- manifests, hashes, managed/unmanaged-file behavior and reversible state changes;
- capability and MCP resolution without free-text semantic routing;
- worker-context projection and bounded capability assignment;
- continuity state/checkpoint behavior;
- Loop/Graph state machines, attempt budgets and receipt acceptance;
- verification probe planning/execution and receipt persistence;
- semantic verification probes activate only from **explicit AI-selected signals**, never because Python parses the task summary;
- architecture-policy tests reject reintroduction of programmatic prompt routing;
- shell syntax, YAML/JSON validity and catalog integrity;
- installation/update scripts remain plan-first and fail closed on unsafe filesystem state.

### Platform matrix

The current shell installer/update implementation is **GNU/Linux + Bash 4+ only**. CI must not imply macOS support until those scripts are made portable and actually exercised on a macOS runner.

Python runtime components should remain portable unless a component explicitly documents otherwise.

## B. Public CLI contract

Every command shown in `README.md` must have at least one automated smoke/regression check at the parser/runtime boundary.

Particular launch-critical checks:

- `agentit verify ... --signal auth` selects `auth-boundary`;
- putting words such as `auth`, `login`, or `jwt` only in task text does **not** select semantic probes;
- repeated explicit signals are normalized and preserved in the receipt;
- plan mode does not execute project commands or mutate managed state;
- `--apply` is required for mutating profile/MCP operations.

## C. Skill quality

Skills are evaluated as behavioral documents, not by line count.

For core or newly promoted skills, review:

- trigger description is discriminative and names real branches;
- overlap with existing skills is low enough to justify a separate skill;
- steps have clear completion criteria;
- branch-only reference material is progressively disclosed when useful;
- instructions point to project facts instead of duplicating easy-to-discover state;
- safety/verification requirements are testable rather than aspirational;
- substantial third-party adaptations have provenance and license notices.

Candidate skills should enter through `incubator/` and be promoted only when they solve a repeated failure mode better than strengthening an existing skill.

## D. Agent-level comparative evaluation

This is the layer required before publishing claims such as “Agentit produces better code” or “Agentit saves tokens.”

Use paired tasks against the **same model/provider/version**:

- baseline: provider defaults + repository instructions;
- treatment: the same environment with Agentit active.

Representative task families:

1. small mechanical edit;
2. ambiguous feature with product decisions;
3. hard reproducible bug;
4. auth/security-sensitive change;
5. medium refactor across modules;
6. multi-session task requiring continuity;
7. documentation-affecting architecture change.

Record:

- task success against blind acceptance criteria;
- regressions introduced;
- independent-review catches that changed the final implementation;
- retries / failed tool calls;
- elapsed time;
- input/output tokens when the provider exposes them;
- number of model calls / delegated workers;
- user interventions;
- verifier evidence quality;
- documentation drift after completion.

Do not aggregate unlike providers/models into one “Agentit score.”

## Promotion criteria

A new runtime mechanism or skill is ready for the default path only when:

1. it addresses a named recurring failure mode;
2. its mechanical behavior is covered where deterministic testing is possible;
3. it does not violate provider neutrality or the no-programmatic-semantic-router boundary;
4. it has an explicit rollback/removal path when it mutates state;
5. it does not duplicate an existing core capability without a measurable reason;
6. provenance is documented for substantial upstream adaptations;
7. public claims do not exceed observed evidence.

## Claims policy

Until comparative agent-level runs exist, Agentit may truthfully claim that it **implements and tests** its mechanical contracts. It must not claim universal improvements in coding quality, tokens, cost, latency, or reliability over a raw frontier agent.
