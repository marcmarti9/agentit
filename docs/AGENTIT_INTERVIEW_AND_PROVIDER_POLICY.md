# Agentit task planning and provider-neutral execution

Agentit owns the work protocol. Providers supply execution primitives.

## 1. Primary AI owns the semantic task decision

After the first meaningful `bare | agentit` dispatch, the active primary AI uses the real conversation, repository, files, tools, instructions, and state to produce `TASK_DECISION`. No regex, keyword table, score, or Python classifier decides user intent, packs, skill count, tools, risk, or worker topology.

For material Agentit work, the decision covers outcome, known facts/unknowns, relevant packs, complexity, risk, selected skills/tools/references, topology/workers, plan, verification, rollback/post-check, and assessment of the user's proposed method.

## 2. Inspect before asking

Discoverable project facts should normally be inspected rather than turned into questions. Ask the user only for unresolved material decisions, permissions, preferences, or trade-offs that cannot be safely inferred.

When several current material questions are known, batch them coherently. Follow up only when new evidence creates genuinely new decisions.

## 3. Packs are flat discovery maps

Runtime packs are model-readable semantic maps. They have no required depth level, fixed ordering, or prescribed skill count. The primary AI selects the concrete skill bodies that earn their context cost for the current stage/worker.

Task depth still exists as judgment, not as a vocabulary. `TASK_DECISION.complexity` (`trivial | bounded | substantial | structural`), the plan, selected capabilities, topology, and verification describe how much work the task deserves. For design/product work the agent may also describe the desired ambition naturally (for example, high-polish or premium) when that affects the plan; no named tier is required.

## 4. User-facing route summary

For substantial or structural tasks, normally tell the user the short route before material execution: major stages, important tools/references, delegation if any, and how completion will be verified. Do not turn this into ceremony for bounded work, and do not expose private chain-of-thought.

## 5. No activation powerword

After installation, Agentit performs semantic first-task dispatch automatically. An explicit request such as “use Agentit” forces the Agentit path when possible, but the user does not need to prepend a phrase to every material task.

## 6. Independent review and delegation

Material decisions receive the configured independent audit. High-risk, destructive, difficult-to-reverse, auth/payments/secrets/PII/production, large structural commitments, or unresolved disagreement require stronger independent review.

Delegate when specialization, isolation, fresh judgment, or genuine parallelism earns its cost. Specialists are optional capabilities, never a mandatory org chart. Catalog trigger text is model-readable discovery metadata, not a software router.

## 7. Loop / Graph execution

Semantic choices belong to the AI; deterministic runtime enforces the reviewed mechanical plan. Executable units with verifiable outcomes use bounded Loop contracts and fresh evidence. Multi-node dependent work uses Graph contracts with explicit dependencies, ownership, handoffs, and node receipts.

## 8. Continuity and documentation

Operational task state defaults to local/private `.agentit/STATE.md` plus `.agentit/checkpoints/`. It must not be committed merely to make Agentit resumable. Durable architecture/product/operations knowledge belongs in the project's normal tracked documentation when the work actually creates such knowledge.

See `docs/PROJECT_CONTINUITY.md` and `docs/DOCUMENTATION_CONTRACT.md`.

## 9. Provider-neutral specialist contract

General roles are logical capability bundles. Preferred fallback order is provider-native scoped worker -> another isolated delegated context -> parent with the same bounded skill bodies. If genuine independent review is required, loss of independence must be visible and may require escalation instead of fallback.

Provider/model names belong only in adapters, endpoint configuration, current observations, or provenance. General Agentit contracts remain provider-neutral.

## 10. MCP / tools

The primary AI chooses tools or an explicit named MCP stack from full context. Software may resolve that explicit ID mechanically. Tool enablement remains least-privilege and follows the applicable review/consent gate.

## 11. PR-first repository changes

Repository mutations default to work branch -> commits -> fresh verification -> PR -> review/user merge unless the current task explicitly authorizes another workflow.

## 12. Non-interactive execution

Do not fake interviews, permissions, or independent reviews. When a material decision cannot be safely inferred and no user input is available, prefer a conservative non-mutating path or explicit escalation.
