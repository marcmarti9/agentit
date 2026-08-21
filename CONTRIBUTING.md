# Contributing to Agentit

Thank you for your interest in contributing to **Agentit**!

Agentit is an early-stage, opinionated, safety-first agent harness designed for AI coding agents (**Claude Code**, **OpenAI Codex**, **Google Antigravity / Open Skills**, **Grok Build**, and compatible providers).

---

## Core Principles for Contributions

1. **AI-native decisions**: Do not add regex, keyword, scoring, or deterministic prompt classifiers for semantic task routing. The primary AI decides from full context and a second AI reviews the proposed decision before material execution.
2. **Intelligent delegation**: Do not add decorative agent hierarchies, but do use independent workers when specialization, isolation, breadth, latency, or fresh judgment provides a concrete benefit. The economy decision reviewer is a deliberate baseline second opinion, not multi-agent theater.
3. **Provider Neutrality**: Agentit policies, skills, semantic tiers, and reviewer contracts must remain platform-agnostic and work across providers.
4. **Safety & Reversibility**: Deployment or management scripts (`install.sh`, `update.sh`, `harden-local.sh`) must run in dry-run/plan mode by default and require an explicit `--apply` flag to modify files.
5. **Machine Isolation**: Never commit local paths, machine-specific configurations, OAuth credentials, or environment secrets. The machine inventory (`reports/local/inventory.yaml`) must remain ignored by git.

---

## How to Contribute

### 1. Developing & Adding Skills

Skills must be modular, single-responsibility guides or tools.

- Place new skills inside `skills/<skill-name>/`.
- Each skill directory must contain a valid `SKILL.md` with YAML frontmatter declaring `name` and `description`.
- Keep skill bodies clean and concise to preserve agent context windows.
- Keep discovery descriptions short and discriminative: explain when the knowledge is useful and one clear non-trigger.
- Add new skills to an opt-in profile in `profiles.yaml` before considering global visibility.
- A skill ID is not proof the skill was used; the stage model must receive/read the actual body.

### 2. Task-decision & review policy improvements

Semantic task decisions live in policy, not executable prompt classifiers:

- `skills/task-router/SKILL.md` defines the primary model's `TASK_DECISION` rubric.
- `skills/task-router/references/economy-reviewer.md` defines the mandatory cheap second-model review.
- `skills/using-agentit/SKILL.md` defines the end-to-end operating protocol.
- `docs/NO_PROGRAMMATIC_ROUTER.md` defines the boundary between AI judgment and mechanical software.

When changing these policies:

- preserve full-context semantic judgment by the active AI;
- preserve the ordinary cheap read-only second opinion;
- preserve stronger review escalation for high-consequence work;
- keep review loops bounded;
- do not reintroduce programmatic risk/category/topology/skill selection from prompt text.

Mechanical Python/shell code may manage manifests, profiles, capabilities, MCP/runtime state, continuity, verification, and similar infrastructure after the AI has decided what to do.

### 3. Testing

Before submitting a Pull Request, verify that all mechanical/runtime test suites pass:

```bash
python3 -m unittest discover -s router -p "test_*.py"
python3 -m unittest discover -s tests
```

Do not add a deterministic prompt-classification benchmark and present it as evidence that Agentit understands natural language. Tests should target mechanical contracts, safety properties, persistence, tooling, and runtime behavior.

---

## Submitting Pull Requests

1. Fork the repository and create a feature branch (`git checkout -b feature/my-feature`).
2. Make your changes adhering to the policy, code style, and safety rules.
3. Verify all tests pass locally.
4. Submit a Pull Request with a clear description of the problem solved and changes made.
