# Reference enforcement summary

For material Agentit tasks:

1. The primary AI explicitly chooses `reference_plan.mode = none | catalog | live | mixed`.
2. `none` is valid for repository-local work where external knowledge does not materially help.
3. Curated packs are used only when relevant.
4. If no pack covers a current domain, the AI chooses live authoritative sources rather than model memory.
5. The cheap auditor challenges an unjustified `none` or weak/stale source plan.
6. If mode is not `none`, `agentit verify --apply` requires selected source IDs/URLs plus inspection evidence; required provenance must also be present.
7. Missing evidence makes the verification receipt fail mechanically.

The runtime never infers the domain or reference pack from natural-language task text.
