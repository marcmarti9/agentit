# Appllama contract (Agentit)

Upstream, not vendored:

- MCP: `https://mcp.appllama.io/mcp`
- Skills: https://github.com/Appllama/appllama-skills
- Site: https://appllama.io/mcp

Inspected 2026-08-26 from public MCP docs and the MIT skill repo. Do not treat this file as a substitute for the live tool schema.

## Enable

```bash
agentit mcp enable appllama --apply
```

Remote URL: `https://mcp.appllama.io/mcp`.
Host clients (Claude / Cursor / Codex / Grok / VS Code) may also add the connector manually.

Optional companion install outside Agentit:

```bash
npx skills add appllama/appllama-skills
```

Agentit does not require that installer. If both Agentit's skill and the upstream skills are visible, prefer **one** usage playbook to avoid duplicate instructions.

## Credits and limits

- `get_credits` is free and should run first.
- Other research calls typically spend 1 credit.
- Pro quota is vendor-stated (about 1,500 credits / month, reset on the 1st UTC). Confirm live via `get_credits`.
- Media URLs expire in about an hour. Screen ids are durable.
- Pagination is cursor-based and sequential. Restart the query if a cursor errors.
- Harvesting the catalog (extracting the dataset rather than answering a task) is against vendor terms.

## Tool map (as published)

| Tool | Job |
|---|---|
| `get_credits` | Balance / limits |
| `search_apps` | Category winners with revenue, downloads, rating, flows |
| `get_app` | One app in full |
| `list_app_screens` | Journey-ordered screens + media |
| `search_screens` | Keyword or semantic screen search |
| `get_screen` | One screen + similar siblings; accepts `app_id/screen_id` |
| `list_flows` / `get_flow_apps` | Flow taxonomy and best examples |
| `list_ui_elements` / `get_element_screens` | Component-level research |
| `list_my_boards` / `get_board` | Member-curated boards; start here if the user has one |

If the live MCP schema differs, trust the connected tools over this table.

## What Agentit forbids

- Shipping a 1:1 recreation of a studied screen.
- Reproducing the Appllama watermark.
- Claiming research that did not happen.
- Enabling Appllama on a web-only task "just in case".
- Spending the monthly quota on catalog sweeps.
