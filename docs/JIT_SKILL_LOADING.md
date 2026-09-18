# JIT skill loading, delivery and host boundaries

## What JIT means here

Agentit separates **availability → discovery → explicit selection → delivered bytes → host retention → observed outcome**. These are different states. A profile is not an active task, a skill ID is not its body, a digest does not prove a model followed instructions, and a new selection does not erase an existing conversation.

The primary model makes semantic decisions. Code resolves explicit IDs, reads selected material and checks structural contracts. There is no keyword classifier, fixed skill quota or automatic full-pack activation.

The canonical execution-depth/risk policy lives in `skills/task-router/SKILL.md`. `using-agentit` is the entry protocol; `using-agent-skills` is the **Agentit-owned** integration adapter. The latter is no longer overwritten by the Addy upstream refresh. Upstream specialist procedures cannot override host safety, user/project constraints, granted tools or that scoped mode policy.

## Installation and discovery

Bootstrap exposes only `using-agentit`, `task-router` and `using-agent-skills` in Agentit-managed host discovery roots. User-owned unrelated skills are preserved; this is not a claim that the entire host sees only three skills.

| Provider adapter | Agentit discovery root |
|---|---|
| Claude Code | `~/.claude/skills` |
| Codex | `~/.agents/skills` |
| Grok Build | `~/.grok/skills` |
| Gemini CLI | `~/.gemini/skills` |
| Antigravity | `~/.gemini/config/skills` |

These are bootstrap adapter paths, not proof of behavior in every future provider version. The full library remains in `~/.agentit/runtime/skills`, outside those discovery roots. Project profiles install packages into `<project>/.agentit/profile-skills` rather than advertising them in `.agents/skills`.

```sh
agentit skills packs --format json
agentit skills candidates engineering backend --format json
agentit skills show debugging-and-error-recovery --project /absolute/project
```

The first two commands expose metadata only. `show` returns exactly the selected bodies. The caller, not a profile or stale manifest, determines selection.

## Source precedence and integrity

1. Intentional project-native `.agents/skills/<id>/SKILL.md`.
2. Managed private `.agentit/profile-skills/<id>/SKILL.md`.
3. The installed harness library.

Paths are checked before symlinks are resolved. Root/resource symlinks, parent traversal, missing/empty selected files and malformed identifiers fail closed. This conservative loader policy is Agentit's own boundary; it does not assert that native hosts universally prohibit symlinks.

Private cache reads require schema-1 installation ownership, the exact managed destination and an installed file hash. Where the canonical source is present, its hash must still match the manifest. Modified, unowned or stale cache files produce an actionable error instead of silently overriding the harness. Refresh through the existing profile plan/apply workflow; do not delete a user's edits to manufacture freshness. A hash is an integrity check, not a signature, sandbox or protection from an attacker controlling the process and manifest together.

Shared references from upstream packages remain copied to `.agentit/references` by the profile installer. Prefer explicit resource locators to ambiguous working-directory assumptions:

```sh
agentit skills resource repo:references/definition-of-done.md
agentit skills resource skill:marketing-and-growth/references/local-seo.md
agentit skills resource project:docs/architecture.md --project /absolute/project
```

The resource loader reads UTF-8 data; it does not execute scripts, expand a library, make network calls or grant new instructions. External URLs require the host's authorized browser/connector. Preserve a relevant inspected excerpt in a project artifact before binding it into a worker.

## Delivery receipts and stage transitions

```sh
agentit skills show debugging-and-error-recovery \
  --project /absolute/project --task-id issue-123 --stage diagnosis \
  --context-origin same-session --receipt --format json
```

A receipt records resource IDs, roots, hashes, byte counts, timestamp and explicit task/stage. UUID files under `.agentit/context` avoid overwriting earlier receipts. They are private operational state, not committed project knowledge. They explicitly set `proves_model_compliance: false` and `proves_context_erasure: false`.

Re-select at a stage boundary. In an existing host conversation, previous bodies may remain in context. For a genuinely fresh context use a real new host session or isolated worker, when available. After compaction inspect the host's retained material. Do not call a mental reset, a new receipt or an MCP disable operation context erasure.

## Worker contract version 3

`agentit worker build` materializes selected skill bodies and local reference bodies. Its payload records source roots, digests, byte counts, unresolved reference locators and delivery metadata. Applicable project instructions are read from the root through **every ancestor** of the bounded work directory, in increasing specificity.

Spawn validation rejects absent/tampered selected bodies, unread material references, unknown/unavailable capabilities and the existing full-catalog-dump condition. No hidden twelve-skill limit remains; a caller can explicitly set a justified budget through the Python API. Older name-only worker payloads must be rebuilt rather than relabelled version 3.

The caller must pass the actual rendered prompt to the actual worker. JSON construction is not a worker invocation. Capability envelopes and read-only reviewer instructions describe requested restrictions; only the real host/provider/OS can enforce them. The runtime does not claim an independent reviewer or sandbox has run.

## Verification and maintenance

Command-bound evidence, self-reported evidence and source freshness are documented in [RUNTIME_ENGINEERING.md](RUNTIME_ENGINEERING.md). Tests cannot certify model judgment or instruction obedience.

The optional precompact compatibility hook now consumes input and exits without invoking a model or rewriting native memory. An active authorized agent may maintain private continuity state explicitly. Existing installed copies require a reviewed bootstrap/profile refresh; a repository PR does not update a user's machine.

Upstream refresh requires a clean worktree, retains every copied canonical package, preserves the owned core adapter and records declared metadata aliases. Shared-reference deletion targets are bounded. Refresh still mutates a working tree: use a branch, inspect the diff, run tests and keep rollback available. It is not an all-or-nothing filesystem transaction.

## Reproducible checks and unproven claims

```sh
python3 -m unittest discover -s router -p 'test_*.py' -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The tests cover all package metadata/discovery, actual body/resource projection, separate CLI processes, private-cache drift, ancestor instructions, receipt typing, process exit/timeout/source changes, offline upstream refresh and optional hook safety. Portable CI also exercises installed JIT commands before rollback.

Real-host semantic selection, model compliance, latency and task-quality comparisons remain separate evaluations; see `evals/jit-host-cases.json`. No native host/model run is claimed by a passing Python test. The baseline and finding-to-fix evidence are in `reports/jit-adversarial-audit-2026-09-18.md` and `reports/jit-implementation-2026-09-18.md`.

External references checked 2026-09-18: https://agentskills.io/specification ; https://developers.openai.com/codex/skills/ ; https://code.claude.com/docs/en/skills . They establish platform/spec behavior, not an Agentit certification.
