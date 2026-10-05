# Native ECC install compatibility and observed baseline

See [ECC_INTEGRATION.md](ECC_INTEGRATION.md) for scope, source pin, commands and host authorization.

## Dependency installation

Use the hash-pinned Yarn version in ECC's `package.json` and `corepack yarn install --immutable --mode=skip-build`, with `YARN_ENABLE_SCRIPTS=false`. The npm compatibility lane rewrote `yarn.lock` in the integration smoke run; do not bless that changed lock by regenerating the source hash manifest.

Yarn also sets executable bits on the package's declared `bin` targets. At the retained revision, `scripts/memory-mcp.mjs` is declared as a binary but is non-executable in Git. Removing that legitimate install-time bit would break the executable that Yarn linked.

The verifier therefore accepts only this narrow class of install-time mode difference: dependencies are present, the source file's bytes/length match its pin, it gains (not loses) the executable bit, and its path is declared in the independently hash-verified upstream `package.json` bin map. Unknown paths, changed source/manifest bytes, symlinks, undeclared executable changes and lost executable permissions still fail. `agentit ecc verify` reports accepted differences in `installed_declared_bin_modes`; the committed source and lock retain the original Git modes.

The native CI gate checks modes with that verifier, then checks unchanged source bytes with Git. It does not launch services, install host hooks or authenticate the dependency graph. Installation on an actual user host remains separate.

## Unmodified upstream native test baseline

GitHub Actions run 37337571776, artifact `ecc-native-baseline-evidence`, recorded **6,195 passed / 6,196 total** on the unmodified pinned ECC source. One test failed: `tests/scripts/codex-hooks.test.js`, “pre-push refuses a tracked interpreter committed under a folded case.”

Its case-insensitive-filesystem guard is `existsSync(__filename.toUpperCase()) || existsSync(__filename.toLowerCase())`. With an all-lowercase checkout path, the lowercase expression is the original existing path, so the platform-specific scenario incorrectly runs on a case-sensitive Linux filesystem. The fixture creates `Python`; the hook searches `python` and does not print the expected tracked-interpreter warning. The assertion that no interpreter was executed passed. This observation is not proof of native macOS hook parity.

The original test remains intact. No test was removed, weakened or silently skipped to present a green baseline. Agentit integration/runtime tests, native CLI smoke, and the full upstream suite are distinct evidence; do not conflate their results.
