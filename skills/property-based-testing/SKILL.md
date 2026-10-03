---
name: property-based-testing
description: >-
  Design, implement, or review property-based tests when behavior must hold across a generated input domain: codecs, parsers, normalizers, validators, ordering, numeric logic, state transitions, and invariants. Use after choosing a test target and before adding a generator-based test, or to investigate a minimized counterexample. Do not use for example-only unit tests, coverage-guided fuzzing, mutation testing, performance benchmarks, or browser flows.
license: CC-BY-SA-4.0
---

# Property-Based Testing

Property-based testing checks a named rule across generated valid inputs. It complements
the example-focused red-green-refactor loop in `test-driven-development`; it does not
replace targeted examples, integration tests, or a release gate.

## Scope the candidate

1. Inspect the public behavior, existing tests, and the repository's test runner before
   choosing a library or changing a dependency.
2. State the operation, input domain, observable result, and the business or technical
   rule that must always hold. If the rule cannot be stated without repeating the
   implementation, use example tests or refactor a seam first.
3. Choose the strongest independent oracle available:

   | Shape | Useful property |
   | --- | --- |
   | encode/decode or parse/print | round trip over the defined representable domain |
   | normalize/canonicalize | idempotence and preservation of required meaning |
   | ordering | monotonic output and permutation preservation |
   | set/map algebra | identity, commutativity, associativity where the contract promises them |
   | replacement/optimization | agreement with a simpler trusted implementation |
   | stateful workflow | declared invariant after each permitted transition |

   Do not claim an algebraic law where the documented contract does not promise it;
   floating-point arithmetic, lossy codecs, locale-aware collation, and side effects
   commonly need a bounded or different oracle.

4. Record the domain boundary explicitly: valid values, invalid values that should be
   rejected, equivalence rules, and any intended lossy behavior. Read
   [references/design-and-review.md](references/design-and-review.md) when choosing a
   generator or evaluating an existing property suite.

## Build a meaningful test

1. Reuse the repository's existing property library and conventions when present. If
   none exists, describe the proposed library, test target, and expected maintenance
   cost; adding a dependency remains a project decision.
2. Make generators construct valid structured data directly. Prefer compositional
   strategies (for example, a valid AST built from valid nodes) over broad generation
   followed by repeated filtering.
3. Add boundary examples beside generation: empty input, a minimal non-empty input,
   maximum permitted size, malformed input, and known historical failures where they
   apply. Generated cases do not excuse omitting named regressions.
4. Assert only observable behavior. A property that recomputes the same algorithm or
   compares an expression to itself is not an independent check.
5. Set runs, seeds, deadlines, and shrinking behavior through the repository's normal
   test configuration. Do not mask a failure by globally reducing generated cases,
   discarding failing inputs, or making a test nondeterministic.

## Execute and investigate

1. Run the focused test with the repository's normal command and preserve the exact
   minimized input, seed (when supplied), and tool version in the failure report.
2. Classify a failure before editing production code:

   - a product defect: the stated contract is violated;
   - a property defect: the assertion is stronger than the contract;
   - a generator defect: invalid or out-of-domain data reached the assertion;
   - an environment defect: flakiness, timeouts, state leakage, or non-repeatability.

3. Turn a genuine minimized failure into a stable regression example, fix the relevant
   behavior within scope, and rerun both the focused property test and the affected
   ordinary tests.
4. When no independent property exists, report that conclusion and why. Do not add a
   no-crash property merely to satisfy a testing request unless robustness itself is the
   stated contract.

## Review existing property tests

Check each test for a named property, a valid domain, an independent assertion, and a
failure that would be actionable. Flag tautologies, vacuous filters, duplicate examples
presented as generation, assertion-free tests, and unbounded generators that make CI
flaky. Use the reference for examples of each failure mode.

## Completion evidence

- [ ] The target contract and domain boundaries are written next to the test or in the
      task evidence.
- [ ] The generator represents the intended domain without excessive rejection.
- [ ] The assertion uses an independent observable property or oracle.
- [ ] Boundary and prior-regression examples cover known exceptions.
- [ ] Focused property and affected ordinary tests have fresh command output, or any
      blocked check is reported with its reason.
- [ ] Any counterexample, seed, and shrink result are retained in test output or the
      defect record.
