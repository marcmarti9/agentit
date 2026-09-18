# Loop and Graph runtime: evidence rather than labels

The primary model chooses the goal, permissions, verifier and topology. `router/loop_runtime.py`, `router/graph_runtime.py` and the persistent `agentit runtime` CLI enforce that explicit contract. They do not select skills or interpret natural-language intent.

## Evidence classes

**`reported`** means a caller supplied a result and evidence text. It remains useful for a human review, a visual observation or compatibility with an older integration, but is not proof this runtime executed a command. Legacy receipts without the new provenance field are treated as reported.

**`command`** means `run_verifier` started the contract's exact argument vector with `shell=False` in its bound working directory and observed the process. It records exit status, timeout, start time, duration, output hash/size/excerpt and optional source hashes. A command-evidence contract cannot pass through `loop-attempt --result pass` alone.

Neither class is a cryptographic attestation. A producer that controls the process and rewrites all hashes can forge JSON. Host permissions, command trust and independent review remain separate boundaries. The command runner is **not a sandbox** and must only receive an authorized verifier. Exit zero does not establish that an inadequate test actually checked the user's goal.

## Executable loop

For a real source test, bind the command and affected source paths before running it:

```sh
agentit runtime loop-init \
  --state .agentit/runtime/loops/check.json \
  --project /absolute/project \
  --goal 'Selected regression is fixed' \
  --verifier 'Run the approved test module' \
  --stop 'Process exits zero with unchanged source' \
  --verifier-argv '["python3","-m","unittest","tests.test_feature"]' \
  --subject src --subject tests
agentit runtime loop-run --state .agentit/runtime/loops/check.json --timeout 120
agentit runtime loop-check --state .agentit/runtime/loops/check.json \
  --require-command --receipt .agentit/runtime/receipts/check.json
```

Use exact argument vectors, not interpolated shell snippets. State initialization refuses an existing file; create a fresh loop for a materially new contract. State paths reject symlinks. Writes use temporary files and atomic replacement, but concurrent writers still require external single-writer ownership; there is no distributed lock or hostile-filesystem race guarantee.

The default budget is two attempts, with a finite maximum. A failed attempt may retry with fresh evidence or a changed strategy. Exhaustion escalates rather than weakening the verifier. `loop-run` returns nonzero on failure. Timeouts kill the process group on POSIX; other hosts require their own descendant-process controls.

Output is spooled to a temporary file, hashed fully and excerpted to 64 KiB in the receipt. This bounds receipt size, not disk output; the host must impose resource limits for untrusted commands. Secrets printed by a verifier can appear in private state, so choose commands and retention appropriately and never commit raw private state.

## Source freshness

`--subject` names explicit project-relative files/directories. Symlinked/missing subjects are rejected. Source fingerprints exclude `.git`, `.agentit` and `__pycache__`. A verifier changing its own selected subject cannot pass merely by returning zero. `loop-check` rejects a successful receipt whose selected source changed afterward; start a new loop.

Without `--subject`, the receipt proves command observation only, not a source snapshot. Source hashes cover the selected files, not dependencies, remote services, model behavior or the entire machine. A directory scan does not prove immunity to an adversary changing files and restoring them during execution.

## Reported evidence

Manual or externally observed checks use an explicitly reported contract:

```sh
agentit runtime loop-init --state .agentit/runtime/loops/visual.json \
  --goal 'Review approved layout' --verifier 'Human inspection' --stop 'Reviewer records result'
agentit runtime loop-attempt --state .agentit/runtime/loops/visual.json \
  --result pass --strategy 'Human review' --evidence 'Reviewer and inspected artifact reference'
```

The resulting receipt says `evidence_source: reported`. It cannot satisfy `--require-command` or a graph node that requires command evidence. Do not present it as executed verification.

## Graph integration

Each node declares dependencies, read/write ownership, expected artifacts and a loop contract. `graph-init --spec ... --state ...` can bind `loop_state` paths to their contract hashes and evidence requirements. A manually supplied node may explicitly request `evidence_requirement: command` or `reported`.

Only `graph-ready` nodes may advance. `graph-complete --node ... --loop-receipt ...` requires a passing receipt from that node's exact contract, the correct evidence class and required handoff artifacts. `graph-check` accepts only a completed graph. Cycles, unknown dependencies, conflicting write ownership, receipt reuse and missing artifacts remain rejected.

A graph checks submitted evidence structure and provenance class. It does not re-execute commands or rehash the source through a detached receipt. Run `loop-check` against the current subject immediately before handoff, and perform a final integration verifier after upstream artifacts change. Graph receipts must not be called universal freshness or sandbox guarantees.

## Tests and migration

Old name-only worker context is rebuilt at schema 3. Existing reported loop/graph records remain inspectable; explicitly opt into command contracts for new executable work. Never silently relabel old evidence as observed.

```sh
python3 -m unittest discover -s router -p 'test_loop_runtime.py' -v
python3 -m unittest discover -s router -p 'test_graph_runtime.py' -v
python3 -m unittest discover -s router -p 'test_jit_*.py' -v
```

The CLI is agent-facing. Users should not need to orchestrate loops by hand. A real independent model review and actual host permission enforcement must be separately observed and reported honestly.

## Source fingerprint version 2

Command-bound subject fingerprints include each selected file's kind, permission
mode and SHA-256, plus selected directories (including empty directories) and their
modes. Symlinks and special files such as FIFOs are rejected, not silently omitted.
`.git`, `.agentit` and `__pycache__` remain excluded from subject enumeration. The
execution record reports `subject_fingerprint_version: 2` when subjects are bound.
A chmod or directory-shape change after PASS now makes the result stale. Pre-v2
source-bound evidence must be rerun before a current-source handoff; unchanged
legacy report-only evidence is not relabelled as command-verified. These are
before/after observations, not a filesystem snapshot lock or signed attestation.
