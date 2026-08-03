#!/usr/bin/env bash
# Instala esta configuración de agentes separando Claude Code y Codex.
# Uso: bash install.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

backup_and_copy() {
  local src="$1"
  local dst="$2"
  [ -e "$src" ] || return 0

  if [ -e "$dst" ]; then
    local backup_root
    backup_root="$(dirname "$dst")/backups/pre-install-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$backup_root"
    cp -r "$dst" "$backup_root/$(basename "$dst")"
  fi

  mkdir -p "$(dirname "$dst")"
  rm -rf "$dst"
  cp -r "$src" "$dst"
  echo "instalado: $dst"
}

# Claude Code conserva la jerarquía multiagente y las skills.
mkdir -p "$HOME/.claude"
backup_and_copy "$REPO_DIR/agents" "$HOME/.claude/agents"
backup_and_copy "$REPO_DIR/skills/architect-orchestrator" "$HOME/.claude/skills/architect-orchestrator"
backup_and_copy "$REPO_DIR/skills/supabase-postgres-best-practices" "$HOME/.claude/skills/supabase-postgres-best-practices"

[ ! -f "$REPO_DIR/settings.json" ] || backup_and_copy "$REPO_DIR/settings.json" "$HOME/.claude/settings.json"
[ ! -f "$REPO_DIR/settings.local.json" ] || backup_and_copy "$REPO_DIR/settings.local.json" "$HOME/.claude/settings.local.json"

if [ -d "$REPO_DIR/hooks" ]; then
  backup_and_copy "$REPO_DIR/hooks" "$HOME/.claude/hooks"
  chmod +x "$HOME/.claude/hooks/"*.sh 2>/dev/null || true
fi

# Codex recibe la guía global, workers acotados y skills compartidas. No se
# instala la jerarquía de agentes de Claude en ~/.codex/agents.
mkdir -p "$HOME/.codex/agents" "$HOME/.codex/skills"
for agent_file in "$REPO_DIR/.codex/agents/"*.toml; do
  [ -f "$agent_file" ] || continue
  backup_and_copy "$agent_file" "$HOME/.codex/agents/$(basename "$agent_file")"
done
backup_and_copy "$REPO_DIR/skills/architect-orchestrator" "$HOME/.codex/skills/architect-orchestrator"
backup_and_copy "$REPO_DIR/skills/supabase-postgres-best-practices" "$HOME/.codex/skills/supabase-postgres-best-practices"

# Open Skills / Antigravity.
mkdir -p "$HOME/.agents/skills"
backup_and_copy "$REPO_DIR/skills/architect-orchestrator" "$HOME/.agents/skills/architect-orchestrator"
backup_and_copy "$REPO_DIR/skills/supabase-postgres-best-practices" "$HOME/.agents/skills/supabase-postgres-best-practices"

# Guías globales. AGENTS.md es la fuente común; las otras son adaptadores.
for f in AGENTS.md CLAUDE.md CODEX.md; do
  [ ! -f "$REPO_DIR/$f" ] || backup_and_copy "$REPO_DIR/$f" "$HOME/$f"
done
[ ! -f "$REPO_DIR/AGENTS.md" ] || backup_and_copy "$REPO_DIR/AGENTS.md" "$HOME/.codex/AGENTS.md"

cat <<'EOF'

Instalación completada.
- Claude Code: jerarquía multiagente + skills.
- Codex: guía global + workers acotados + skills compartidas, sin jerarquía obligatoria.
EOF
