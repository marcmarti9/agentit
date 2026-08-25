# Reference runtime gate

Agentit keeps semantic reference selection in the primary AI while mechanically enforcing the decision afterward.

## Contract

The primary AI decides:

```text
reference_plan.mode = none | catalog | live | mixed
```

The verifier does **not** infer this value from task text.

When the mode is `catalog`, `live`, or `mixed`, `agentit verify --apply` requires:

- one or more selected/inspected source IDs or URLs;
- compact evidence describing what was actually inspected/verified;
- provenance output when the AI marked provenance as required.

If those are missing, the verification receipt is blocking-failed and `receipt.passed` is false.

Example agent-facing call:

```bash
agentit verify "implement public landing" \
  --project . \
  --reference-mode mixed \
  --reference-source web-design-studio \
  --reference-source https://react.dev/... \
  --reference-evidence "Inspected design pack; selected asymmetric editorial hierarchy" \
  --reference-evidence "Verified current React implementation pattern in official docs" \
  --reference-provenance-required \
  --reference-provenance docs/agentit/REFERENCES.md \
  --apply
```

For a repository-local task where external references do not materially help:

```bash
agentit verify "rename private helper" --project . --reference-mode none --apply
```

The purpose is not to force browsing on every task. The purpose is to make a reviewed decision to use references **auditable and enforceable**, so naming a pack in `TASK_DECISION` without ever reading it cannot produce a passing completion receipt.
