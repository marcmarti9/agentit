#!/usr/bin/env bash
# Instala esta configuración de Claude Code en ~/.claude/ de esta máquina.
# Uso: bash install.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$HOME/.claude"
BACKUP="$HOME/.claude/backups/pre-install-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$TARGET" "$BACKUP"

copy_with_backup() {
  local rel="$1"
  local src="$REPO_DIR/$rel"
  local dst="$TARGET/$rel"
  [ -e "$src" ] || return 0
  if [ -e "$dst" ]; then
    mkdir -p "$BACKUP/$(dirname "$rel")"
    cp -r "$dst" "$BACKUP/$rel"
  fi
  mkdir -p "$(dirname "$dst")"
  rm -rf "$dst"
  cp -r "$src" "$dst"
  echo "instalado: $rel"
}

copy_with_backup "agents"
copy_with_backup "hooks"
copy_with_backup "skills/supabase-postgres-best-practices"
copy_with_backup "settings.json"
copy_with_backup "settings.local.json"

chmod +x "$TARGET/hooks/"*.sh 2>/dev/null || true

echo
echo "Listo. Copia de seguridad de lo que había antes (si algo había) en:"
echo "  $BACKUP"
echo
echo "Si settings.json ya tenía claves que no están en este repo (env, plugins"
echo "específicos de esta máquina, etc.), revisa el diff a mano — este script"
echo "SOBRESCRIBE settings.json entero, no hace merge."
