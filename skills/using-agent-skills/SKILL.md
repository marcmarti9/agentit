---
name: using-agent-skills
description: Discover Agentit skills through bounded semantic packs, then let the primary AI choose only the concrete bodies that materially help the current stage or worker.
---

# Using Agent Skills

Skills are **JIT knowledge**, not a context dump.

A new execution session starts with only Agentit's global core:

```text
using-agentit
+ task-router
+ using-agent-skills
```

The host-visible skill roots must contain only those three Agentit skills. The full Agentit skill library lives privately under Agentit's runtime and is discovered through the `agentit skills` CLI. A provider seeing a skill name/description is already context exposure, even if it has not opened that skill's `SKILL.md`.

**installation is not activation.** A skill may exist in Agentit's private runtime for discovery without being active model context. Only explicitly selected bodies count as active for the current stage.

## Progressive disclosure contract

Use these layers in order and stop as soon as enough context exists:

```text
LEVEL 0 — startup
3 core skills only

LEVEL 1 — domain discovery
agentit skills packs

LEVEL 2 — bounded candidate metadata
agentit skills candidates <pack...>

LEVEL 3 — exact selected bodies
agentit skills show <skill...> --project .

LEVEL 4 — references owned by an active skill
only the smallest relevant files
```

Do **not** open or inject the complete `references/packs.md` map just to discover one domain. That file is private backing data for bounded mechanical discovery. The model should normally use the CLI surfaces above.

## Pack-first discovery

For an Agentit task/stage:

```text
understand task
-> inspect only pack IDs/descriptions if needed
-> request metadata only for relevant pack(s)
-> AI chooses any number of skills that materially help
-> load only those exact SKILL.md bodies
-> execute / verify
-> add or remove bodies later if evidence changes the need
-> next session starts from the three core skills again
```

The primary AI owns semantic selection. Software only exposes requested metadata and bodies. There are intentionally **no fixed skill counts and no pack levels**.

A task may legitimately use no non-core skill, one skill, or several skills across packs. The deciding question is:

> Which skill bodies would materially improve this specific stage, and are they worth their context cost now?

## Profiles vs packs vs active context

These are deliberately different concepts:

- **Profiles** (`profiles.yaml`) are installation/discovery bundles. They answer which capabilities Agentit can make available.
- **Packs** are semantic discovery maps. They answer which capabilities might be relevant to a domain.
- **Selected skills** are the current stage's actual context bodies.

Never collapse these layers. Enabling a profile does not activate every skill in it; inspecting candidate metadata does not activate a skill; a previous session's selection never survives as active context in the next session.

## Selection rules

1. **Host roots are core-only for Agentit.** Never install/project non-core Agentit skills into `.claude/skills`, `.agents/skills`, `.grok/skills`, `.gemini/skills`, `.gemini/config/skills`, or another provider discovery root merely to make them available.
2. **Use packs as discovery maps, not bundles.** Never inject a whole pack merely because its domain matches.
3. **No quotas.** Do not target a predetermined number of skills.
4. **Load bodies, not IDs.** A non-core skill is active only when the executing model reads its exact body through `agentit skills show ...` or receives equivalent bounded worker injection.
5. **Cross-pack selection is allowed.** Choose whatever combination the actual task warrants.
6. **Do not preload cross-cutting skills.** Security, performance, references, MCP fit, orchestration, long-horizon recovery and advanced verification remain JIT.
7. **Project-local skills win.** Prefer compatible project-local instructions/skills over generic Agentit guidance.
8. **Selection can change during work.** Add a body when a concrete gap appears and stop carrying it when no longer useful.
9. **No cross-session semantic carry-over.** Previous selections are history/evidence only.
10. **Provider persistence is not activation.** Persistent MCP/config/plugin availability never means selected for the new task.

## Parent and worker loading

The same rule applies to the parent and delegated workers.

Parent example:

```text
agentit skills candidates engineering backend
agentit skills show debugging-and-error-recovery security-and-hardening --project .
```

Worker context should receive only:

```text
role / objective
relevant pack labels
selected skill bodies
selected references (if any)
project constraints/instructions
allowed tools/permissions
read/write scope
expected output/handoff
verification / stop condition
```

The parent keeps integration responsibility; workers do not receive the whole catalog.

## References are also JIT

`reference-intelligence` is not globally loaded. When external/current knowledge materially matters, first select that skill, then load only the smallest relevant curated/live source set. Re-select and re-verify across sessions when freshness matters.

## Tools are also JIT

Do not load `mcp-tooling-fit` or enable MCPs because they exist. Host/provider MCP configuration may persist beyond a task; persistence means available, not authorized or selected.

## Missing capability

If the selected pack(s) do not expose an adequate skill:

1. inspect project-local skills/instructions;
2. inspect another genuinely relevant pack through `agentit skills candidates`;
3. use approved external skill discovery when a durable reusable procedure could help;
4. use authoritative live sources for one-off/current facts;
5. adapt/create a new skill only when the procedure is durable and likely to recur.

## Anti-patterns

- installing all Agentit skills into a provider's native skill directory;
- relying on "the body is lazy" while exposing dozens of names/descriptions at startup;
- opening the full pack map for a one-pack task;
- loading every skill in a selected pack;
- carrying yesterday's selected bodies into today's task;
- spawning every worker with the same giant context;
- adding skills "just in case";
- treating persistent host/tool configuration as active semantic context.

## Completion check

Before execution/spawn, be able to answer:

```text
Why these pack(s)?
Why each selected skill?
Why is each selected body worth its context cost now?
What useful context did we deliberately NOT load?
Does the host-visible Agentit surface still contain only the three core skills?
```

There is no correct skill count. The correct set is whatever the primary AI can justify from the actual task.
