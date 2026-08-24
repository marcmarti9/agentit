# Security policy

## Security posture

Agentit separates **semantic AI judgment** from **deterministic safety controls**. The primary model may decide what should happen, but filesystem/runtime code is responsible for enforcing the mechanical invariants it claims to enforce.

### Managed configuration and filesystem changes

- The canonical `bootstrap.py` / `agentit bootstrap` flow is **plan-first** and requires explicit `--apply` for installation changes.
- Legacy `install.sh`, `update.sh`, and `security/harden-local.sh` remain plan-first for their managed changes.
- Profile and MCP enable/disable operations are plan-first and require `--apply` to apply managed configuration.
- `agentit verify` is plan-first; `verify --apply` executes probes and writes a verification receipt.
- Continuity commands such as `continuity init` and `continuity checkpoint` are explicit state-writing commands by design and are **not** described as dry-run operations.

Do not generalize a dry-run guarantee to commands whose purpose is explicitly to create project state.

### Portable bootstrap safety

The canonical portable bootstrap uses Python standard-library filesystem primitives rather than GNU-specific shell utilities. Its managed file operations include:

- rejection of symlinked path components in source and destination trees;
- provider/runtime allowlists from `bootstrap-manifest.json`;
- a private Agentit runtime under `~/.agentit/runtime`;
- a private virtual environment under `~/.agentit/venv` for runtime Python dependencies;
- SHA-256 verification before and after managed copies;
- per-file backups for pre-existing destinations;
- atomic temporary-file replacement;
- a bootstrap receipt containing installed hashes and rollback metadata;
- fail-closed rollback when an installed destination was modified after installation.

The bootstrap intentionally does **not** recursively delete the private runtime/venv during rollback. It restores/removes only files proven by the receipt to be safe to change.

### Filesystem safety

For other managed install/update paths, Agentit uses controls such as:

- rejection of symlinked/unsafe path components where applicable;
- explicit allowlists instead of arbitrary tree import for sensitive provider state;
- private backup directories/files;
- SHA-256 hashes in managed backup manifests;
- atomic temporary-file replacement where implemented;
- refusal to silently delete or overwrite unmanaged/modified project skill files.

These guarantees apply to the code paths that implement them; they are not a claim that every arbitrary tool an AI can invoke inherits Agentit's filesystem protections.

### Secrets and machine-local state

Never commit API keys, OAuth tokens, cookies, private keys, database credentials, `.env` contents, auth headers, or other secret material to Agentit.

Git ignores local report/backups/runtime patterns such as `reports/local/`, `backups/local/`, `.agentit/`, and `*.local.json`. **No file named exactly `settings.local.json` is tracked.** The repository template lives at `templates/claude/settings.local.example.json`; an agent may copy it to a machine-local Claude path only through an explicit opt-in install action.

Machine-local `.local` files remain untracked and must not be treated as safe places to publish or commit secrets merely because Git ignores them.

### Provider configuration

The normal launch/bootstrap path installs Agentit's runtime, core skill discovery surfaces and bounded agent profiles. It does **not** require replacing provider credentials or general provider configuration.

Optional settings/hook installation is deliberately separate from the normal path and must be explicitly requested/reviewed. Credentials and machine-specific secrets are never portable Agentit state.

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

## Supported bootstrap platforms

The canonical Python bootstrap is intended for **macOS and GNU/Linux** and is tested in CI on both platforms before the README may claim support.

The older `install.sh` / `update.sh` implementations remain GNU/Linux/Bash-4+-oriented compatibility paths and must not be used as evidence of macOS shell portability.

## Reporting vulnerabilities

Please report security vulnerabilities privately rather than opening a public issue:

- use GitHub Security Advisories for this repository;
- include a concise impact summary, reproduction steps, affected revision, and any safe proof-of-concept evidence;
- redact real secrets or personal data from reports.

Patches should be prepared before public disclosure when practical.
