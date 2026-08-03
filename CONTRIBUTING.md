# Contributing to Agentit

Thank you for your interest in contributing to **Agentit**!

Agentit is an early-stage, opinionated, safety-first agent harness designed for AI coding agents (**Claude Code**, **OpenAI Codex**, **Google Antigravity / Open Skills**, and **Grok Build**).

---

## Core Principles for Contributions

1. **Single-Agent-First**: Do not add multi-agent wrappers or complex hierarchies for tasks that can be solved by a single capable agent.
2. **Provider Neutrality**: Agentit policies, skills, and router logic must remain platform-agnostic and work seamlessly across providers.
3. **Safety & Reversibility**: All deployment or management scripts (`install.sh`, `update.sh`, `harden-local.sh`) must run in **dry-run plan mode by default** and require an explicit `--apply` flag to modify files.
4. **Machine Isolation**: Never commit local paths, machine-specific configurations, OAuth credentials, or environment secrets to the repository. The machine inventory (`reports/local/inventory.yaml`) must remain ignored by git.

---

## How to Contribute

### 1. Developing & Adding Skills
Skills must be modular, single-responsibility guides or tools.
- Place new skills inside `skills/<skill-name>/`.
- Each skill directory must contain a valid `SKILL.md` with YAML frontmatter declaring `name` and `description`.
- Keep skill bodies clean and concise to preserve agent context windows.

### 2. Router & Policy Improvements
- Router logic lives in `router/route.py` and `registry.yaml`.
- Ensure risk classification rules distinguish between *explaining* an action and *executing* an action on a target system.
- Add unit tests for any new router behavior in `router/test_route.py` or `router/test_registry.py`.

### 3. Testing
Before submitting a Pull Request, verify that all test suites pass:

```bash
# Run router tests
python3 -m unittest discover -s router -p "test_*.py"

# Run harness & script tests
python3 -m unittest discover -s tests
```

---

## Submitting Pull Requests

1. Fork the repository and create a feature branch (`git checkout -b feature/my-feature`).
2. Make your changes adhering to code style and safety rules.
3. Verify all tests pass locally.
4. Submit a Pull Request with a clear description of the problem solved and changes made.
