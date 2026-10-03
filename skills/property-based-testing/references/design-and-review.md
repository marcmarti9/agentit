# Designing and reviewing property-based tests

Use this reference only when a property test is being designed, debugged, or reviewed.

## Generator checks

Start from the contract, then generate its components. A parser accepting a grammar
should receive generated grammar trees; a money type should receive allowed currencies,
scales, and amounts; a state machine should receive only transitions enabled from its
current state. Filters are acceptable for rare final constraints, but a high rejection
rate is a signal that the generator is modelling the wrong domain.

Use a bounded size appropriate to the operation. A property test that creates large
recursive structures can hide a stack or timeout problem; if that size is meaningful,
name it as a separate stress test rather than silently treating it as a normal case.

## Assertion checks

Ask what implementation mutation would make the property fail. If the answer is "none",
the property is tautological. For instance, `sort(xs) == sort(xs)` proves nothing;
`is_sorted(sort(xs)) && multiset(sort(xs)) == multiset(xs)` constrains two observable
outcomes. A reference implementation is useful only when it is materially simpler or
independently implemented; copying the same branching logic produces a correlated bug.

## Counterexample handling

Treat shrinking as a diagnosis aid, not a proof. Reproduce the minimized value under the
same configuration, inspect whether it is within the declared domain, then preserve it as
an example if it reveals a product defect. If it identifies an unspecified edge case,
clarify the contract before changing either implementation or property.

## Review questions

- What exact contract does this assert, and where is that contract defined?
- Can a valid generated input violate it because of a real implementation mutation?
- Are discard/filter rates visible and proportionate?
- Could repeated runs produce a different result because of time, I/O, shared state, or
  random seeds outside the framework?
- Is a small explicit regression test warranted in addition to the generated test?

## Provenance

This Agentit adaptation and this reference are licensed CC-BY-SA-4.0. They are a
substantial procedure adaptation informed by Trail of Bits' property-based-testing skill
at commit `82fe8226252622fa807643bdca1710901198553a`, inspected 2026-10-03:
<https://github.com/trailofbits/skills/blob/82fe8226252622fa807643bdca1710901198553a/plugins/property-based-testing/skills/property-based-testing/SKILL.md>.
The source repository's root `LICENSE` is CC BY-SA 4.0 (SHA256
`7abe19ec9bb73b36141b999b861d24ad855e808bafe0f81e84cce28556f6c297`), retained at
`vendor/adaptation-licenses/trailofbits--skills/LICENSE`. Distributed copies must credit Trail
of Bits and the pinned source, link the CC BY-SA 4.0 license, indicate this adaptation,
and remain available under CC-BY-SA-4.0. No upstream scripts, assets, installers, or
runtime contract are included.
