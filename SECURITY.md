# Security Policy & Principles

## Security Architecture

Agentit is designed with a **safety-first, deterministic security model**:

1. **Dry-Run by Default**: All management scripts (`install.sh`, `update.sh`, `security/harden-local.sh`) operate in plan mode by default. File modifications occur strictly when passed the explicit `--apply` flag.
2. **SHA-256 Backup Manifests**: Before overwriting or updating files, Agentit creates an atomic, timestamped backup directory with permissions `0700` and `0600` file modes.
3. **Symlink Rejection**: Scripts reject symlinked destinations or source files to prevent arbitrary file overwrite attacks.
4. **Machine Isolation**: Environment configuration state and local paths are isolated into `reports/local/inventory.yaml` and `settings.local.json`, which are excluded from source control. Agentit does not collect or store credentials or API secret values.

---

## Reporting Vulnerabilities

If you discover a security vulnerability within Agentit, please report it responsibly:

- **Do NOT open a public GitHub issue.**
- Submit a private security advisory via [GitHub Security Advisories](https://github.com/marcmarti9/agentit/security/advisories/new).
- Provide a summary of the issue, steps to reproduce, and potential impact.

We will review reports promptly and publish patches prior to public disclosure.
