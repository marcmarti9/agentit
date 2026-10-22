# Use Agentit from a chat or coding agent

Agentit is an operating protocol plus a library of expertise. Reading and applying
its instructions is the primary use; CLI installation is an optional adapter for
discovery, exact-byte delivery, verification and continuity. A normal chat can
use the same core and skills through file uploads or an authorized repository
reader. It cannot run tools its host does not provide.

## Start without installing

Use this instruction, with an accessible copy of this repository:

> Use Agentit for this task. Read AGENTIT.md completely, inspect its profile
> pointers, then read the complete skill files relevant to the task. Apply their
> procedures, finish the requested outcome, and report actual verification and
> any access limitations. Installing Agentit is not the requested outcome.

[AGENTIT.md](../AGENTIT.md) is a generated single-file copy of the three exact
core bodies, including all profile purpose pointers. The
[profile index](../references/agentit-profile-index.md) maps each domain to its
skills and actual repository paths. Follow paths within the same revision.
Agentit-owned and imported expertise share this navigation; vendor directories
preserve provenance and are not a separate user workflow.

For an ordinary chat, provide the starter file and profile index as uploaded
files or accessible repository content. The chat then retrieves the selected
skills using its authorized reader. If it has no reader, supply those selected
files too. Uploading the starter alone does not upload the library. For recurring
use, put the startup instruction in the host's project instructions and make the
files available as project sources. Do not assume a chat discovers local
`AGENTS.md` or local skill installation automatically.

ChatGPT project instructions and shared sources are documented in
[Projects and chats](https://learn.chatgpt.com/docs/projects). These host features
do not establish that Agentit files were actually retrieved in a particular chat.
Agent Skills distinguishes metadata discovery from complete body activation:
[specification](https://agentskills.io/specification). Agentit keeps this split.

## With an installed adapter

The core still requires complete reads and task-specific application. Useful
agent-facing commands are:

```sh
agentit skills profiles --format json
agentit skills candidates --profile backend --format json
agentit skills activate api-and-interface-design --project /absolute/project
```

Profiles are domain discovery and optional installation sets. Packs remain
additional task-oriented views. Neither selects expertise semantically; that is
the model's responsibility. Installing a profile is not needed to discover it.
Only the three navigation bodies are globally exposed by Agentit.

## Read enough, then apply

Scan profile purposes, inspect matching skill metadata, and select bodies that
cover the material requirements and current risks. Read those bodies fully.
Loading fewer skills is not a goal in itself. Loading every skill in a broad
profile introduces irrelevant procedures and conflicting workflow owners.

A complete profile is appropriate when all its members apply and their combined
size fits the context. Select its actual IDs explicitly and record the reason.
Otherwise stage selection as the task advances, or delegate bounded subproblems
when useful and authorized. A profile name never substitutes for its bodies.

Keep a compact application record in the task state: selected IDs, actual reads,
applicable constraints/checks and observed outcome evidence. Do not dump private
reasoning or repeat process banners for each small action. At completion compare
the result with the user's complete scope and the applicable procedures.

For code, BUILDER completes requested behavior with focused checks. REVIEW
freezes feature scope and validates the finished change. These rules belong to
the core and apply even if `anti-overengineering` was not selected. Imported
workflows cannot force broader architecture, repeated audits or extra features.

## Honest boundaries

If the host cannot read the remaining body after truncation, disclose the missing
content before dependent work. If it cannot execute a verifier, report that
verification as unavailable. If it lacks workers, self-review remains
self-review. A CLI delivery receipt proves delivered bytes, not attention,
comprehension or compliance. Agentit does not override system permissions.

## Maintain the portable entry

```sh
python3 scripts/build_profile_index.py
python3 scripts/build_chat_entry.py
python3 scripts/build_profile_index.py --check
python3 scripts/build_chat_entry.py --check
```

The generated entry contains no project data, private receipts, transcripts,
credentials, installed state or complete domain catalog bodies. Source hashes
detect accidental drift, not adversarial authorship.
