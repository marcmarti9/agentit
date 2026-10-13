# ClickUp team tracking (opt-in)

Agentit can coordinate human work through **ClickUp's official remote MCP**, without a second issue tracker, custom API client, webhook, polling job or transcript collector. This is a **model-driven session workflow**; it is not continuous background monitoring. A connected ChatGPT ClickUp app and a connected Codex MCP are **separate OAuth authorizations**.

## Ownership and sources of truth

- **ClickUp**: agreed deliverables, the real human owner, current work status, concise progress, blockers and next action.
- **GitHub**: code, issues, PRs, CI/review and final merge evidence. Link these from ClickUp; don't copy raw diffs.
- **Private `.agentit/STATE.md`**: resumable context, including the ClickUp task ID/URL when known. Never send it, secrets, transcripts or private reasoning to ClickUp. A separately authorized private Git continuity sync is independent of ClickUp (see `docs/PROJECT_CONTINUITY.md`).
- **Agentit**: selects tools at task time and performs best-effort MCP synchronization at meaningful milestones. A configured MCP is not automatically authorized for an unrelated task.

No tracker is enabled in a fresh installation. The opt-in is user-level and applies across authorized team projects, not to every personal repository.

## One-time setup per machine/account

1. In ClickUp, create or choose one **shared work list** with ordinary `to do`, `in progress`, `complete` statuses (names may differ). Invite real collaborators individually to enable native assignees and filters; a shared service login is *not* two different assignees.
2. Copy [the example](../templates/team-tracking.example.json) to `~/.agentit/team-tracking.json`; fill in the existing Workspace ID, List ID, team name, repository scope and the names of real people. Keep this file **local** and readable only by its owner (`chmod 600`). Never commit it, even when it has no tokens.
3. In Codex, choose **one** configuration route:

   ```bash
   # Native Codex route
   codex mcp add clickup --url https://mcp.clickup.com/mcp
   codex mcp login clickup
   codex mcp list
   ```

   Or run `agentit mcp enable clickup --providers codex --apply` (after reviewing the plan), followed by `codex mcp login clickup`. Both routes configure the **same** server. OAuth takes place in the user's browser; do not request or save passwords/tokens. Open a new Codex session/reconnect MCP tools if necessary.

4. ChatGPT's ClickUp app must be connected **independently**. It has its own permissions and is not a shortcut for authorizing Codex.
5. Confirm read access to the intended ClickUp list, then do a limited real create/update/read test. A successful config write or `mcp list` alone does **not** verify an authenticated ClickUp write.

Official endpoint: `https://mcp.clickup.com/mcp`. References: [ClickUp MCP](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server) and [Codex MCP configuration](https://developers.openai.com/learn/docs-mcp).

### Local config example

```json
{
  "schema_version": 1,
  "enabled": true,
  "team": "Example team",
  "provider": "clickup",
  "workspace_id": "YOUR_WORKSPACE_ID",
  "list_id": "YOUR_LIST_ID",
  "repository_prefixes": ["your-organization/"],
  "additional_repositories": [],
  "members": {
    "Member A": null,
    "Member B": null
  }
}
```

A `members` entry maps the human's self-declared name to their **numeric ClickUp user ID**, or `null` if they have not joined yet. It is *not* a record of who is speaking: human identity must be established anew in each session, even when the same device, OS account, Git author or generic ClickUp account is reused. An explicitly named, team-owned project without a Git remote may be tracked only when the person confirms it belongs to the opted-in team.

## Session protocol (all opted-in projects)

1. **Scope and identity.** Check that the local config exists, is enabled, and matches the current team/repository. Derive the human operator's name only from the user's explicit declaration in this session or an equally trustworthy session-local statement. Do not infer identity from commit author, email, machine, or the shared team ClickUp login. If unknown, mark owner unconfirmed and ask only when needed for a meaningful assignment; never attribute work to the wrong person.
2. **Find before create.** Prefer the task ID/URL already in `.agentit/STATE.md`. Otherwise search the configured list using its project, exact outcome, GitHub issue/PR URL or the stable key below. If one clear task exists, update it. If matches are ambiguous or search is unavailable, do not create a likely duplicate: note the blocker and request clarification only if needed.
3. **One outcome, one task.** Create a task only for a substantial deliverable the team intends to coordinate, not every prompt, file change, test, research substep or background tool call. Use `[Operator] Project — Deliverable` as a *temporary* title fallback when the operator is not yet a ClickUp member. Do not assign a generic shared account as if it were Marc or Edgar. Native `assignees` should be used when the person's ClickUp ID resolves.
4. **Minimum description (brief).** Keep `Proyecto`, `Responsable real`, `Objetivo/criterio de cierre`, `Agentit key` (stable `repo:deliverable`), `GitHub` (issue/PR links), `Bloqueo` and `Siguiente acción`. Use ClickUp comments for dated progress checkpoints rather than rewriting the entire description or dumping private state.
5. **Meaningful synchronization.** Update at session start/resumption if the task state actually changed, on a major milestone (e.g. PR opened, review requested), a new blocker, ownership transfer or verified completion. Target a few writes per work session at most, never one update per command. Include actual evidence and a `Última actualización` timestamp; do not represent a stale status as live computer activity.
6. **Status semantics.** Use only the list's real statuses. `to do` = planned, `in progress` = being implemented/reviewed, `complete` = accepted/verified scope really finished. If there is no `blocked` status, keep `in progress` with a clearly named blocker. An open/unreviewed PR is not automatically `complete`. Never mark a task complete merely because a model wrote code.
7. **Failure and concurrency.** If ClickUp tools, OAuth, permissions or a member account are missing, the engineering task continues. Report `ClickUp pending sync` and retain only the task link or concise pending action in private local state. Do not invent success, retry writes blindly, or overwrite another person's recent comments/status. Re-read before significant ownership or completion changes.

When asked **“What is a particular team member doing?”**, query the configured list for native assignee IDs where available, otherwise exact title prefixes / real-owner descriptions. Return the tasks, latest confirmed update and blockers. Do not imply real-time monitoring outside active sessions.

## Acceptance tests

- With an authorized team config and explicit identity, one deliverable yields **one** ClickUp task and a real task URL.
- A second session from another computer finds that same task before writing progress.
- A non-member is identified visibly but **never impersonated** as a native ClickUp assignee.
- A second PR milestone adds progress without producing a duplicate or overwriting another person's work.
- Missing OAuth/list access results in a truthful pending-sync outcome; no data leaves the local project.
- Private `.agentit` continuity, raw chats and credentials never enter ClickUp.

This workflow is intentionally *not* a background sync daemon. For event-triggered or scheduled syncing, design a separate explicit GitHub webhook/ClickUp API integration only if real operational demand justifies it.
