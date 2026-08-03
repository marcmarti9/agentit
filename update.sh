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
for f in CLAUDE.md CODEX.md; do
  if [ -f "$HOME/$f" ]; then
    cp "$HOME/$f" "$REPO_DIR/$f"
  fi
done

if [ -f "$HOME/.codex/AGENTS.md" ]; then
  cp "$HOME/.codex/AGENTS.md" "$REPO_DIR/AGENTS.md"
elif [ -f "$HOME/AGENTS.md" ]; then
  cp "$HOME/AGENTS.md" "$REPO_DIR/AGENTS.md"
fi

# Solo se sincronizan los perfiles portables declarados por este repo; no se
# suben perfiles personales ni el config.toml completo de la máquina.
if [ -d "$HOME/.codex/agents" ]; then
  mkdir -p "$REPO_DIR/.codex/agents"
  for f in terra-worker.toml luna-worker.toml; do
    if [ -f "$HOME/.codex/agents/$f" ]; then
      cp "$HOME/.codex/agents/$f" "$REPO_DIR/.codex/agents/$f"
    fi
  done
fi

echo "Sincronización completada sin mezclar agentes de Claude y Codex."
