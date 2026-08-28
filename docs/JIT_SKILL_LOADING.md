# JIT skill loading and host isolation

Agentit treats provider-native skill directories as **startup context surfaces**, not passive storage.

Most capable coding-agent hosts use progressive disclosure: they advertise at least skill names/descriptions before loading the full body. Therefore copying the whole Agentit catalog into a host skill directory is already a context leak even if each `SKILL.md` body is lazy.

## Invariant

A fresh Agentit session exposes exactly three Agentit skills to the host:

```text
using-agentit
+ task-router
+ using-agent-skills
```

All other Agentit skills remain in the private runtime library and are loaded only after the active model selects them for the current stage.

## Provider surfaces

The portable bootstrap projects the same three core skills to each provider's dedicated discovery root:

| Provider | Agentit host-visible root |
|---|---|
| Claude Code | `~/.claude/skills` |
| Codex | `~/.agents/skills` |
| Grok Build | `~/.grok/skills` |
| Gemini CLI | `~/.gemini/skills` |
| Antigravity | `~/.gemini/config/skills` |

Codex keeps host-specific model worker profiles under `~/.codex/agents`; those are execution bindings, not extra semantic skills.

The complete Agentit catalog remains under:

```text
~/.agentit/runtime/skills
```

Provider CLIs must not be pointed at that private runtime directory.

## Progressive disclosure

The active model uses bounded discovery:

```text
agentit skills packs
agentit skills candidates engineering backend
agentit skills show debugging-and-error-recovery security-and-hardening --project .
```

The first command exposes only pack IDs and short domain descriptions. The second exposes only candidate metadata from requested packs. The third loads exact selected bodies and emits a skill-load receipt.

`skills/using-agent-skills/references/packs.md` remains canonical backing data, but it is not intended to be injected wholesale into model context for ordinary discovery.

## Existing installations

Older Agentit versions may have copied non-core skills into provider-visible roots. Bootstrap now inspects current and known legacy roots.

An old non-core directory is automatically removed only when its complete tree exactly matches the current Agentit source copy. Before removal, it is copied into the bootstrap backup and recorded as a reversible `removed_skill_tree` receipt.

A same-ID skill whose contents differ is treated as user-owned/modified and is never deleted automatically. This is deliberate: reducing Agentit context does not authorize destroying unrelated user configuration.

## Cold-session semantics

Persisting files in `~/.agentit/runtime/skills` means **available**, not active. A new session starts from the three core skills again. Previous selected bodies, pack choices, workers, references and MCP decisions do not become semantic startup state.

## Design boundary

The model decides:

- relevant packs;
- selected skills and count;
- when a body is worth its context cost;
- whether selection changes during execution.

Software performs only mechanical work:

- enumerate bounded pack metadata;
- load exact requested bodies;
- verify paths and hashes;
- keep provider roots core-only;
- back up and safely remove provably Agentit-managed legacy copies;
- restore those copies during rollback.

This preserves Agentit's LLM-native rule: **the primary AI makes semantic decisions; software enforces deterministic packaging and safety invariants.**
