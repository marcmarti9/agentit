# Digitem growth stack — Agentit wiring

Scouted / wired: 2026-08-18

## Intent

Digitem-style work is a **digital agency domain**, not only coding:
programming + marketing + SEO + paid media + analytics.

Agentit keeps **core** lean. Growth capabilities are **on-demand profiles + optional MCP**.

## Profiles

| Profile | Role |
|---------|------|
| `growth` | Strategy / CRO / copy layer on top of `product` |
| `seo` | SEO + GEO specialist |
| `paid_ads` | Media buyer specialist |
| `analytics` | Measurement / reporting |
| `digitem` | Agency umbrella (product + growth skills) |

Enable examples:

```bash
agentit enable digitem --project . --apply
agentit enable growth --project . --apply
```

## Skills (method)

| Id | Status |
|----|--------|
| `marketing-and-growth` | In-repo curated (active via product/growth) |
| `marketingskills` | Corey Haines pack — selective install, on-demand |
| `hyperfx-marketing-skills` | Execution layer — optional |
| `aaron-seo-geo-skills` | SEO/GEO specialist — optional |
| `claude-ads-audit-pack` | Audit depth — experimental until upstream pinned |
| `arcads-marketing-os` | Role OS — incubating until public artifact |

Install selective skills (example):

```bash
npx skills add coreyhaines31/marketingskills --skill page-cro copywriting seo-audit ai-seo paid-ads analytics-tracking
```

Do **not** dump every upstream skill into global discovery.

## MCP (hands)

| Stack / server | Use |
|----------------|-----|
| `growth_marketing` | Research + browser verification baseline |
| `digitem` | Dev core + research/browser for agency sessions |
| `meta-ads` | RISK_3 — human gate before writes |
| `google-ads` | RISK_3 — prefer read-only first |
| `ga4` | RISK_2 — live analytics |
| `google-search-console` | RISK_2 — organic evidence |

```bash
agentit mcp enable-stack digitem --apply
# after credentials + review:
agentit mcp enable ga4 --apply
agentit mcp enable google-search-console --apply
agentit mcp enable meta-ads --force --apply   # human review required
```

## Safety rules

1. Skills without MCP may invent KPIs — treat numbers as hypotheses until connected.
2. Ad-platform write tools require human approval.
3. Never commit OAuth tokens or service-account JSON.
4. Prefer client-scoped credentials per engagement.

## Next gates

- Pin concrete upstream commits for optional skill packs.
- Merge/close Arcads Marketing OS candidate when files + license exist.
- Optional: slim local adapters under `skills/` for Digitem house process.
