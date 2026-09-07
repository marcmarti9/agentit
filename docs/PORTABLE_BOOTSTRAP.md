# Portable bootstrap and recovery

`bootstrap.py` delegates to `router/bootstrap.py`. It supports GNU/Linux and
macOS with Python 3.10 or newer. The manifest defines runtime files, the three
global core skills, provider discovery paths and optional settings templates.

## Plan, apply and update

From a reviewed checkout, run:

```bash
python3 bootstrap.py --provider codex --home /path/to/existing/home
python3 bootstrap.py --provider codex --home /path/to/existing/home --apply
```

Use `--provider all` to target every configured provider. `--home` defaults to
the current user's home; temporary homes are required for installation tests.
An update uses the same commands from the newly reviewed checkout.

Planning does not create files. Every file operation records the desired hash
and mode and the destination's observed hash and mode. Apply rejects changed
sources or destinations, including permission-only changes. Re-run the plan
after inspecting the disagreement. Do not suppress this check to overwrite
concurrent edits.

The full library goes into `~/.agentit/runtime`. Only the three core skills go
into provider discovery roots; see [JIT skill loading](JIT_SKILL_LOADING.md).
Settings and hooks require explicit flags. Installation creates a private
virtual environment and installs the manifest's Python dependencies without
running vendored skill scripts. `--skip-dependencies` is for offline tests only.

## Durable file transaction

Apply validates the whole file plan, prepares verified backups, then writes a
restricted write-ahead `manifest.json` before replacing any managed file.
Files are atomically replaced and their bytes and permissions checked. The
receipt is finalized only when all file replacements finish.

An interrupted installation keeps `recovery_only` and pending records. A
pending record may still match its original state, or already match its
installed state if interruption happened after atomic replacement. Recovery
accepts those two exact states and refuses any other content or permission
state. Backups must also match their recorded hashes.

Legacy host skill removal has its own durable receipt before deletion. Removal
is limited to exact Agentit copies; modified or unrecognized directories are
preserved. Updating source packages can make a historical copy unrecognizable:
that copy remains for manual inspection rather than being deleted by name.

Private runtime files are tracked separately in
`~/.agentit/runtime-inventory.json`. When an update no longer distributes a
recorded file, bootstrap removes it only if its current hash and mode exactly
match that inventory. Removal has the same verified backup and pending receipt
as replacement, so interruption immediately after deletion is recoverable.
Rollback restores both the retired files and the prior inventory.

For an older installation without an inventory, final successful bootstrap
receipts from the same home can establish per-file ownership. Failed or rolled
back receipts are excluded. Missing receipts do not authorize cleanup by name.
Plans and apply results list retained modified and unmanaged runtime files;
review these explicitly if complete removal of obsolete content matters. The
inventory lives in the user's private Agentit state and is not a security
boundary against a malicious process able to alter that state.

## Rollback

Use the `backup_manifest` path returned by apply. After a failed apply, receipts
are under `~/.agentit/backups/install-*/manifest.json`, or the explicit new
`--backup-dir` directory.

```bash
python3 bootstrap.py --rollback /path/to/manifest.json
python3 bootstrap.py --rollback /path/to/manifest.json --apply
```

Rollback checks every record before beginning and rechecks each file immediately
before restoration or removal. It persists `rollback_in_progress` before its
first mutation. Retrying an interrupted rollback skips exact already-restored
originals and resumes remaining operations. Modified files fail closed; resolve
their changes before retrying. Skill trees are copied into a staging directory,
verified and atomically restored.

The receipt covers managed files and identified legacy skill trees. It does
not restore Python dependency versions, uninstall the virtual environment, or
recursively delete runtime directories. These operations are not a filesystem
lock or protection against a malicious concurrent process; the repeated state
checks protect against observed changes at transaction boundaries.

## Verification

```bash
python3 -m unittest router.test_bootstrap router.test_bootstrap_transactions router.test_runtime_inventory router.test_jit_safety_regressions -v
```

Regression tests inject failures before and after atomic file replacement,
interrupt rollback, alter sources and destinations after planning, exercise
permission-only updates, preserve post-install edits, and restore legacy skill
copies. GitHub CI additionally exercises the installed CLI and rollback on
GNU/Linux and macOS. Provider checks inspect configured installation paths;
they do not launch every provider application or certify its discovery behavior.
