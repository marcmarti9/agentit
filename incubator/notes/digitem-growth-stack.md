# Digitem growth stack — Agentit wiring

Scouted / wired: 2026-08-18

## Intent

Digitem-style work is a **digital agency domain**, not only coding:
programming + marketing + SEO + paid media + analytics.

Agentit keeps **core** lean. The verified growth method is available through
on-demand profiles; marketing MCPs remain incubator candidates.

## Integrated profiles

| Profile | Role |
|---------|------|
| `growth` | Product/CRO/copy method plus launch discipline |
| `digitem` | Growth plus incremental delivery and Git handoffs |

Enable examples:

```bash
agentit enable digitem --project . --apply
agentit enable growth --project . --apply
```

## Skill candidates (not integrated)

| Id | Status |
|----|--------|
| `marketing-and-growth` | In-repo curated (active via product/growth) |
| `marketingskills` | Corey Haines pack — selective install, on-demand |
| `hyperfx-marketing-skills` | Execution layer — optional |
| `aaron-seo-geo-skills` | SEO/GEO specialist — optional |
| `claude-ads-audit-pack` | Audit depth — experimental until upstream pinned |
| `arcads-marketing-os` | Role OS — incubating until public artifact |

External packs remain incubator candidates. Review and pin their source,
license, current IDs and exact skill bodies before installing any selective
subset. Do **not** dump every upstream skill into global discovery.

## MCP candidates (not integrated)

Meta Ads, Google Ads, GA4 and Search Console are recorded only in
`incubator/candidates.yaml`. They are deliberately unavailable through
`agentit mcp` until a later integration reviews provider configuration,
credentials, risk gates and runtime tests. Do not present enable commands for
them yet.

## Safety rules

1. Skills without MCP may invent KPIs — treat numbers as hypotheses until connected.
2. Ad-platform write tools require human approval.
3. Never commit OAuth tokens or service-account JSON.
4. Prefer client-scoped credentials per engagement.

## Next gates

- Pin concrete upstream commits for optional skill packs.
- Merge/close Arcads Marketing OS candidate when files + license exist.
- Integrate only the connectors that have verified provider snippets and tests.
- Optional: slim local adapters under `skills/` for Digitem house process.
