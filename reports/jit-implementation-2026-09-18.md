# Agentit adversarial implementation — pass 2, 2026-09-18

## Result and evidence boundary

The baseline audit found a real break between selected skill IDs and delivered worker instructions. The implementation repairs that path instead of replacing model judgment with a keyword router. It also fixes installation/update drift and distinguishes observed command evidence from reported results.

**Local verification: 226 router tests and 29 script tests pass (255 total).** The baseline had 201 router tests with one failure and 27 passing script tests. Twenty-seven new behavioral tests cover the audit findings; existing assertions were updated only where the contract intentionally changed (owned core adapter, version-3 bodies, explicit cache ownership and consolidated mode policy). Obsolete test expectations were not restored by reintroducing duplicated instructions.

A separate invocation through the new persistent runtime executed **35 JIT regression tests**, observed exit zero, and verified the selected source fingerprint was unchanged. The receipt explicitly says `evidence_source: command`; it is not a manually asserted PASS. Both full suites, compiler checks, shell syntax and `git diff --check` were run locally. Native host/model evaluations were **not run**; Python processes are not independent LLMs.

## What changed

| Findings | Repair | Regression evidence |
|---|---|---|
| J01, J11 | Worker schema 3 materializes exact skill and local reference bodies with hashes/bytes. Missing/tampered bodies and unread material references block spawn validation. | `router/test_jit_adversarial.py`, `router/test_jit_integration.py`, updated worker tests |
| J02 | Manifest availability never automatically selects skills, even through the old compatibility flag. | Explicit empty selection stays empty |
| J03 | Every applicable ancestor's project instructions are delivered in order. | Intermediate directory sentinel reaches worker |
| J04, J05 | Check symlinks before resolving; require managed cache ownership, file hashes and canonical-source freshness. Intentional project-native overrides remain supported. | Root/dangling symlinks, traversal, unowned/tampered/stale cache, real profile install/read |
| J06 | Bound argv/cwd process execution, exit/timeout/output observation, evidence classes and optional source fingerprints. Reported evidence cannot satisfy command contracts. | Actual zero/nonzero/timeout; source changes; graph evidence-class rejection |
| J07 | Upstream refresh retains all copied packages, protects the owned meta adapter, validates shared-reference targets, requires a clean worktree and records declared name normalization. | Complete offline update against fourteen mocked upstream repositories |
| J08 | One mode/risk owner (`task-router`), smaller core and owned integration adapter. Scope and risk override irrelevant upstream lifecycle ceremony. | Core budget and policy tests; original candidate-attack gate preserved |
| J09 | Fix two YAML descriptions; make missing retained capabilities discoverable; absorb PR53 rather than recreate local SEO. | All current 74 packages have valid YAML/name/description and pack/core discovery; all-profile matches packages |
| J10, J13 | Separate availability, selection, delivery, retained context and actual isolation; optional task/stage receipts cannot claim compliance or erasure. | Receipt fields and separate-process sentinel isolation |
| J12 | Exact `repo:`, `project:` and `skill:` resource roots; private CLI instructions taught in the core. | Read resource contents and reject missing/traversing locators |
| J14 | Optional precompact hook no longer executes a headless model or rewrites native memory. | Fake model binary is never invoked; user memory remains unchanged |
| J15 | Preserve specialist depth but distinguish alternative design/editorial workflows from complementary implementation/research stages. Upstream registry no longer overwrites the owned core adapter. | Per-skill disposition table, registry and offline refresh checks |
| J16 | Capability envelopes describe requested grants; only the actual host enforces permissions. Independent review cannot be inferred from a role label or constructed payload. | Documentation and explicit unobserved host evaluation manifest |

The new `local-model-routing` guidance also removes claims of an automatic parent/worker/critic assignment that the implemented preference CLI does not provide.

## All skills and context cost

All 75 baseline packages are recorded in `jit-skills-baseline.json` and receive an individual disposition in `jit-skill-dispositions-2026-09-18.md`. PR53 folds the redundant local SEO package into the existing marketing skill, leaving 74, not a wholesale deletion of specialist knowledge.

The three core bodies fell from **41,481 to 15,284 UTF-8 bytes**, a reduction of approximately **63.2%**. `AGENTS.md` fell from 12,786 to 4,181 bytes. These are measured byte counts, not token counts, latency measurements or quality scores. Large canonical design/reference bodies remain large when explicitly selected; they are not silently truncated.

Design taste alternatives, editorial passes, product speculation, artifact review, testing, release gates and executive functions are kept distinct. There is no requirement to load every related skill, no implicit committee, and no universal twelve-skill ceiling. Code enforces explicit material delivery, not semantic relevance.

## Run sequence

1. Freeze baseline `bf880fd7e04cb541eff48527ad9b54bf4bf0270c`, capture source and original test failure in Actions run `35371883907` / artifact `10558103335`.
2. Inventory all 75 packages and reproduce broken worker bodies, manifest inheritance, missed ancestor rules, unsafe cache precedence and untyped self-report receipts.
3. Freeze the sixteen findings and repair acceptance criteria in `jit-adversarial-audit-2026-09-18.md`.
4. Add adversarial tests and observe the red run before implementing the loader/worker/evidence fixes.
5. Implement against that finding list; integrate the exact pending PR53 source and avoid a conflicting second SEO consolidation.
6. Run fresh CLI processes, the complete offline updater, both full test suites, and an actual command-bound runtime acceptance loop on the changed source.
7. Publish branch changes for review. Main and the user's installed machine are not silently updated.

## Reproduction

```sh
python3 -m pip install PyYAML
python3 -m unittest discover -s router -p 'test_*.py' -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 reports/reproduce_jit_baseline.py --repo /path/to/checkout --output /tmp/jit-probes
```

Run the probe script against a separate baseline checkout to reproduce old behavior. Its fixture writes are temporary, and its outputs go only to the explicit output directory. A reported manual PASS remains possible by design; the correction is provenance plus a command-evidence requirement, not pretending human observations are executable tests.

Portable CI additionally tests bootstrap, installed skill/resource/worker commands, observed verifier execution and rollback on Linux/macOS. A CI result must be attributed to its actual commit; do not substitute these local results for an unobserved remote job.

## Limits and remaining acceptance boundaries

- **Native model behavior:** actual Claude/Codex/other host selection accuracy, instruction following, latency, cost and output quality require observed host runs. `evals/jit-host-cases.json` remains `not_run_on_native_models`, with eight concrete scenarios and required trace fields.
- **Isolation:** a new Python process proves separation of generated payloads, not host context erasure or an independent model review. Same-session skill text may persist after logical deselection.
- **Trust:** receipts are integrity-checked JSON, not signed attestations; capability envelopes are not an OS sandbox. The host must authorize commands and enforce real permissions.
- **Source scope:** source-bound checks cover the declared files, not every dependency or remote system. Detached graph receipts do not independently rescan source; check the current loop and run a final integration verifier.
- **Upstream content:** all package integration/metadata surfaces were checked, not every external factual claim. Three Hallmark links outside the vendored package remain absent locally, though their upstream repository exists. Do not invent or silently substitute their contents. Re-check domain-specific/platform facts when they become material.
- **Rollout:** the branch depends on the pending SEO consolidation in PR53. Review/merge and a reviewed bootstrap/profile refresh are required before installed copies change. Old name-only worker payloads must be rebuilt, not relabelled. Modified user cache files must not be deleted merely to pass freshness checks.

This is a repaired and regression-tested delivery/verification layer. It is not a claim that every future model will select perfectly or that all specialist knowledge is permanently correct.
