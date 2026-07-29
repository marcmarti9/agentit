#!/usr/bin/env bash
# Instala esta configuración unificada de agentes (Claude Code, Antigravity, Codex) en esta máquina.
# Uso: bash install.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

install_to_target() {
  local target_dir="$1"
  local backup_dir="$target_dir/backups/pre-install-$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$target_dir" "$backup_dir"

  copy_sub() {
    local rel="$1"
    local src="$REPO_DIR/$rel"
    local dst="$target_dir/$rel"
    [ -e "$src" ] || return 0
    if [ -e "$dst" ]; then
      mkdir -p "$backup_dir/$(dirname "$rel")"
      cp -r "$dst" "$backup_dir/$rel"
    fi
    mkdir -p "$(dirname "$dst")"
    rm -rf "$dst"
    cp -r "$src" "$dst"
    echo "instalado en $target_dir: $rel"
  }

  copy_sub "agents"
  copy_sub "skills/architect-orchestrator"
  copy_sub "skills/supabase-postgres-best-practices"
}

# 1. Claude Code (~/.claude)
install_to_target "$HOME/.claude"
if [ -f "$REPO_DIR/settings.json" ]; then
  cp "$REPO_DIR/settings.json" "$HOME/.claude/settings.json"
fi
if [ -f "$REPO_DIR/settings.local.json" ]; then
  cp "$REPO_DIR/settings.local.json" "$HOME/.claude/settings.local.json"
fi
if [ -d "$REPO_DIR/hooks" ]; then
  mkdir -p "$HOME/.claude/hooks"
  cp -r "$REPO_DIR/hooks/"* "$HOME/.claude/hooks/"
  chmod +x "$HOME/.claude/hooks/"*.sh 2>/dev/null || true
fi

# 2. Codex (~/.codex)
install_to_target "$HOME/.codex"

# 3. Antigravity / Open Skills (~/.agents)
mkdir -p "$HOME/.agents/skills"
if [ -d "$REPO_DIR/skills/architect-orchestrator" ]; then
  cp -r "$REPO_DIR/skills/architect-orchestrator" "$HOME/.agents/skills/"
fi
if [ -d "$REPO_DIR/skills/supabase-postgres-best-practices" ]; then
  cp -r "$REPO_DIR/skills/supabase-postgres-best-practices" "$HOME/.agents/skills/"
fi

# 4. Archivos de guías globales en $HOME
for f in AGENTS.md CLAUDE.md CODEX.md; do
  if [ -f "$REPO_DIR/$f" ]; then
    cp "$REPO_DIR/$f" "$HOME/$f"
    echo "instalado: ~/$f"
  fi
done

echo
echo "Instalación completada correctamente para todos los proveedores de IA."
