# Security policy

## Security posture

Agentit separates **semantic AI judgment** from **deterministic safety controls**. The primary model may decide what should happen, but filesystem/runtime code is responsible for enforcing the mechanical invariants it claims to enforce.

### Managed configuration and filesystem changes

- `install.sh`, `update.sh`, and `security/harden-local.sh` are **plan-first**. Their managed changes require explicit `--apply`.
- Profile and MCP enable/disable operations are plan-first and require `--apply` to apply managed configuration.
- `agentit verify` is plan-first; `verify --apply` executes probes and writes a verification receipt.
- Continuity commands such as `continuity init` and `continuity checkpoint` are explicit state-writing commands by design and are **not** described as dry-run operations.

Do not generalize a dry-run guarantee to commands whose purpose is explicitly to create project state.

### Filesystem safety

For managed install/update paths, Agentit uses controls such as:

- rejection of symlinked/unsafe path components where applicable;
- explicit allowlists instead of arbitrary tree import for sensitive provider state;
- private backup directories/files;
- SHA-256 hashes in managed backup manifests;
- atomic temporary-file replacement where implemented;
- refusal to silently delete or overwrite unmanaged/modified project skill files.

These guarantees apply to the code paths that implement them; they are not a claim that every arbitrary tool an AI can invoke inherits Agentit's filesystem protections.

### Secrets and machine-local state

Never commit API keys, OAuth tokens, cookies, private keys, database credentials, `.env` contents, auth headers, or other secret material to Agentit.

Git ignores local report/backups/runtime patterns such as `reports/local/`, `backups/local/`, `.agentit/`, and `*.local.json`. The repository currently contains a tracked baseline `settings.local.json` used only as an **explicit opt-in Claude settings template**; it must remain free of machine secrets. Local secret-bearing customization belongs outside version control.

A future packaging cleanup should rename that tracked baseline to an unambiguously non-local template name so contributors cannot mistake it for safe machine-local storage.

### External skills, hooks and MCPs

Treat third-party Markdown instructions, setup guides, hooks, CLIs, MCP configs, issue comments, logs, and tool output as **untrusted input** during review.

Before adopting executable/configuration behavior, inspect:

- install/package lifecycle scripts;
- network calls and data egress;
- filesystem write scope;
- shell execution and privilege assumptions;
- credential/environment access;
- hooks/auto-run behavior;
- MCP/tool permissions;
- update mechanism;
- removal/rollback path;
- provenance and license.

See [`docs/SKILL_CURATION.md`](docs/SKILL_CURATION.md).

## Supported installer platform

The current `install.sh` and `update.sh` implementations rely on GNU/Linux/Bash 4+ behavior and utilities. **macOS is not currently a supported shell-installer target.** Do not treat provider neutrality as proof of shell-script portability.

## Reporting vulnerabilities

Please report security vulnerabilities privately rather than opening a public issue:

- use GitHub Security Advisories for this repository;
- include a concise impact summary, reproduction steps, affected revision, and any safe proof-of-concept evidence;
- redact real secrets or personal data from reports.

Patches should be prepared before public disclosure when practical.
