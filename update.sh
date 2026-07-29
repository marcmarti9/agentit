#!/usr/bin/env bash
# Sincroniza los agentes, habilidades y configuraciones locales hacia este repo.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$HOME/.claude/agents" ]; then
  mkdir -p "$REPO_DIR/agents"
  cp -r "$HOME/.claude/agents/"* "$REPO_DIR/agents/"
fi

if [ -f "$HOME/.claude/settings.json" ]; then
  cp "$HOME/.claude/settings.json" "$REPO_DIR/settings.json"
fi

if [ -f "$HOME/.claude/settings.local.json" ]; then
  cp "$HOME/.claude/settings.local.json" "$REPO_DIR/settings.local.json"
fi

if [ -d "$HOME/.claude/hooks" ]; then
  mkdir -p "$REPO_DIR/hooks"
  cp -r "$HOME/.claude/hooks/"* "$REPO_DIR/hooks/"
fi

for f in AGENTS.md CLAUDE.md CODEX.md; do
  if [ -f "$HOME/$f" ]; then
    cp "$HOME/$f" "$REPO_DIR/$f"
  fi
done

echo "Sincronización hacia agents-config completada."
