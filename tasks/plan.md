# Implementation Plan: Router Explainability and Representative Evals

## Overview

Convert the external alpha feedback into a focused proof-oriented improvement: make
the heuristic router explicit about the signals behind a decision, avoid treating a
sensitive word in a presentation-only task as sufficient evidence of high risk,
publish a small reproducible evaluation set, and make the physical skill installation
respect a bounded global discovery budget.

## Architecture Decisions

- Keep routing deterministic and provider-neutral; add explainability as derived
  metadata rather than introducing a model, network call, or project inspection.
- Treat `confidence` as an uncalibrated heuristic confidence score, not a probability.
  The output will say so explicitly until labeled historical data exists.
- Keep single-agent-first as the default. Use `writer_reviewer` only when the task
  requests a substantive RISK_3 implementation that benefits from independent
  verification; keep `audit` for high-risk review/operational work.
- Add a standard-library evaluation runner and checked-in representative cases. It
  will measure router decisions only and will not claim agent quality, token savings,
  or production readiness.
- Treat `profiles.yaml` as the install/profile policy for the 28 repository skills:
  `core` is the default global profile and provider installers copy only that
  profile; project profiles add skills under a project-local `.agents/skills` tree.
- Keep all skill bodies in the repository and avoid merging or deleting them in this
  iteration. Shorten only discovery frontmatter descriptions so the catalog remains
  discriminative under a small provider budget.
- Project activation is plan-first and manifest-backed. It never overwrites a
  modified managed file and never removes an unmanaged file.

## Task List

### Phase 1: Foundation

- [x] Task 1: Add regression tests for presentation-only sensitive wording and the
  explainability/topology contract.
- [x] Task 2: Implement contextual signals, uncalibrated confidence, rejected
  topology reasons, and the `writer_reviewer` selection while preserving existing
  safety gates.
- [x] Task 2b: Add the profile catalog, classify 10 core skills as global, and mark
  the remaining repository skills as on-demand without deleting their bodies.

### Checkpoint: Router

- [x] All router tests pass.
- [x] CSS/payment wording remains low risk while real payment/auth changes remain
  high risk.
- [x] Every output includes actionable signals and explicit topology trade-offs.

### Phase 2: Evidence

- [x] Task 3: Add representative JSON cases and a deterministic `evals/run.py`
  command with concise and JSON reports.
- [x] Task 4: Add eval runner tests and document the scope and limitations of the
  evaluation rather than presenting it as a quality benchmark.
- [x] Task 4b: Make `install.sh` and `update.sh` use the profile policy where
  applicable, and add `agentit enable|disable|status` for project-local profiles.
- [x] Task 4c: Add an explicit `--prune-on-demand` migration path for older global
  installs, guarded by exact hashes and backups.

### Checkpoint: Evals

- [x] The case manifest runs without failures.
- [x] The runner reports the case count and pass/fail status.
- [x] No external service, real HOME, or destructive operation is used.

### Phase 3: Public contract

- [x] Task 5: Update README and `router/SKILL.md` with concrete Direct, Probe,
  Fan-Out, Writer-Reviewer, and Audit examples plus the explainability fields.

### Checkpoint: Complete

- [x] Router, eval, script, syntax, YAML, and JSON checks pass.
- [x] Documentation accurately labels the router as deterministic/heuristic and the
  evals as a regression suite, not a calibrated quality claim.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| New contextual heuristics change existing safety behavior | High | Write regression tests first and preserve the highest-risk action gates. |
| A numeric confidence is mistaken for statistical certainty | Medium | Include `confidence_calibrated: false` and document the limitation. |
| Examples drift from the actual router | Medium | Generate README example output from the checked-in CLI after implementation. |
| Eval cases overstate real agent quality | Medium | Limit the runner to expected router fields and state non-goals prominently. |

## Open Questions

- A future version should collect reviewed classifications before attempting
  calibration or comparing agent quality against a baseline.
