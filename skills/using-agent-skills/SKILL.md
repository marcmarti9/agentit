---
name: using-agent-skills
description: Agentit-owned navigation adapter. Discover bounded skill metadata and load only the bodies selected for the current task and stage.
---

# Using Agent Skills with Agentit

This is Agentit's own adapter, informed by Addy Osmani's Agent Skills. The
unchanged upstream meta-workflow is retained as source material under
`vendor/agent-skills/using-agent-skills`; it is not a fourth global skill.
Origins, file hashes and licenses are recorded in `skills/UPSTREAM_LOCK.json`.

## Select before loading

After `using-agentit` dispatch and `task-router`'s current `TASK_DECISION`:

1. Inspect relevant pack metadata only when discovery is useful:
   `agentit skills packs` and `agentit skills candidates <pack-id>`.
2. Select the concrete skill IDs that help this task and stage. A pack/profile
   makes capabilities available; it never prescribes a sequence or count.
3. Read selected bodies with
   `agentit skills show <skill-id> [<skill-id> ...] --project <project>`.
4. Load referenced material only as needed. Give workers just their selected
   guidance, permitted tools, scope, expected result and verifier.

The agent operates these commands; the user need not learn the CLI. Project
skills take precedence over private profile caches and the shared library.
An unresolved skill path is an explicit loading failure, not an active skill.

## Authority boundary

Host instructions and the user's current authorization govern execution.
Project constraints and Agentit's reviewed task decision own scope, execution
mode, skill/tool selection, delegation and verification.

Canonical source skills remain verbatim. Their words such as MUST, always,
every task, or a complete lifecycle apply only as useful guidance within the
selected stage. They do not activate other skills, force a new interview or
specification, expand the user's request, or authorize scripts, dependencies,
downloads, telemetry, external writes, publication or provider changes.

Use the source's domain expertise and respect its applicable checks. Resolve
material conflicts explicitly, retain host/user safety requirements, and
adapt the procedure in Agentit-owned policy instead of silently rewriting the
canonical package. A source's model preference is not a general dependency.

## Keep context bounded

Availability metadata, selected bodies and text already read are different.
Loading a body consumes context; removing its selection does not erase that
text from the current model context. Every new task/session makes a fresh
selection. Never dump the full catalog or inherit an old profile as active
instructions.

Verification follows the current execution mode in `using-agentit`, not a
mandatory spec/TDD/review/shipping sequence inferred from an upstream catalog.
