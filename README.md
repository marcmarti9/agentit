# Agentit

[![CI](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**Provider-neutral workflows and a small execution runtime for coding agents.**

Agentit helps an agent select relevant expertise, carry bounded context into
workers, track verifiable work, and leave useful project documentation. The
active model makes semantic decisions. Python handles explicit IDs, files,
permissions, state and evidence.

Use it with an agent that can read skills, inspect your project and run the
required tools. The user can work in ordinary language; Agentit's CLI is an
implementation surface for the agent.

## Install or update

Requirements: Python 3.10+, Git, and GNU/Linux or macOS. Applying an installation
creates an isolated virtual environment and installs PyYAML. The plan itself is
read-only.

```bash
git clone https://github.com/marcmarti9/agentit.git
cd agentit
python3 bootstrap.py --provider codex
python3 bootstrap.py --provider codex --apply
```

Choose `claude`, `codex`, `grok`, `gemini`, `antigravity`, or `all`. Review the
plan before applying it. The generated CLI is available at
`~/.local/bin/agentit`; it does not need to be on the user's PATH.

To update a clean checkout, fetch and fast-forward its reviewed branch, then
run the same plan/apply commands. Preserve local modifications before changing
Git state. General settings and hooks require explicit opt-in flags.

For installation tests, pass `--home /path/to/existing/temporary/home`. Apply
returns a backup manifest that can also recover an interrupted installation:

```bash
python3 bootstrap.py --rollback /path/to/manifest.json
python3 bootstrap.py --rollback /path/to/manifest.json --apply
```

See [bootstrap and recovery](docs/PORTABLE_BOOTSTRAP.md) for transaction limits,
concurrent-edit protection and retryable rollback. Legacy shell install/update
entrypoints remain for compatibility; the Python bootstrap is canonical.

## A small core, selected expertise

A fresh installation publishes exactly three Agentit skill IDs to each selected
provider's discovery directory:

- `using-agentit`: dispatch, execution modes, shared quality and completion rules;
- `task-router`: the model's current task decision and review contract;
- `using-agent-skills`: Agentit's own navigation and source-authority adapter.

The complete library stays under `~/.agentit/runtime/skills`. Project profiles
use `.agentit/profile-skills`, outside provider skill discovery. Existing
unrelated or modified host skills remain the user's configuration.

```text
current request → bare or Agentit → current task decision
  → selected skills, references and tools
  → implementation and proportionate independent review
  → fresh verification and durable project documentation
```

The core distinguishes FAST localized edits, NORMAL functional changes and DEEP
audits or high-risk work. Small edits get targeted verification. Architectural
or consequential changes justify stronger review and broader checks.

A profile makes skills available. A pack exposes bounded discovery metadata.
Reading a selected body consumes context. Removing its selection cannot erase
text already read by the model, and each new session makes fresh selections.

```bash
agentit skills packs
agentit skills candidates engineering
agentit skills show debugging-and-error-recovery --project .
```

These commands expose pack metadata, then candidates, then only the requested
bodies. Prompt and JSON output include an explicit authority boundary. A source
skill cannot activate another skill, force its entire lifecycle, or authorize
scripts, downloads, external actions or provider changes by saying “always.”
Host instructions, user authorization and the current task govern execution.

See [JIT loading and host isolation](docs/JIT_SKILL_LOADING.md).

## What is included

| Capability | Purpose and contract |
| --- | --- |
| Task decisions and review | Select relevant expertise, identify uncertainty and challenge consequential choices. [Decision protocol](docs/LLM_NATIVE_DECISION_PROTOCOL.md) |
| Engineering, design and product skills | Implementation, debugging, interfaces, visual design, accessibility and requirements. [Pack map](references/agentit-skill-packs.md) |
| Writing and source research | Preserve claims and voice, inspect current authoritative evidence when needed. [Reference Intelligence](docs/REFERENCE_INTELLIGENCE.md) |
| Executive and growth profiles | Discover strategy, finance, operations, marketing and related expertise only when relevant. [Executive profile](docs/EXECUTIVE_PROFILE.md) |
| Worker context | Project constraints, selected skills, allowed paths and capabilities, expected output and verifier. [Runtime contract](docs/RUNTIME_ENGINEERING.md) |
| App security gate | An opt-in adversarial retest before a consequential release. [Security gate](skills/app-security-gate/SKILL.md) |
| Loop and Graph runtime | Observable goals, bounded retries, dependency and write ownership, receipts backed by fresh evidence. [Runtime engineering](docs/RUNTIME_ENGINEERING.md) |
| MCP and capabilities | Resolve explicitly selected capabilities and keep task-owned tool changes bounded. [Capabilities](docs/CAPABILITIES.md), [MCP catalog](docs/MCP_CATALOG.md) |
| Continuity and documentation | Private operational state plus durable component and architecture knowledge. [Continuity](docs/PROJECT_CONTINUITY.md), [documentation contract](docs/DOCUMENTATION_CONTRACT.md) |

Client-facing work also inherits two compact rules from the installed core:
use truthful product evidence and intentional design choices; give clients a
safe way to manage routine mutable business content when the operating model
requires it. These rules do not require a CMS for a genuinely static site.

## Upstream content and maintenance

Agentit-owned code, adapters and compositions are separate in authority and
provenance from canonical third-party packages. Public skill IDs remain stable.
Canonical task packages stay in `skills/<id>`, identified by the lock registry;
the raw upstream meta-workflow is kept under `vendor/agent-skills`, separate from
Agentit's global adapter. Original licenses and notices live in `vendor/licenses`.

[The source registry](skills/UPSTREAM_SOURCES.md) records pinned source commits.
[The lock](skills/UPSTREAM_LOCK.json) records every canonical package file's
SHA-256 and mode, shared references and exact license/NOTICE copies. Repository-root
packages explicitly record which package entries are included.

```bash
# Offline check; changes nothing.
python3 scripts/sync_upstream_skills.py

# Inspect a refresh plan.
python3 scripts/sync_upstream_skills.py --refresh
```

Save the plan's `source_commits` object to a JSON file, review those revisions,
then apply that exact cached selection:

```bash
python3 scripts/sync_upstream_skills.py --refresh --heads-file /path/to/reviewed-commits.json --offline --apply
```

Refresh reads pinned source archives, refuses local edits and unowned collisions,
and preserves complete selected packages. It does not execute upstream scripts,
install upstream dependencies or modify provider configuration. Optional tools
inside a package may require separate downloads or services when deliberately
selected; for example, current Impeccable uses a versioned binary launcher.

See [upstream maintenance](docs/UPSTREAM_MAINTENANCE.md) and
[third-party notices](THIRD_PARTY_NOTICES.md). Agentit's original material is
Apache-2.0; third-party material retains its own license.

## Verification and limits

```bash
python3 -m unittest discover -s router -p 'test_*.py' -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/sync_upstream_skills.py
bash -n install.sh update.sh security/harden-local.sh scripts/sync-upstream-design-skills.sh
python3 -m py_compile agentit bootstrap.py router/entrypoint.py router/bootstrap.py
git diff --check
```

CI verifies mechanical runtime contracts and portable bootstrap behavior on
GNU/Linux and macOS. Tests can prove that selected bodies and authority rules
are transported; they cannot prove that every model will follow them.

Agentit has not established universal improvements in model quality, speed,
cost or token usage. Paired agent evaluations are tracked in
[issue #29](https://github.com/marcmarti9/agentit/issues/29) and the
[evaluation plan](evals/evaluation-plan.md).

Repository changes normally end in a reviewed PR. Publishing a branch, merging
and deploying remain distinct actions governed by the user's actual authority.
Contributions follow [CONTRIBUTING.md](CONTRIBUTING.md).
