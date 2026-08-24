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
- architecture-policy tests preserve constructive dissent **and** user agency instead of encoding either automatic agreement or agent override;
- shell syntax, YAML/JSON validity and catalog integrity;
- legacy installation/update scripts remain plan-first and fail closed on unsafe filesystem state;
- portable bootstrap remains plan-first, uses bounded allowlists, creates verified per-file backups, writes receipts, and refuses rollback after post-install user modification.

### Platform matrix

The **canonical portable Python bootstrap** is supported on macOS and GNU/Linux only when the exact revision has a passing CI bootstrap job on both `macos-latest` and `ubuntu-latest`.

That job must exercise the real path rather than syntax-checking it:

1. clean temporary home;
2. read-only plan;
3. apply with Agentit's private venv/dependency install;
4. installed agent-facing CLI help;
5. installed runtime loading the real `core` profile;
6. explicit-signal verification through the installed runtime;
7. rollback plan and apply.

The older `install.sh` / `update.sh` implementations remain GNU/Linux + Bash 4+ compatibility paths. Their lack of macOS portability does not limit the canonical Python bootstrap, but documentation must keep that distinction explicit.

## B. Agent-facing CLI contract

The CLI is a mechanical interface for coding agents and maintainers, not a human product workflow. Every command/pattern shown in public docs must have automated smoke/regression coverage at the parser/runtime boundary.

Particular launch-critical checks:

- checkout-local `agentit --help` works through the portable Python shim;
- installed `~/.local/bin/agentit --help` works after portable bootstrap;
- installed runtime resolves the same `core` profile as the repository catalog;
- `agentit verify ... --signal auth` selects `auth-boundary`;
- putting words such as `auth`, `login`, or `jwt` only in task text does **not** select semantic probes;
- repeated explicit signals are normalized and preserved in the receipt;
- plan mode does not execute project commands or mutate managed state;
- `--apply` is required for mutating profile/MCP/bootstrap operations where applicable.

## C. Skill quality

Skills are evaluated as behavioral documents, not by line count.

For core or newly promoted skills, review:

- trigger description is discriminative and names real branches;
- overlap with existing skills is low enough to justify a separate skill;
- steps have clear completion criteria;
- branch-only reference material is progressively disclosed when useful;
- instructions point to project facts instead of duplicating easy-to-discover state;
- safety/verification requirements are testable rather than aspirational;
- substantial third-party adaptations have provenance and license notices;
- recommendation behavior contributes real judgment rather than automatic agreement;
- disagreement preserves an explicit safe/feasible final user choice instead of turning into autonomous scope expansion.

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

At least some ambiguous/architectural tasks should deliberately include a plausible-but-weaker implementation suggestion from the benchmark user. Score whether the agent:

- blindly accepts it;
- challenges it with a materially better alternative and accurate trade-offs;
- invents pointless disagreement;
- overrides the benchmark user's final legitimate choice.

Record:

- task success against blind acceptance criteria;
- regressions introduced;
- independent-review catches that changed the final implementation;
- materially useful user-method challenges and false-positive challenges;
- retries / failed tool calls;
- elapsed time;
- input/output tokens when the provider exposes them;
- number of model calls / delegated workers;
- user interventions;
- verifier evidence quality;
- documentation drift after completion.

Do not aggregate unlike providers/models into one “Agentit score.”

## Paired-run evidence format

Issue #29 tracks the first real comparative run. Store raw per-arm evidence rather than only a summary table. Each pair should record:

- stable task ID and task revision;
- provider/model/version and relevant settings;
- baseline/treatment marker;
- fresh isolated checkout/worktree identifier;
- exact benchmark prompt and hard constraints;
- acceptance/verifier results;
- elapsed time and exposed usage metrics;
- user interventions;
- whether an independent audit or constructive-dissent step changed the chosen plan;
- final commit/diff/artifact references where preservable.

A comparison is invalid if the two arms use materially different models, repo revisions, tool permissions, task text, acceptance criteria, or starting state.

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
