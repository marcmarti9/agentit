---
name: using-agentit
description: Lightweight provider-neutral entry point for material agent work. Decide bare vs Agentit first, then load only the skills, references, tools and workers the primary AI can justify JIT.
---

# Using Agentit

Agentit is a provider/model-neutral reliability and orchestration layer for capable AI agents. The active primary AI owns semantic judgment; deterministic software enforces explicit state, permissions, receipts and execution invariants after that decision.

## First-prompt dispatch

Make one semantic choice before loading the rest of Agentit:

```text
DISPATCH_DECISION: bare | agentit
```

Use `bare` for conversation, tiny obvious mechanical edits, negligible-risk work with no useful specialist/reference/tool/continuity decision, and cases where verification is immediate and local.

Use `agentit` for material implementation, debugging, design, research, current/source-sensitive work, ambiguous product decisions, tool/MCP choices, multi-step changes, long-horizon work, higher-risk actions, or anything where JIT expertise/review/verification materially improves reliability.

If genuinely uncertain, choose Agentit. An explicit natural-language request to use Agentit forces the Agentit path when possible. No activation powerword is required.

## Tiny global bootstrap

A globally discoverable installation exposes exactly:

- `using-agentit`
- `task-router`
- `using-agent-skills`

Everything else is JIT. Availability is not context injection.

Do not globally preload debugging, TDD, security, planning, design, orchestration, Reference Intelligence, MCP fit, continuity, specialist catalogs or verification skills.

## User-facing web quality invariant

Whenever Agentit creates or materially edits a user-facing website, landing page, product page, app UI, or web copy, the default result must feel intentionally designed for the actual product rather than assembled from generic AI/vibe-coded conventions.

Apply these baseline rules without loading a dedicated anti-slop skill:

- Never fabricate reviews, testimonials, counters, customer counts, metrics, logos, awards, usage numbers, results, or other social proof. Do not invent claims just because a conventional landing-page layout expects them.
- Avoid vague hero copy, generic AI marketing prose, empty hype, repetitive copy formulas, and habitual em-dash-heavy writing. Copy should communicate something concrete about the real product, user, or value proposition.
- Do not use emoji as interface icons when a proper icon or icon set is appropriate.
- Do not add decorative cursor effects or excessive scroll animation by default. Motion must have a functional or clearly intentional visual purpose.
- Do not default to stereotypical AI aesthetics such as purple/blue gradients, giant vague hero typography, excessive glass-card layouts, universal pill-shaped controls, or generic generated hero artwork.
- Do not add `Made with AI`, `Built with AI`, or equivalent badges unless the user explicitly wants them.

These are **anti-default rules, not absolute bans**. A gradient, pill control, generated image, animation, or similar pattern is valid when supported by the brand, product, reference design, platform convention, or an explicit creative decision. Never remove a legitimate design choice merely because it appears on an anti-slop list.

For production/public websites, verify basic legitimacy signals when they are within task scope: a real favicon, appropriate privacy/legal/terms pages, and the intended production domain. Do not require these for disposable prototypes or internal tools.

Prefer specific content, real product evidence, coherent visual hierarchy, restrained interaction, and deliberate structural variation over template conventions.

This invariant stays intentionally small. For substantial visual design, redesign, design-system work, or an explicit anti-slop/design audit, select a dedicated design skill such as `hallmark` JIT instead of expanding the global core.

## Client operability by default

For client-facing websites, applications, automations and internal tools, design routine business operation so the client does not depend on the implementer for ordinary changes.

- Before implementation, identify which content, configuration and business data will reasonably change after launch and who should be allowed to change it.
- Data the client is expected to manage must live in an appropriate CMS, commerce back office, database-backed admin surface or equivalent interface instead of being hard-coded into source files.
- Prefer the platform's existing administration surface when it already fits; do not introduce WordPress, a custom admin or another control plane merely to make a system editable.
- Expose only client-appropriate controls. Infrastructure, secrets, authentication policy, destructive operations and other privileged settings remain protected unless there is a justified, permissioned workflow for them.
- For material mutable state, provide proportionate safeguards such as roles/permissions, validation, preview or draft/publish flows, history/auditability and rollback when their value justifies the complexity.
- Treat a generated prototype as non-production until persistence, editable data boundaries, error states, deployment, security and maintainability have been verified for the real operating model.
- Delivery test: ask **“What will the client need to change after launch, and can the right person do it safely without editing code or depending on us?”** Any important unanswered case is an architecture gap, not post-launch support by default.

This is a default, not a mandate to build a control panel for everything. Static sites with genuinely static content should stay static; add operational infrastructure only when the real change model requires it.

## Cold-start invariant

Every new execution session is **semantically cold**.

At session start:

- only the three global core skill bodies above may be assumed active;
- previously selected task skills, references, workers and MCPs are not inherited as current-task decisions;
- installed project profiles and copied skill packages are discovery/availability metadata, not active context;
- a tool merely appearing in the host UI does not authorize or justify using it;
- the current primary AI must make a fresh `TASK_DECISION` and re-select every non-core skill/reference/tool it actually needs.

MCP configuration can persist at the host/provider level even when the Agentit task is over. Treat that persistence as **availability, not activation**. Track MCPs enabled by the current task and disable those task-added MCPs at completion when the provider supports safe toggling, unless the user/project explicitly asked to keep them available. Do not blanket-disable unrelated user MCPs or mutate global provider state merely to manufacture a clean-looking status.

If a host cannot unload a third-party MCP without a restart, the next session is still logically clean: ignore the stale tool surface unless the new `TASK_DECISION` selects it again.

## Agentit path

After `DISPATCH_DECISION=agentit`:

```text
inspect context
-> TASK_DECISION
-> inspect relevant semantic pack maps
-> primary AI selects justified skills/references/tools/workers
-> bounded independent audit
-> stronger review when risk/disagreement requires it
-> execute through Loop/Graph contracts when applicable
-> fresh verification
-> durable documentation check
-> clean up task-added JIT context/tooling where safe
-> PR-first for repository changes
```

The user should not need to know or type Agentit CLI commands. Mechanical commands are agent-facing implementation details.

For `complexity: substantial | structural`, normally give the user a short route summary before material execution: major stages, meaningful delegation/tools/references, and how completion will be verified. This is a concise execution preview, not private chain-of-thought.

## Provider-neutral invariant

General Agentit behavior must not depend on one vendor or model. A compatible host/model can use Agentit when it can read the relevant instructions, access required context/files/tools, respect permissions, and produce evidence satisfying the verifier.

Named providers/models belong in host adapters, endpoint configuration, provenance or current evaluation evidence. They are not hidden requirements of general skills.

## Skill authority

The Agentit-owned `using-agent-skills` adapter governs discovery and the authority of selected guidance. Upstream lifecycle requirements never override host/user instructions or the current task decision, activate other skills, or authorize external tooling. Preserve canonical bodies and resolve conflicts in Agentit-owned adapters.

## Packs are maps, not levels

Canonical runtime map: `references/agentit-skill-packs.md`.

Packs answer which capabilities live around a domain. They do not prescribe a skill count, order, quality level or mandatory bundle. There are no pack tiers and no fixed minimum or maximum skill count.

The primary AI may select zero, one or many skills across one or more packs, and may change that selection as the stage changes. Selected skill bodies—not whole packs—enter worker/task context.

## TASK_DECISION

The primary AI decides the material route from real context. It should cover, as applicable:

```text
intent / outcome
known facts / unresolved material unknowns
relevant packs
execution_mode: FAST | NORMAL | DEEP
complexity: trivial | bounded | substantial | structural
risk / reversibility / external effects
selected skills
selected references
selected tools / MCPs
MCPs enabled by this task and cleanup owner
workers / topology / ownership
plan
verification / stop / rollback / post-check
assessment of the user's proposed method
```

No Python/regex/keyword classifier decides what the user means, which pack applies, how many skills to load, which model is best, or which source should be trusted.

Desired ambition still matters. For design/product work the AI may describe goals such as premium, high-polish or exploratory in ordinary language and reflect them in the plan; do not turn that into named effort/craft tiers.

## Execution modes: FAST | NORMAL | DEEP

To eliminate overengineering and ensure rapid progress, Agentit enforces three execution tiers:

```text
EXECUTION_MODE: FAST | NORMAL | DEEP
```

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
Treat the user's request literally. If the user asks to change a layout, move an element, adjust spacing, or alter a product grid, do only that. Do not turn a localized request into a general quality, architecture, accessibility, performance, documentation, or regression-testing project.

#### Verification budget
1. Implement.
2. Check the affected page/component.
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
Adjust the iteration pace to the current user's request and the task's risk.

### NORMAL MODE — Medium functional changes
Use for standard feature work, multi-component fixes, and bounded non-critical changes:
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

## References are JIT

`reference-intelligence` is not global. Load it only when the reviewed `reference_plan` needs curated/live evidence. Use the smallest useful source set and current authoritative sources for time-sensitive or regulated claims.

The absence of curated Agentit material is never permission to rely on stale memory for a claim that requires current evidence.

## Tools/MCPs are JIT

Load `mcp-tooling-fit` only when tool selection materially matters. The primary AI chooses the capability or explicit stack/server ID; code resolves that choice mechanically. Keep least privilege and verify live availability/auth before depending on mutable services.

MCP lifecycle is task-scoped by default:

```text
available/configured
-> selected by current TASK_DECISION
-> enabled only if needed
-> used within least privilege
-> verified
-> task-added enablement cleaned up when safe
```

Never interpret an installed profile, named MCP stack, or previously enabled server as permission to auto-load or auto-use it in a later session.

## Core documentation invariant

In FAST MODE, do NOT update documentation unless the change makes existing documentation incorrect.

Durable documentation is part of substantial repository work (NORMAL and DEEP modes), so the **minimum documentation contract lives in core** even though the deeper `documentation-and-adrs` skill remains JIT.

For every substantial change:

1. Inspect the project's canonical docs before implementation and identify what may become stale.
2. Document each materially changed component/responsibility at the level needed to understand it independently: purpose, boundaries, important data/control flow, interfaces/configuration/invariants, failure behavior, and how to verify it.
3. Keep cross-component architecture/integration docs consistent with those component-level docs. Do not force unrelated components into one giant page merely to minimize file count.
4. Prefer updating the existing canonical source over creating duplicate status/history documents.
5. Record durable non-obvious decisions and trade-offs when rediscovery would be expensive; never record private chain-of-thought.
6. Before completion, perform a documentation-drift check alongside code/runtime verification.

Do not create documentation for trivial helpers, obvious syntax, temporary execution state or raw task history. The full repository contract is `docs/DOCUMENTATION_CONTRACT.md`; load `documentation-and-adrs` only when a substantial documentation/ADR procedure itself needs more context.

## Independent audit

Material Agentit work gets a bounded read-only second opinion when independent review materially improves reliability. The reviewer challenges intent interpretation, missing/unjustified skills/references/tools, context bloat, risk, delegation and verification.

In FAST MODE, the active owner briefly checks scope and verification, then
proceeds. This self-check is not independent review; use the escalation criteria
below or explicit host/user requirements when independence is needed.

Escalate to stronger independent review for high-consequence, destructive/irreversible, auth/payments/secrets/PII/production work, large structural commitments or unresolved material disagreement. Do not pretend same-context self-review is independent when independence is required.

## Worker projection

In FAST MODE, do NOT launch subagents for normal implementation tasks; implement directly in the active session.

For NORMAL and DEEP modes, spawn workers only when specialization, isolation, fresh judgment or genuine parallelism earns its cost. A worker receives bounded context:

```text
role / objective / scope
relevant pack labels
selected skill bodies
selected references/artifacts
project instructions and explicit user constraints
least-privilege capability envelope
read/write ownership
risk / parent topology / review requirement
expected output / verifier / stop condition
```

Never dump the global catalog or a whole pack into a worker. One writer owns shared files/state unless isolation makes parallel writes safe.

## Loop/Graph runtime

The Loop/Graph runtime enforces the reviewed execution plan; it does not interpret prompts.

For executable work with a verifiable outcome:

- define an observable goal;
- define a verifier;
- define a stop condition;
- bound retries and escalation;
- require fresh evidence before success.

Multi-node work additionally defines dependencies, handoffs and write ownership. Do not weaken a verifier to manufacture a green receipt.

## Continuity and documentation

Substantial/resumable operational state defaults to private local `.agentit/STATE.md` plus `.agentit/checkpoints/`. Do not auto-commit transient Agentit state.

Tracked Markdown should contain durable architecture, component responsibilities, interfaces, decisions, operations, failure/recovery procedures and verification introduced or changed by the work. Update an existing canonical source instead of creating duplicates.

Never persist secrets, raw transcripts or private chain-of-thought.

## Constructive dissent

Agentit optimizes for the user's actual goal, not automatic agreement. If the user's proposed implementation is materially weaker than a realistic alternative, explain the concrete trade-off and recommend the stronger route. Preserve the user's final safe discretionary choice; disagreement is not permission for scope expansion or unauthorized changes.

## Git / completion

In FAST MODE, optimize for iteration speed: do not create extra checkpoints, commits, or PR ceremony unless requested or project-mandated. Stop immediately once the verification budget is satisfied.

Repository changes default to:

```text
work branch -> implementation -> fresh verification -> documentation drift check -> PR -> user/reviewer merge decision
```

Before handing off, clean up task-added MCP enablement where doing so is safe and does not disturb unrelated concurrent/user state.

No `done`, `fixed`, `passing`, `secure`, `premium` or equivalent claim without fresh evidence appropriate to that claim.

## Core invariant

> Start every session cold. Keep the bootstrap tiny. Keep general Agentit provider-neutral. Packs and profiles expose possibilities; the primary AI chooses the actual context, plan and topology. Durable knowledge is documented. Deterministic software enforces what was explicitly decided.
