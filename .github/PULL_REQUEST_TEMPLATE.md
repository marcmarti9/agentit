## Problem

<!-- What real failure mode, user need, or maintenance problem does this solve? -->

## Change

<!-- Describe the smallest useful change. If this adds a skill, explain why strengthening an existing skill was insufficient. -->

## Evidence

<!-- Commands, tests, reproductions, screenshots, receipts, or comparative evidence. Do not claim more than this evidence supports. -->

```text
<verification here>
```

## Agentit invariants

- [ ] No programmatic natural-language router/classifier was introduced.
- [ ] Deterministic code is enforcing mechanical state/invariants, not pretending to make semantic product decisions.
- [ ] Delegation/topology changes have a concrete benefit rather than adding hierarchy by default.
- [ ] New/changed managed filesystem behavior is bounded, explicit, and reversible.
- [ ] Durable docs were updated if architecture/operations/contracts changed.
- [ ] Public claims are backed by evidence for this revision.

## Skills / upstream provenance

<!-- Delete if not relevant. -->

- [ ] I checked `docs/SKILL_CURATION.md` before adding a new skill.
- [ ] Existing Agentit coverage was inspected for overlap.
- [ ] Any substantial upstream adaptation has source + license/provenance in `THIRD_PARTY_NOTICES.md`.
- [ ] External hooks/installers/tool configs were treated as untrusted and reviewed before adoption.

## Risk / rollback

<!-- What can break? Is the change reversible? For high-consequence work, what independent review/verification was used? -->
