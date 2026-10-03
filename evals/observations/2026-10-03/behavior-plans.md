# Observed behavior plans

These are bounded plans derived from the exact selected skill bodies and their relevant references. They do not represent execution of the hypothetical application, scanner, renderer, or device flows.

## pbt-sort — `property-based-testing`

1. Inspect the sort function's documented comparator/order contract, existing tests, and repository test runner.
2. State the valid generated domain, including duplicates, empty input, comparator semantics, and any excluded non-orderable values.
3. Replace `sort(xs) == sort(xs)` with independent observable assertions: output is ordered according to the contract and its multiset equals the input's multiset. Add named boundary examples and any historical regression separately.
4. Configure deterministic seeds/runs/shrinking through the existing test setup, run the focused property test and affected ordinary tests, and retain a minimized counterexample if one occurs.

Boundary: do not claim stability, locale ordering, mutation behavior, or a total order unless the real contract promises it; do not add a new property-test dependency merely from this plan.

## data-join — `data-analysis-quality`

1. Write the decision, customer-level metric, numerator/denominator, intended grain, population, period, sources, and exclusions.
2. Profile row and distinct-customer counts before and after the customer-to-orders join; declare the expected one-to-many relationship.
3. Aggregate orders to the customer grain before joining, or demonstrate why row duplication cannot affect the calculation; retain query/version/parameters.
4. Reconcile the result with an independent customer-level derivation and report the original and corrected values, formulas, base counts, and remaining limitations.

Boundary: the stated counts alone cannot establish a valid average or causal explanation; no query was run by this plan.

## data-causal — `data-analysis-quality`

1. Record conversion definitions, eligibility, period/timezone, sources, rollout details, and the two base counts.
2. Report the direct observation accurately: 20/100 to 25/100 is a five-percentage-point change and a 25% relative change in the observed rate.
3. Check comparability of periods, tracking/definition changes, sampling, late data, and other concurrent changes; preserve the calculation and source cut-off.
4. Withhold a causal claim unless a suitable causal design or comparator is available; label the copy explanation as a hypothesis otherwise.

Boundary: this quality procedure does not itself supply an experiment, statistical model, or causal identification strategy.

## security-sarif — `security-analysis`

1. Capture the exact revision, scanner/version, command, ruleset, configuration, SARIF, extraction/build logs, and intended Python scope.
2. Compare intended Python paths with extraction coverage and exclusions. Classify the zero-alert output as coverage-inconclusive when no Python files were extracted.
3. Repair or correctly configure scan targeting only after establishing the real source layout, then rerun the focused scan and record its examined paths.
4. Report the coverage boundary separately from findings; a clean rerun only covers the actual examined target.

Boundary: a zero exit code and empty SARIF do not establish absence of Python vulnerabilities; no scanner command is run here.

## security-authz — `security-analysis`

1. State the target revision, protected record, principals A and B, endpoint/entry points, tenant and authorization invariant.
2. Trace request-controlled identifier through routing, authentication, authorization/ownership check, persistence sink, and alternate/error paths.
3. Classify reachability, effective control, affected scope, and confidence. Parameterized SQL and login are recorded as controls with scopes distinct from object authorization.
4. Where safe and locally authorized, design a benign fixture asserting A is denied an update to B; propose remediation at the authorization decision and retest the focused path.

Boundary: no production probing or destructive payload is implied; missing deployment/identity evidence keeps the classification conditional.

## mobile-failed-save — `mobile-runtime-engineering`

1. Inspect the actual RN route/component, installed versions, state owner, mutation API, and native build/platform before selecting implementation details.
2. Define the flow: draft exists, submit starts, timeout occurs, draft remains with clear failed/unsynced state, and retry resolves one server record.
3. Preserve the authoritative draft on failure, prevent repeat submissions in flight, and use the product idempotency/reconciliation contract when a timeout might follow server success; cancellation alone is not rollback.
4. Verify focused race/state checks plus failed save → retry, double tap, navigation during response, background/resume, account switch, and timeout-after-success on an available target device/simulator.

Boundary: this plan does not create an offline queue, replace the state manager, add native modules, upload with EAS, or claim release-device verification without observed evidence.

## artifact-pdf — `artifact-production`

1. Establish audience, required content/data, fixed page dimensions, print/screen use, editable-source format, font/accessibility needs, and actual authoring/rendering tools.
2. Build a representative page first with meaningful structure, then produce both the PDF and promised editable source.
3. Render or open every saved PDF page through an available supported route; inspect clipping, glyph/font substitution, text size, tables, margins, numbering, and final page. Extract text separately to check headings, values, and encoding.
4. Deliver the actual final files and state which accessibility properties and rendering route were checked.

Boundary: visual rendering alone does not prove tags, reading order, selectable text, or editable-source fidelity; this plan does not transmit material to an external renderer.

## artifact-sheet — `artifact-production`

1. Define raw-input, calculation, and presentation ranges; preserve numeric/date types and make input cells distinct.
2. Use formulas for revenue totals and keep units, denominators, data assumptions, and unavailable inputs visible.
3. Open the saved workbook in an available calculation engine and check formula results against independent control totals. Change a source input to confirm recalculation.
4. Test blank input, duplicate keys, divide-by-zero behavior, filter/sort behavior, realistic row volume, widths, frozen headers, locale formats, and formula-injection handling for untrusted text.

Boundary: a cached plausible value is not recalculation evidence; no macro, external connection, or unobserved target-editor compatibility claim is implied.
