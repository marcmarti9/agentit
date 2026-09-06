# Agentit global agent instructions

These instructions are intentionally small. Project-local instructions take precedence when more specific; safety and explicit user constraints still govern execution.

## First-prompt dispatch

On the first meaningful task, make a semantic choice:

```text
DISPATCH_DECISION: bare | agentit
```

### Prefer `agentit` for material work

Use Agentit when JIT expertise, planning, references, tools, independent review, delegation, continuity or stronger verification could materially improve the result.

This normally includes non-trivial implementation/debugging, design, research, source-sensitive/current domains, multi-step work, ambiguous product decisions, external tools/MCPs, long-running work and higher-risk changes.

### `bare` is the exception

Use bare execution only for trivial/conversational work or a tiny obvious mechanical action where Agentit would add no material value: negligible risk, no useful domain/reference/tool decision, no meaningful orchestration/continuity need and an obvious local verifier.

**If genuinely uncertain, choose Agentit.**

An explicit natural-language request to use Agentit always selects `agentit` unless impossible or overridden by a higher-priority rule.

## Execution modes: FAST | NORMAL | DEEP

To prevent overengineering and keep iterative work responsive, calibrate execution depth to the task:

```text
EXECUTION_MODE: FAST | NORMAL | DEEP
```

- **FAST** (Default for iterative development: localized UI, styling, layout, copy, component, or behavior changes)
- **NORMAL** (Medium functional changes, multi-component features, relevant targeted tests)
- **DEEP** (Audits, migrations, production releases, security, auth, payments, high-risk systems)

### FAST MODE — Default for iterative development

When the user requests a localized UI, styling, layout, copy, component, or behavior change, optimize for iteration speed.

#### Default behavior

* Make the smallest change that correctly satisfies the request.
* Modify only files directly necessary for the requested change.
* Do NOT refactor unrelated code.
* Do NOT redesign surrounding systems.
* Do NOT perform architecture reviews unless required.
* Do NOT update documentation unless the change makes existing documentation incorrect.
* Do NOT create additional abstractions unless necessary.
* Do NOT launch subagents for normal implementation tasks.
* Do NOT perform broad repository audits.
* Do NOT search the entire repository when the relevant implementation is already known.
* Do NOT run the complete test suite for a localized change.
* Run only the minimum targeted checks necessary to detect obvious regressions.
* For visual changes, perform one desktop verification and one mobile verification unless something is visibly broken.
* Do NOT repeatedly inspect the same result after it is already correct.
* Do NOT spend time polishing things the user did not request.
* Preserve existing functionality instead of revalidating every existing feature.
* Do NOT create GitHub checkpoints/commits unless requested or unless this project explicitly requires one.

#### Scope rule

Treat the user's request literally.

If the user asks to:

* change a layout → change the layout;
* move an element → move the element;
* change spacing → change spacing;
* alter a product grid → alter the product grid.

Do not turn a localized request into a general quality, architecture, accessibility, performance, documentation, or regression-testing project.

#### Verification budget

For normal iterative changes:

1. Implement.
2. Check the affected page.
3. Fix obvious issues.
4. Stop.

Do not continue improving after the requested result has been achieved.

#### Escalation

Only switch to DEEP MODE when:

* the user explicitly asks for a deep review/audit/refactor;
* the change affects infrastructure, security, payments, authentication, production data, migrations, or other high-risk systems;
* the implementation cannot safely be localized;
* targeted validation reveals a wider regression.

Otherwise FAST MODE is mandatory.

#### Priority

During interactive design/development sessions:

**iteration speed > exhaustive validation > documentation.**

The user prefers five quick iterations over one supposedly perfect iteration that takes excessively long.

### NORMAL MODE — Medium functional changes

Use for standard feature work, multi-component fixes, and bounded non-critical tasks:

* Direct implementation with targeted test coverage.
* Run relevant test suites for affected modules, not the entire repository.
* Update durable documentation only for materially changed contracts or responsibilities.
* Subagents used only if genuine isolation/specialization provides clear value.

### DEEP MODE — High-risk, architectural, and production releases

Reserved for high-consequence work:

* Explicit deep audit/review/refactor requests from the user.
* Infrastructure, security, authentication, payments, production data, migrations, or high-blast-radius changes (`RISK_3`/`RISK_4`).
* Architecture reviews, independent critic/auditor review, comprehensive testing, durable documentation contract, and formal verification gates.

Unless DEEP MODE criteria are met, **FAST MODE is mandatory for iterative development.**

## Cold start

Every new execution session is **semantically clean**.

Assume only these three global core skill bodies are active:

```text
using-agentit
+ task-router
+ using-agent-skills
```

Installed profiles/skill files are discovery availability, not active context. Previously selected task skills, references, workers and MCPs do not carry forward as current-task decisions.

Provider MCP configuration may physically persist. A visible/configured MCP is still inactive for Agentit purposes until the new task explicitly selects it. Track MCPs enabled by the current task and clean up those task-owned additions when safe; never blanket-disable unrelated user/concurrent tooling merely to manufacture a clean status.

## When Agentit is selected

1. Load/follow `using-agentit` and the three-skill core.
2. Select `EXECUTION_MODE` (FAST by default for iterative/localized work; NORMAL for medium functional work; DEEP for high-risk/architectural tasks).
3. Inspect the relevant domain **pack(s)** as discovery maps.
4. Let the primary AI choose whatever concrete skill bodies the current stage/worker actually needs (in FAST mode, keep context tiny and avoid subagents).
5. Execute with the required verification/runtime contract (in FAST mode, follow the verification budget: implement -> check affected page -> fix obvious -> stop).
6. For substantial repository work (NORMAL/DEEP), update durable architecture/component documentation and run a documentation-drift check before completion. In FAST mode, do NOT touch documentation unless existing docs become incorrect.
7. Clean up task-added JIT tooling where safe.

## Semantic decisions belong to the AI

Do not use Python, regexes, keyword tables, fixed tiers, quotas or deterministic classifiers to infer user intent, relevant packs, skill count, selected skills, references, tools or worker topology from task text.

The primary AI owns semantic interpretation using the current conversation, repository/project state, files, instructions, tools and constraints. Cheap/strong reviewers may audit that decision; they do not replace it.

Mechanical code may resolve explicit IDs, copy files, manage manifests/state, run commands/tests and enforce reviewed Loop/Graph contracts.

## Provider/model neutrality

General Agentit contracts, packs, skills, references, Loop/Graph execution and verification are **provider/model-neutral**.

A compatible model may execute a general Agentit skill when it can receive/read the required instructions and context and satisfy the task's real tool, modality, permission and verification requirements.

Provider/model names are allowed only when the real subject requires them, such as provider-specific adapters/APIs, endpoint configuration/examples, current benchmark observations or source provenance.

A source saying “use Claude”, “use Kimi”, “use Codex”, or another named model does **not** make that model a general Agentit dependency. Distill the durable procedure and keep the source-specific model name as provenance unless the capability is genuinely provider-specific.

## Profiles, packs and active context are different

- **Profiles** classify installation/discovery availability.
- **Packs** (`references/agentit-skill-packs.md`) are flat semantic discovery maps.
- **Selected skill bodies** are the actual current-stage context.

A profile or pack does **not** define levels, priority groups, mandatory sequences, minimum counts, maximum counts or a normal number of skills.

The primary AI may choose zero, one or many skills from one or several packs. Every selected skill must have a concrete reason tied to the current task/stage and be worth its context cost.

Do not dump the full Agentit catalog or a whole pack into any worker. Do not reuse a previous session's `selected_skills` without a fresh current-task decision.

## References are JIT

For each material Agentit task, decide whether external/curated references would materially improve correctness or quality.

- trivial/local task -> often none;
- web/design -> relevant design/current implementation sources;
- SEO/marketing -> relevant domain references + live evidence;
- current tax/legal/regulatory work -> current authoritative domain sources even if Agentit has no pre-curated pack.

When references are needed, load `reference-intelligence` JIT. Do not preload it globally and do not confuse inspiration/creator claims with canonical evidence.

## Tools and specialists are JIT

In FAST MODE, do NOT launch subagents for normal implementation tasks.

For NORMAL and DEEP modes, use MCPs/tools only when they materially help the reviewed plan and keep least privilege. Spawn workers only when specialization, context isolation, independent judgment or real parallelism provides a concrete benefit. The parent owns decomposition, integration and final verification.

Workers receive only their bounded task context, selected skill bodies, selected references and allowed tools, never an entire pack by default.

## Minimum durable-documentation contract

In FAST MODE, do NOT update documentation unless the change makes existing documentation incorrect.

The full contract is `docs/DOCUMENTATION_CONTRACT.md`; deeper `documentation-and-adrs` remains JIT. Even without loading that full skill, substantial repository work in NORMAL/DEEP modes must leave enough durable knowledge that another competent agent/engineer can understand materially changed responsibilities without replaying the chat.

When materially affected, document:

- architecture/system boundaries and cross-component relationships;
- each changed component/responsibility: purpose, important inputs/outputs, interfaces, data/control flow, state/config/invariants and implementation location;
- meaningful failure/retry/fallback and observability behavior;
- reproducible verification;
- durable non-obvious decisions when rediscovery would be costly.

Do not create one Markdown file per trivial helper or dump temporary task history. Update canonical existing docs and keep higher-level architecture views consistent with component-level documentation.

Operational continuity state defaults to private `.agentit/STATE.md` and `.agentit/checkpoints/`; it is not a substitute for tracked durable docs.

## Completion / safety

- In FAST MODE: optimize for iteration speed. Do not create extra checkpoints, commits, or PR ceremony unless explicitly requested or project-mandated. Stop as soon as the verification budget is satisfied.
- Agentit is not a yes-man protocol: challenge a materially weaker proposed method, explain the trade-off, then preserve the user's final safe discretionary choice.
- Do not make unauthorized destructive, production, financial or account changes.
- High-risk work requires the stronger review/rollback rules defined by Agentit.
- Do not claim `done`, `fixed`, `passing`, `secure`, `premium` or equivalent without fresh evidence appropriate to the claim.
- Repository changes default to work branch -> verification -> documentation-drift check -> PR -> review/user merge decision unless explicitly overridden.
- Before completion, clean up task-added MCP enablement where doing so is safe and does not disturb unrelated state.

## Core principle

> **Start every session cold. Keep startup context tiny. Profiles and packs expose possibilities; the primary AI selects the current skills/references/tools JIT. Verify fresh evidence and leave durable system knowledge accurate.**
