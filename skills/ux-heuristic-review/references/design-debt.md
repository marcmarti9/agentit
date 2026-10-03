# Design debt inventory

Read only when asked to inventory recurring design drift across a product.
Ordinary one-screen review does not need a debt register.

1. Bound surfaces, states and current system/brand authority. Inventory actual
   instances with captures/source locations; list uninspected surfaces separately.
2. Classify visual inconsistency, structural/navigation drift, accessibility
   evidence gaps, documentation drift or divergent implementation. A different
   treatment can be intentional for a different task; record the intended reason.
3. Group instances by root cause. Record affected screens, impact, occurrence
   count from the inventory, owner/role, effort estimate and its source, dependencies
   and status. Do not extrapolate user reach from screen count.
4. Prioritize serious task/access barriers, then recurring friction and low-cost
   consistency fixes. Keep impact, frequency and effort separate; multiplying
   ordinal labels does not produce reliable risk or exact business value.
5. Separate quick repairs, systemic changes and justified deferrals. Include
   migration/rollback needs where changing a shared component affects consumers.
6. Return a bounded register with evidence and a retest. Mark a finding resolved
   after relevant verification, not after merely editing a token or closing a ticket.

For a real token/component consolidation, the model may select
`design-system-engineering`. This reference inventories drift; it does not own
the migration. No mandatory cadence, backlog service or new control plane is
introduced. Source-informed adaptation of Owl-Listener's design-debt audit.
