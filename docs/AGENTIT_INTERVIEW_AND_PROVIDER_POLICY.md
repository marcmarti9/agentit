# Agentit interview, domain packs, craft depth, and provider-neutral execution

Agentit owns the work protocol. Providers own only the execution primitive.

## 1. AI decision before product interview

Agentit has no programmatic natural-language router. The active primary AI inspects the available conversation, repository, files, tools, instructions and state, then owns the semantic `TASK_DECISION`.

For product-affecting work, inspect discoverable facts first. If material user decisions remain unresolved, use `interview-me` before implementation. Mechanical chores with no product decision can bypass the interview, but not task understanding, review or verification.

## 2. Batch every currently identifiable material question

Ask all currently identifiable material user decisions in one useful batch with recommendations. Follow up only for genuinely new decisions. Do not ask the user to repeat facts that are already available in project or conversation context.

## 3. Domain packs are AI-selected knowledge families

Machine catalog: `effort/levels.yaml` + `profiles.yaml`.

The primary AI chooses the smallest useful domain pack for each stage: engineering, frontend, design, backend, data, product, writing, release, research, or another clearly scoped role.

Profiles and registries are inventories, not classifiers. Load actual skill bodies only when relevant; an ID in metadata is not proof a skill was used.

## 4. Craft depth is design/visual only

Standard / Polished / Studio apply only to visual/design craft. They do not gate ordinary APIs, infrastructure, pure logic or documentation.

Lean / normal / thorough may describe non-design rigor, but they are guidance rather than semantic routing outputs.

## 5. Effort and token estimates are contextual guidance

Do not present fixed token tables as authoritative bills and do not derive semantic decisions through a deterministic `token_estimate` router.

The active model may provide a rough contextual effort/token estimate when useful, based on inspected project scope, risk, dependencies, topology and evidence. Such estimates never decide category, risk, topology, skills or delegation.

## 6. No task-routing powerwords

Only natural Agentit activation in the user's language is special. After activation, the primary AI interprets ordinary language from full context. No regex, keyword table, scoring script or prompt classifier decides task meaning.

## 7. Independent decision review and intelligent delegation

Before material execution, the proposed `TASK_DECISION` receives a read-only economy audit from the cheapest competent independent model, normally semantic tier `fast`.

`CHALLENGE` requires primary reconsideration. `ESCALATE`, unresolved material disagreement, `RISK_3/RISK_4`, destructive or difficult-to-reverse work, auth, payments, secrets, PII, production, significant migrations and large structural plans require a stronger independent `critic`/`judgment` review before material execution.

Delegate when specialization, isolation, independent hypotheses, breadth, latency or fresh judgment adds value. Do not force single-agent or multi-agent execution as ideology.

## 8. Loop/Graph execution runtime remains mandatory

The semantic router was removed; the mechanical execution guarantees were not.

Every executable unit with a verifiable outcome must use a persisted Loop Contract and is accepted only after fresh verifier evidence and a passed Loop Receipt.

Multi-node execution must additionally materialize a Graph Contract with dependencies, ownership and handoffs. Final multi-node acceptance requires a passed Graph Receipt backed by the node Loop Receipts.

Loop/Graph infrastructure enforces a plan after the AI has decided it. It must never infer natural-language intent, category, risk, topology, skills or delegation.

## 9. Continuity

Chat is disposable. Persist `docs/agentit/STATE.md` (or the project's canonical equivalent) per `docs/PROJECT_CONTINUITY.md` for substantial work.

Record compact durable state: objective, confirmed constraints, `TASK_DECISION` summary, economy-review verdict, strong-review verdict when required, domain pack/craft depth/effort, worker ownership, branch/PR, verification evidence, blockers and next actions. Do not persist secrets or private chain-of-thought.

## 10. PR-first

`work branch -> commits -> verification -> PR -> user merge` unless explicitly overridden for that task.

## 11. Provider-neutral specialist contract

Catalog roles are logical bundles. Fallback order is provider-native scoped worker -> isolated delegated call/fresh context -> parent with the same bounded skill bodies and execution contracts.

A missing independent strong review for high-risk work must degrade visibly rather than being silently replaced by same-context confidence.

## 12. MCP fit

Use `mcp-tooling-fit` and `agentit mcp` to inspect the catalog and explicitly selected named stacks. The primary AI chooses a stack from full context; software resolves that exact `stack_id` mechanically.

MCP activation remains opt-in and plan-first. RISK_3+ tooling requires the applicable review and force/consent gate.

## 13. Cross-provider compatibility

Shared policy describes semantic capability tiers for OpenAI, Anthropic, Google, xAI and compatible clients, not one vendor's model names or subagent API.

## 14. Non-interactive execution

Do not fake interviews or independent reviews. If a material decision cannot be safely inferred and no user input is available, block or take the conservative non-mutating path rather than inventing permission.
