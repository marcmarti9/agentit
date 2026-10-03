---
name: data-analysis-quality
description: Validate whether a dataset, query result, metric calculation, or analytical claim is fit for a stated decision. Use before presenting counts, rates, trends, funnels, cohorts, dashboards, exports, or comparisons from structured data. Do not use to operate a database, design a dashboard, perform statistical modelling, or replace a domain-specific data contract.
license: Apache-2.0
---

# Data Analysis Quality

This skill establishes whether an analysis can support its stated claim. It owns the
quality and traceability gate around an analysis; it does not own query syntax, chart
design, statistical inference, data cleaning, or independent review.

## Define the claim before trusting the number

Write an analysis definition that a second analyst could implement:

```text
decision/question:
metric and numerator/denominator:
unit of analysis (grain):
population and deliberate exclusions:
time window, timezone, and comparison baseline:
source tables/files and refresh/cut-off time:
known assumptions and expected failure modes:
```

If a required field is unknown, label the result exploratory or pause for clarification.
Never turn an unconfirmed environment, date range, timezone, population, or exclusion
into an invisible default.

## Inspect the source before aggregation

1. Capture an immutable or versioned source reference when the platform permits it:
   file checksum/version, query identifier and parameters, warehouse snapshot, or export
   timestamp. Do not record credentials or raw personal data in evidence.
2. Profile the raw result at its intended grain:

   - row count and distinct entity count;
   - schema and type coercions;
   - minimum/maximum timestamps and missing intervals;
   - null, duplicate, and out-of-range rates for fields used in the claim;
   - category distributions and unexpected values;
   - join cardinality before and after every material join.

3. Reconcile at least one aggregate with a source-system total, prior validated report,
   or an independently derived query when a suitable comparator exists. A mismatch is a
   finding to explain, not a value to normalize away.
4. Check for test/internal records, late-arriving data, deleted/soft-deleted records,
   sampling, retries, and definition changes that could alter the population.

Read [references/claim-checks.md](references/claim-checks.md) when the analysis uses
joins, time series, rates, cohorts, or a comparison period.

## Make transformations reviewable

1. Keep the query, notebook, or transformation script with its parameters and input
   version. A manually transcribed total is not reproducible evidence.
2. State every filter, grouping, deduplication rule, type conversion, imputation, and
   exclusion in the result or its adjacent evidence.
3. For each derived metric, retain the formula, numerator, denominator, rounding rule,
   and the value before display formatting. For percentages, show the base count.
4. Separate direct observation from interpretation. "Conversion was 24/120 (20%)" is a
   fact; "the campaign caused the decline" requires a causal design and remains a
   hypothesis without one.
5. If a quality defect materially changes confidence, either repair it with an auditable
   rule and report the impact, or withhold the affected claim. Do not silently drop rows.

## Report a decision-grade result

Every final finding should include its metric definition, scope, time window, source
reference, calculation, and caveat. State what was checked, what could not be checked,
and how that limitation affects the conclusion. Label sampled, preliminary, and
unreconciled values as such.

For high-impact work, arrange an independent re-derivation from the saved query/data
artifacts. Same-context rereading is useful review but is not independent verification.

## Completion evidence

- [ ] The metric, grain, population, window, and exclusions are explicit.
- [ ] Source version/cut-off and query or transformation parameters are retained.
- [ ] Coverage, schema, nulls, duplicates, ranges, and join cardinality were checked for
      fields material to the claim.
- [ ] At least one suitable reconciliation or independent derivation was attempted, with
      discrepancies explained or reported.
- [ ] Formulas and base counts make each derived value traceable.
- [ ] Facts, interpretations, and limitations are visibly distinct.
