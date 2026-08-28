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

All other Agentit skills remain in private Agentit storage and are loaded only after the active model selects them for the current stage.

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

The complete global Agentit catalog remains under:

```text
~/.agentit/runtime/skills
```

Provider CLIs must not be pointed at that private runtime directory.

## Project profiles are availability, not host context

Project profiles such as `frontend`, `design`, `agency` or `supabase` also stay outside provider discovery roots.

`agentit enable <profile> --project . --apply` stores Agentit-managed profile packages under:

```text
<project>/.agentit/profile-skills/
```

It does **not** copy those packages into `<project>/.agents/skills`. The latter remains a project-native/user-owned provider surface and keeps precedence when the project intentionally defines its own skill.

When a selected skill is requested, Agentit resolves in this order:

```text
project-native .agents/skills
-> private .agentit/profile-skills
-> global Agentit runtime library
```

This lets a profile make expertise available without advertising its entire skill set at session startup.

Older Agentit project manifests that previously managed copies in `.agents/skills` are migrated only if every managed file still matches the recorded installed hash and the skill directory contains no unknown user files. Modified legacy copies fail closed for manual review instead of being deleted.

## Progressive disclosure

The active model uses bounded discovery:

```text
agentit skills packs
agentit skills candidates engineering backend
agentit skills show debugging-and-error-recovery security-and-hardening --project .
```

The first command exposes only pack IDs and short domain descriptions. The second exposes only candidate metadata from requested packs. The third loads exact selected bodies and emits a skill-load receipt.

`skills/using-agent-skills/references/packs.md` remains canonical backing data, but it is not intended to be injected wholesale into model context for ordinary discovery.

## Existing global installations

Older Agentit versions may have copied non-core skills into provider-visible global roots. Bootstrap now inspects current and known legacy roots.

An old non-core directory is automatically removed only when its complete tree matches the current Agentit source copy, or when it is the historical `SKILL.md`-only projection and that body matches exactly. Before removal, it is copied into the bootstrap backup and recorded as a reversible `removed_skill_tree` receipt.

A same-ID skill whose contents differ is treated as user-owned/modified and is never deleted automatically. This is deliberate: reducing Agentit context does not authorize destroying unrelated user configuration.

## Cold-session semantics

Persisting files in `~/.agentit/runtime/skills` or `<project>/.agentit/profile-skills` means **available**, not active. A new session starts from the three core skills again. Previous selected bodies, pack choices, workers, references and MCP decisions do not become semantic startup state.

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
- keep Agentit-managed project profiles private;
- back up and safely remove provably Agentit-managed global legacy copies;
- safely migrate provably unchanged project-profile legacy copies;
- restore global bootstrap removals during rollback.

This preserves Agentit's LLM-native rule: **the primary AI makes semantic decisions; software enforces deterministic packaging and safety invariants.**
