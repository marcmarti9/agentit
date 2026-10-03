# Checks for common analytical claims

Read this reference only when the corresponding shape appears in the analysis.

## Joins and entities

Declare the expected relationship before joining: one-to-one, one-to-many, or many-to-
many. Compare entity counts and row counts on both sides and after the join. If a
one-to-many table is joined to a per-entity metric, aggregate it to the intended grain
first or demonstrate why duplication is harmless.

## Time series and comparisons

Use a documented timezone and inclusive/exclusive boundary convention. Check partial
first/last periods, ingestion lag, calendar versus rolling windows, and changes to event
definitions or tracking. Compare like periods (for example, complete weeks with complete
weeks) and show absolute counts alongside rates.

## Rates, funnels, and cohorts

Specify eligibility before computing a denominator. A conversion rate needs a defined
opportunity to convert; a funnel needs ordering, a session or entity identity, and rules
for repeated events. For cohorts, record cohort-entry event, membership date, and whether
later identities can join more than once.

## Provenance

This Agentit-authored adaptation and this reference are licensed Apache-2.0. They are
source-informed by ajrcre's MIT-licensed `data-analysis` skill at
commit `cbc906e4912a980423aecd1e318061eb98f3e0b2`, inspected 2026-10-03:
<https://github.com/ajrcre/data-analysis-skills/blob/cbc906e4912a980423aecd1e318061eb98f3e0b2/data-analysis/SKILL.md>.
The pinned source `LICENSE` is MIT, copyright `Copyright (c) 2026 ajrcre` (SHA256
`fe80e84c999e740339b53890b2fc9fe77014ff9b36ec10abbb2dec1a9afac7d4`), retained at
`vendor/adaptation-licenses/ajrcre--data-analysis-skills/LICENSE`. This source notice and its
MIT copyright and permission notice must accompany any distributed substantial source
material. No upstream text, scripts, assets, or runtime contract are included here; the
source-informed scope is limited to evidence retention, metric definition, and data
validation principles.
