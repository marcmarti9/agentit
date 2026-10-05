# ECC + Agentit: one discovery and delivery system

## Scope and ownership

Agentit retains the complete `affaan-m/ECC` 2.2.3 source at commit
`ef648e01899ba3e8dc6371642deaaf64b4477775` in `vendor/ecc`: all 4,212
source files, including 293 skills, 68 agent definitions, 94 legacy command
shims, rules, hooks, memory, continuous learning, native CLIs, host adapters,
tests, assets and original licenses. Nothing is fetched at skill-activation time.

The unified catalog exposes **380 canonical skills: 96 existing Agentit skills
and 284 ECC skills**. Nine overlapping/deprecated ECC skill names resolve to one
canonical procedure. Source retention is not duplicate activation: the original
nine remain inside the pinned tree so upstream commands, links, tests and
attribution keep working, but they are not installed/discovered as extra
Agentit procedures. The explicit decisions and reasons live in
`references/ecc-policy.json`; `agentit ecc resolve NAME` displays the winner.

This is a full source integration with a unified skill runtime, **not a claim
that every native ECC service has been installed, enabled or tested on every
host**. No hosted ECC Pro service or subscription is included by copying the
open-source repository. No host, cloud account or model-provider configuration
is changed by importing or discovering it.

## Canonical responsibilities

| Responsibility | Single owner / integration |
| --- | --- |
| Global entry, routing, execution mode | Agentit's existing three core skills and model-owned task decision. |
| Skills, profiles and metadata packs | Existing Agentit discovery and exact-byte JIT delivery; nine additional ECC domain packs. |
| Worker context, tool grants and evidence | Existing schema-3 workers, capability checks and command-bound Loop/Graph runtime. ECC role files are explicit resources, not a second automatic dispatcher. |
| TDD, review cadence and completion | Agentit BUILDER/REVIEW and risk overrides; upstream blanket TDD, 80% coverage or per-stage commits do not override them. |
| Remotion | `remotion-video-engineering`, retaining Agentit's expanded current official resources rather than an overlapping older checklist. |
| Security and Git workflows | `security-and-hardening` and `git-workflow-and-versioning`; language/domain ECC specialists remain complementary. |
| Runtime memory and continuity | Agentit private checkpoints remain authoritative for runs. ECC memory, vaults and project-scoped learning are explicit specialist/native capabilities; they do not start transcript collection or background workers on import. |
| Native ECC tools/hooks/adapters | Retained unchanged under the pin, exposed through `agentit ecc`. Host setup and processes require explicit scoped authorization. |

ECC's `autonomous-loops` points to its successor `continuous-agent-loop`;
`continuous-learning` points to `continuous-learning-v2`. The other aliases and
selection rationale are in the policy, rather than duplicated in every skill.
The choices are compatibility/scope judgments, not a benchmark proving every
selected procedure universally superior. Intentional alternatives such as
framework-specific tests or distinct visual-design directions are retained.

## Discovery, activation and delegation

The commands below are agent-facing mechanics. The user does not need to select
profiles or run them manually. Profiles provide availability, never activation.
Existing domain profiles gain explicit relevant specialists; `ecc` makes all
canonical ECC skills available and `all` includes the whole unified inventory.

```sh
python3 agentit ecc status
python3 agentit skills packs --format json
python3 agentit skills candidates ecc-web --format json
python3 agentit skills activate api-design --project /absolute/project --format json
python3 agentit enable ecc-web --project /absolute/project       # plan only
python3 agentit enable ecc-web --project /absolute/project --apply
python3 agentit ecc resolve tdd-workflow
python3 agentit ecc list --kind agents
python3 agentit skills resource repo:vendor/ecc/agents/architect.md --project /absolute/project
```

`router/ecc.py` resolves explicit IDs and verifies approved source bytes.
`router/profiles.py` and `router/profile_jit_cli.py` reuse that source resolver
and validate the full selected package before private caching. `skill_loader.py`
keeps precedence: project-native override → verified managed private cache →
canonical harness/ECC source. An alias is rejected with a canonical-ID hint;
selection and delivered IDs must still match exactly.

Every ECC body is the **complete original SKILL.md**, not a translated summary
or generated adapter. Supporting resources are delivered separately when needed.
Use `skill:ID/path` for a skill-local file. Upstream paths outside the package
resolve against the declared `upstream_root` using `repo:vendor/ecc/path` or
`agentit ecc read path`. Never infer that a mentioned reference has been read.
These same exact bodies/resources are carried by the existing worker renderer;
an ECC role definition can be passed as an explicit resource to an authorized
worker without creating an invented provider, permission grant or reviewer.

## Native ECC execution

The Python/JIT layer needs no Node packages. The retained native ECC CLI needs
Node.js and its existing dependencies. For a separately authorized native-tools
setup, inspect the retained `package.json`, `yarn.lock`, dependency source and
install-script policy first. The canonical package manager is pinned in
`package.json`; do not upgrade it to an unspecified latest version.

```sh
cd vendor/ecc
corepack yarn install --immutable --mode=skip-build
cd ../..
python3 agentit ecc run -- --help
# Only after choosing a native operation and approving its host-state effects:
python3 agentit ecc run --allow-host-changes -- <native-command> <arguments>
```

The flag acknowledges a boundary; it is not an OS sandbox or automatic user
permission. The wrapper never installs packages, launches daemons or registers
hooks merely because the catalog exists. It preserves the caller's current
working directory and original ECC argument vector. It verifies the retained
source before native execution, requires already-installed dependencies, and
blocks native `auto-update`, which would invalidate the pinned source. Dependency
bytes themselves are not authenticated by the source manifest.

Do not install ECC's entire global plugin/rules surface on top of Agentit's
three-core-skill setup: that would create the competing lifecycles this merge
removes. For a specific native adapter/hook, inspect its actual changes and
register only the selected non-conflicting capability. Native ECC setup still
has upstream host-specific limitations; retained files are not evidence of
feature parity across Codex, Claude, Cursor or other hosts.

## Provenance, updates and rollback

`vendor/ecc.lock.json` records the approved revision, file SHA-256, byte lengths,
executable bits, resource inventory and canonical skill metadata. Hashes detect
changes relative to this reviewed manifest; they are not signatures and do not
protect against an attacker rewriting the manifest and policy together.
The root Apache-2.0 license is unchanged. ECC's MIT license and its original
notices/licenses remain in the retained source; see `THIRD_PARTY_NOTICES.md`.

The importer is offline and never executes upstream code:

```sh
python3 scripts/ecc_integrate.py --source /path/to/clean-pinned-ECC-checkout
python3 scripts/ecc_integrate.py
python3 agentit ecc verify
python3 scripts/check_skill_curation.py
```

A checkout must be clean and at the policy's exact revision. For an independently
obtained offline archive, `--source-revision SHA` records reported provenance;
it does **not** prove the archive originated at that Git commit. CI imports from
the actual pinned Git checkout. Re-importing the same content is idempotent.
Mismatched pins, unreviewed skill collisions, stale/tampered sources, unsafe
paths and symlinks fail closed. Existing vendor content is not silently replaced.

An upstream update requires a work branch, comparison of upstream changes,
explicit reconciliation of policy/aliases and the pinned tree, regenerated
catalogs and fresh tests. Keep a clean checkpoint before replacing an old
snapshot; the importer deliberately refuses an automatic version overwrite.
Rollback is reverting the integration commit(s), then running Agentit's normal
managed bootstrap/update. Existing cache sources that no longer exist are
rejected until the corresponding profiles are refreshed. Never delete unowned
host configuration or unrelated project files as part of rollback.

The portable bootstrap includes the source/lock/policy privately but still
exposes only the original three global bodies. `node_modules`, `.git` and `.yarn`
are pruned before traversal; dependency-generated symlinks must not cause them
to be copied into the runtime. Installing native dependencies in the source
checkout does not make them part of future managed runtime updates.

## Verification and failure diagnosis

```sh
python3 -m unittest router.test_ecc -v
python3 -m unittest discover -s router -p 'test_*.py' -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/sync_upstream_skills.py
python3 scripts/check_skill_curation.py
python3 agentit ecc verify
```

The integration tests cover exact delivery of every canonical ECC body, explicit
shared resources in schema-3 worker prompts, aliases, project overrides,
private profile enable/idempotence, cache/source tampering, path traversal and
symlinks, the native execution boundary and bootstrap dependency exclusion.

An integrity failure means stop and inspect the named source/manifest, not
recompute its hash to hide the change. A redundant-ID error means select the
reported canonical skill. A stale-cache error means compare local edits before
refreshing the profile. A missing native-dependencies error does not affect
Python skill activation; install only when native execution is actually needed.
Native tool tests and real host installation are separate evidence from these
Python/inventory checks. CI logs and PR results report the tests actually run;
this document does not assert an independent model review or blanket security.
