# Vendored upstream design skills

These packages are copied from their canonical upstream repositories without compressing or rewriting their skill bodies. Agentit-specific routing and composition belong outside the vendored packages.

| Agentit skill | Upstream | Upstream path | Snapshot |
| --- | --- | --- | --- |
| `design-taste-frontend` | `Leonxlnx/taste-skill` | `skills/taste-skill` | `ccbc15639c97057cbfcf32ecebc38ef716e4bb37` |
| `impeccable` | `pbakaus/impeccable` | `.agents/skills/impeccable` | `fcc271c1cb5e1ef17022dd8b84074361b4d0acd7` (skill v4.1.3) |
| `emil-design-eng` | `emilkowalski/skills` | `skills/emil-design-eng` | `d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7` |

Refresh all three snapshots with:

```bash
./scripts/sync-upstream-design-skills.sh
```
