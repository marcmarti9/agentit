# Codex Luna execution policy — 2026-10-22

## Problem and correction

Agentit shipped `luna_worker` pinned to `gpt-5.6-luna`. Its setup guide recommended high-context reading, complex implementation and larger isolated workloads. The old worker prompt reserved interpretation/integration to the parent and escalated decisions outside its scope, but did not require a Sol supervisor or prohibit consequential decisions inside a broadly delegated objective. It did not meet the requested execution-only boundary.

The portable Codex adapter and installed worker now use `gpt-6-luna` with the existing `max` reasoning effort. Luna receives a closed contract from GPT-6.1 Sol or GPT-6 Sol: decided steps, read/write ownership, expected output, exact checks and stop/escalation conditions. Missing context and consequential choices return to Sol. Architecture, product/security decisions, open-ended implementation/research, diagnosis, review/approval and supervision are excluded. Sol inspects the actual result before acceptance. Luna performs no commits, pushes, deployments, remote migrations, data/backup deletion or external mutations.

`CODEX.md` makes this limit discoverable before model selection and extends it to explicit overrides and differently named roles. Core task-router adds a short authority invariant; detailed portable guidance remains JIT in architect-orchestrator. Other providers and unrelated models/defaults are preserved. Task length or writing volume is not a justification to select an execution-only model.

## Verification and installation

- 370 runtime tests and 75 script tests passed, including a new actual temporary-home migration/rollback regression that preserves the primary model settings and a custom role.
- Generated portable entry and unified profile metadata match canonical bodies. Core remains exactly three bodies, 15,968 bytes within its 16,000-byte cap. Both modified skills pass Skill Creator validation; whitespace checks pass.
- A fresh real `gpt-6-luna` worker applied an exact label replacement in an isolated fixture. Sol checked the resulting bytes. A subsequent architecture request without requirements was escalated without further edits. The model selection was verified from host metadata. This exercised the new role text with an explicit model binding because the originating chat retained the old custom-role descriptor; it does not certify fresh-session role loading or universal instruction compliance.
- The canonical all-provider bootstrap updated 14 files with a rollback receipt, including the local Codex worker. Repeat planning reported 5,572 keep operations and no changes. The primary local model remains GPT-6.1 Sol. Existing unrelated/private files were preserved.

Role instructions and a declared supervisor model are not a sandbox or authenticated model check. Already-running chats may retain the old role/model descriptor: start a fresh session and verify the exposed binding before using the custom role. Other machines need the updated source and bootstrap too.

## Usage attribution limits

The supplied account message chart establishes model-labelled message volume, not decision authority. A separate Sol auditor inspected local metadata and available bounded rollout samples. These artifacts do not establish the accountwide cause of the chart or reconstruct historical Luna decisions. Automatic approval reviews expose an internal model label without its underlying billing-model mapping. Do not infer that mapping or claim that no important decision was ever delegated. Detailed local usage aggregates remain private rather than publishing account/session inventory.

Official model ID and custom-role configuration checked against [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) and [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). No provider-internal model or accountwide settings were modified.
