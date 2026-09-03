#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

clone() {
  local repo="$1"
  local dest="$2"
  git clone --quiet --depth 1 "$repo" "$dest"
}

clone https://github.com/Leonxlnx/taste-skill.git "$TMP/taste"
clone https://github.com/pbakaus/impeccable.git "$TMP/impeccable"
clone https://github.com/emilkowalski/skills.git "$TMP/emil"

for source in \
  "$TMP/taste/skills/taste-skill/SKILL.md" \
  "$TMP/impeccable/.agents/skills/impeccable/SKILL.md" \
  "$TMP/emil/skills/emil-design-eng/SKILL.md"; do
  test -f "$source" || { echo "missing expected upstream skill: $source" >&2; exit 1; }
done

rm -rf \
  "$ROOT/skills/design-taste-frontend" \
  "$ROOT/skills/impeccable" \
  "$ROOT/skills/impeccable-design" \
  "$ROOT/skills/emil-design-eng"

mkdir -p \
  "$ROOT/skills/design-taste-frontend" \
  "$ROOT/skills/impeccable" \
  "$ROOT/skills/emil-design-eng"

cp -a "$TMP/taste/skills/taste-skill/." "$ROOT/skills/design-taste-frontend/"
cp -a "$TMP/impeccable/.agents/skills/impeccable/." "$ROOT/skills/impeccable/"
cp -a "$TMP/emil/skills/emil-design-eng/." "$ROOT/skills/emil-design-eng/"

TASTE_SHA="$(git -C "$TMP/taste" rev-parse HEAD)"
IMPECCABLE_SHA="$(git -C "$TMP/impeccable" rev-parse HEAD)"
EMIL_SHA="$(git -C "$TMP/emil" rev-parse HEAD)"
IMPECCABLE_VERSION="$(python3 - "$ROOT/skills/impeccable/SKILL.md" <<'PY'
from pathlib import Path
import re
import sys
text = Path(sys.argv[1]).read_text(encoding="utf-8")
match = re.search(r"(?m)^\s*version:\s*([^\s]+)\s*$", text)
print(match.group(1) if match else "unknown")
PY
)"

cat > "$ROOT/skills/UPSTREAM_SOURCES.md" <<EOF
# Vendored upstream design skills

These packages are copied from their canonical upstream repositories without compressing or rewriting their skill bodies. Agentit-specific routing and composition belong outside the vendored packages.

| Agentit skill | Upstream | Upstream path | Snapshot |
| --- | --- | --- | --- |
| \`design-taste-frontend\` | \`Leonxlnx/taste-skill\` | \`skills/taste-skill\` | \`$TASTE_SHA\` |
| \`impeccable\` | \`pbakaus/impeccable\` | \`.agents/skills/impeccable\` | \`$IMPECCABLE_SHA\` (skill v$IMPECCABLE_VERSION) |
| \`emil-design-eng\` | \`emilkowalski/skills\` | \`skills/emil-design-eng\` | \`$EMIL_SHA\` |

Refresh all three snapshots with:

\`\`\`bash
./scripts/sync-upstream-design-skills.sh
\`\`\`
EOF

printf 'Synced design skills:\n'
printf '  taste       %s\n' "$TASTE_SHA"
printf '  impeccable  %s (v%s)\n' "$IMPECCABLE_SHA" "$IMPECCABLE_VERSION"
printf '  emil         %s\n' "$EMIL_SHA"
