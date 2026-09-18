# Fresh integration CI follow-up

The first fresh PR #55 CI run was `35393423786`, reviewing head
`7e43721132415fb7e77c9f92dd52f22e17822842` through GitHub's merge ref
`5238d2eb66860e1a6cca840538111d96538bbbdc`.

The complete test job `105756731233` passed: 272 runtime tests, 42 script tests,
canonical-package integrity and the remaining syntax/catalog checks. Both
portable jobs (`105756731585` Ubuntu and `105756731540` macOS) failed at an obsolete
wording assertion inherited from #45: it looked for `Agentit's own adapter`, but
the deliberately compact owned adapter says `This is an Agentit-owned adapter`.
The clean plan, real dependency install, provider-root inventory and idempotent
update checks passed before that assertion. Later portable steps were skipped;
this run is not evidence of a successful complete installation smoke test.

The corrected check compares the entire installed adapter byte-for-byte to the
owned source and additionally rejects equality with the archived upstream
meta-skill. It no longer equates one English phrase with ownership. No runtime
code, source pins, test counts or existing security assertions were weakened.

An offline local smoke exercised the corrected check, installed CLI, actual skill
and resource bodies, schema-3 worker delivery, executed command evidence and
repeatable rollback. That local smoke used `--skip-dependencies` plus the already
available local PyYAML; it is not a substitute for the fresh Ubuntu/macOS CI jobs,
which retain real dependency installation. The portable smoke verifies command
execution; source fingerprint binding and stale-evidence rejection are exercised
by the runtime regression suite, not by its unbound `print(42)` smoke verifier.

The merge gate remains a fresh complete CI run on the corrected published head.
Its exact head, run IDs and conclusions will be recorded in the PR conversation
before merging. Historical red runs remain part of the diagnostic record.
