#!/usr/bin/env bash
# Trae a este repo los cambios hechos localmente en ~/.claude/, para poder
# revisarlos con git diff y luego hacer commit + push.
# Uso: bash update.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HOME/.claude"

cp "$SRC"/agents/*.md "$REPO_DIR"/agents/
cp "$SRC"/hooks/*.sh "$REPO_DIR"/hooks/ 2>/dev/null || true
cp "$SRC"/settings.json "$REPO_DIR"/settings.json
cp "$SRC"/settings.local.json "$REPO_DIR"/settings.local.json
rm -rf "$REPO_DIR"/skills/supabase-postgres-best-practices
cp -r "$SRC"/skills/supabase-postgres-best-practices "$REPO_DIR"/skills/

echo "Repo actualizado desde ~/.claude. Revisa con:"
echo "  cd $REPO_DIR && git status && git diff"
echo "y luego:"
echo "  git add -A && git commit -m \"...\" && git push"
