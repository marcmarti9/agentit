#!/usr/bin/env bash
# PreCompact hook: antes de que se pierda detalle por compactación (manual o
# automática), pide a un Claude headless barato (Haiku) que actualice la
# memoria persistente del proyecto con lo imprescindible para retomar sin
# fricción. Ver ~/.claude/settings.json -> hooks.PreCompact.
set -euo pipefail

input="$(cat)"
transcript_path="$(printf '%s' "$input" | jq -r '.transcript_path // empty')"
cwd="$(printf '%s' "$input" | jq -r '.cwd // empty')"

# Sin transcripción no hay nada que resumir.
[ -n "$transcript_path" ] && [ -s "$transcript_path" ] || exit 0
[ -n "$cwd" ] || cwd="$HOME"

# Misma convención que el auto-memory nativo de Claude Code:
# ~/.claude/projects/<cwd-sanitizado>/memory/MEMORY.md
sanitized="$(printf '%s' "$cwd" | sed 's/\//-/g')"
mem_dir="$HOME/.claude/projects/${sanitized}/memory"
mem_file="$mem_dir/MEMORY.md"
mkdir -p "$mem_dir"

existing=""
[ -f "$mem_file" ] && existing="$(cat "$mem_file")"

# Solo las últimas líneas del JSONL: mantiene la llamada de resumen barata.
recent="$(tail -n 400 "$transcript_path" 2>/dev/null || true)"
[ -n "$recent" ] || exit 0

prompt="Esta conversación de Claude Code está a punto de compactarse y se va a perder detalle. A partir de la transcripción JSONL reciente de abajo (puede incluir ruido de tool calls), escribe una actualización BREVE (máx. 15 líneas, markdown) con: la tarea en curso, decisiones de diseño tomadas y por qué, qué queda pendiente, y datos costosos de re-averiguar. No dupliques lo que ya está en la memoria existente, integra ambas cosas. Devuelve SOLO el markdown final combinado, listo para guardar tal cual, sin explicaciones ni fences de código alrededor.

MEMORIA EXISTENTE:
${existing:-'(vacía)'}

TRANSCRIPCIÓN RECIENTE:
${recent}"

summary="$(claude -p "$prompt" --model haiku 2>/dev/null || true)"

if [ -n "$summary" ]; then
  printf '%s\n' "$summary" > "$mem_file"
fi
exit 0
