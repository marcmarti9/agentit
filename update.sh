#!/usr/bin/env bash
# Sincroniza la configuración local hacia este repo sin mezclar proveedores.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Claude Code es la fuente de la jerarquía multiagente.
if [ -d "$HOME/.claude/agents" ]; then
  mkdir -p "$REPO_DIR/agents"
  rm -rf "$REPO_DIR/agents"/*
  cp -r "$HOME/.claude/agents/"* "$REPO_DIR/agents/"
fi

for f in settings.json settings.local.json; do
  if [ -f "$HOME/.claude/$f" ]; then
    cp "$HOME/.claude/$f" "$REPO_DIR/$f"
  fi
done

if [ -d "$HOME/.claude/hooks" ]; then
  mkdir -p "$REPO_DIR/hooks"
  rm -rf "$REPO_DIR/hooks"/*
  cp -r "$HOME/.claude/hooks/"* "$REPO_DIR/hooks/"
fi

# Las guías globales se sincronizan de forma explícita. CODEX.md no se genera
# desde ~/.codex/agents ni absorbe la configuración de Claude.
for f in AGENTS.md CLAUDE.md CODEX.md; do
  if [ -f "$HOME/$f" ]; then
    cp "$HOME/$f" "$REPO_DIR/$f"
  fi
done

echo "Sincronización completada sin mezclar agentes de Claude y Codex."
