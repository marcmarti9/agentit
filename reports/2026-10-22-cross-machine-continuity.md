# Cross-machine continuity — 2026-10-22

## Result and architecture

Agentit now separates code delivery through Git, optional private STATE.md
synchronization, and explicit verified handoff of state plus selected evidence.
No new service, background process, account, or automatic context replication is
required. Hosts may use different directories and agent providers.

The receiving host checks project identity, exact committed HEAD, clean code,
three core bodies, explicitly selected skills, recorded profile membership and
every transferred file before writing state. Identical skill bytes remain
compatible across harness and managed private-cache locations. Project-owned
skills can also be verified. Previous selections remain historical evidence;
the new agent makes a fresh task decision and selects skills just in time.

## Commands and recovery

1. Update the private `.agentit/STATE.md` with real decisions and next actions.
2. Commit and publish code using the project's authorized Git workflow.
3. Preview `agentit continuity handoff --project . --output PATH`, adding
   explicit `--profile`, `--skill` and `--artifact` selections as needed.
4. Repeat with `--apply`, then transfer the private directory through an
   authorized private channel.
5. Obtain the exact code commit and required Agentit bodies on the receiver.
6. Run `agentit continuity inspect PATH --project .`, then
   `agentit continuity resume PATH --project . --apply` when ready.

A differing local state blocks replacement unless explicitly selected with
`--replace-state`; the displaced state is backed up. Evidence is retained under
private `.agentit/received/`, including the exact original manifest, rather than
written over project source. Repeated imports check actual retained bytes.
Wrong commits, changed skills, malformed packages, unsafe paths and concurrent
state edits block restoration without overwriting the existing state.

Ordinary continuity status now distinguishes structural state completeness from
cross-machine verification. The latter requires inspecting the actual package
on the receiving host.

## Private Git transport

The existing command-triggered state synchronization remains opt-in and exports
only STATE.md to a caller-verified separate private repository. Link, unlink and
sync share a project lock. Failed initial links remain disabled. Divergence
preserves both versions. Unlinked status does not create a state directory.

The transport rejects aliases of the project origin, disables hooks and
filesystem monitors, avoids remote working-tree checkout and writes state
without clean/smudge filters. Unrelated remote tree entries remain preserved.
An independent review reproduced a Git push-rewrite escape using temporary
repositories; the final verification includes regression coverage for that
destination boundary.
All effective push destinations must match the validated separate fetch
destination. The original reproduction now stops before state export and leaves
both remote histories and local state intact; the independent reviewer confirmed
the repair.

## Verification scope

Focused tests exercise real Git repositories, clones at different roots, CLI
subprocesses, preview/apply, idempotence, metadata retention, backups, drift,
integrity, path/privacy limits, transport hooks/filters and conflict handling.
Final command-bound verification and installation/CI results are recorded in
the completion evidence for this branch.

Observed local acceptance: **352 runtime tests and 74 script tests passed**,
along with generated profile/core freshness, canonical/ECC integrity, shell
syntax, compilation and whitespace checks. The verifier bound unchanged source
fingerprints. Two real subprocess CLI exchange tests also passed against the
installed runtime. All-provider bootstrap applied 10 files with backups, then
reported **5,568 keep operations and no changes**, preserving two unmanaged
private documents. CI also exercises the installed handoff flow in its Ubuntu
and macOS bootstrap jobs; remote results belong to the exact PR head.

No real private remote or second physical PC was configured. These are local
integration tests and CI evidence, not certification of a user's remote access
or physical machines. Preparing a package records a commit; it cannot establish
that the commit has been published or is available on another computer.

## Limits

The package accepts at most 32 explicit evidence files, 1 MiB per file and 8 MiB
total. Secret-marker checks are heuristic; the caller must review selected
material. Hashes detect corruption and incompatibility, not authenticity against
a malicious producer. Credentials, provider settings, tool grants, unsaved chat,
live processes and databases are not transferred. Incoming text is untrusted
data and cannot authorize actions or activate skills.

See [the operational contract](../docs/PROJECT_CONTINUITY.md) for exact behavior.
