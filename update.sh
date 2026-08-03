#!/usr/bin/env bash
# Importa cambios locales seleccionados al repositorio de forma explícita.
# Por defecto solo muestra el plan y nunca importa settings.local ni secretos.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
USER_HOME="${HOME:?HOME must be set}"
MODE="plan"
SOURCE_PROVIDER="claude"
WITH_SETTINGS="false"
WITH_HOOK="false"
WITH_GUIDES="false"
BACKUP_ROOT=""

usage() {
  cat <<'EOF'
Uso: bash update.sh [opciones]

Por defecto no modifica el repositorio y muestra el plan.

  --apply                    aplicar cambios (requiere backup local)
  --provider NAME            claude|codex|antigravity (por defecto: claude)
  --home DIR                 raíz de usuario alternativa para pruebas
  --with-settings            importar settings.json (revisar hook y permisos)
  --with-hook                importar el hook de Claude explícitamente
  --with-guides              importar las guías globales explícitamente
  --backup-dir DIR           directorio explícito para backups
  --help                     mostrar esta ayuda
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 2
}

while (($#)); do
  case "$1" in
    --apply) MODE="apply" ;;
    --provider)
      (($# >= 2)) || die "--provider requiere un valor"
      SOURCE_PROVIDER="$2"
      shift
      ;;
    --home)
      (($# >= 2)) || die "--home requiere un valor"
      USER_HOME="$2"
      shift
      ;;
    --with-settings) WITH_SETTINGS="true" ;;
    --with-hook) WITH_HOOK="true" ;;
    --with-guides) WITH_GUIDES="true" ;;
    --backup-dir)
      (($# >= 2)) || die "--backup-dir requiere un valor"
      BACKUP_ROOT="$2"
      shift
      ;;
    --help|-h) usage; exit 0 ;;
    *) die "opción desconocida: $1" ;;
  esac
  shift
done

[[ -d "$USER_HOME" ]] || die "la raíz de usuario no existe: $USER_HOME"
USER_HOME="$(cd "$USER_HOME" && pwd -P)"
case "$SOURCE_PROVIDER" in
  claude) SOURCE_ROOT="$USER_HOME/.claude" ;;
  codex) SOURCE_ROOT="$USER_HOME/.codex" ;;
  antigravity) SOURCE_ROOT="$USER_HOME/.gemini/antigravity-cli" ;;
  *) die "provider inválido: $SOURCE_PROVIDER" ;;
esac
[[ -d "$SOURCE_ROOT" ]] || die "no existe el target del provider: $SOURCE_ROOT"

if [[ "$MODE" == "plan" ]]; then
  printf 'MODO PLAN: no se escribirán archivos. Usa --apply para aplicar.\n'
else
  if [[ -z "$BACKUP_ROOT" ]]; then
    BACKUP_ROOT="$REPO_DIR/backups/update-$(date +%Y%m%d-%H%M%S)"
  fi
  mkdir -p "$BACKUP_ROOT"
  printf 'provider=%s\ndate=%s\n' "$SOURCE_PROVIDER" "$(date --iso-8601=seconds)" > "$BACKUP_ROOT/manifest.txt"
fi

declare -A BACKED_UP=()

assert_source() {
  local path="$1"
  [[ -e "$path" ]] || die "fuente ausente: $path"
  [[ ! -L "$path" ]] || die "no se siguen symlinks: $path"
}

backup_existing() {
  local dst="$1"
  local rel="$2"
  [[ -e "$dst" || -L "$dst" ]] || return 0
  [[ ! -L "$dst" ]] || die "destino symlink rechazado: $dst"
  [[ -n "${BACKED_UP[$dst]+yes}" ]] && return 0
  BACKED_UP["$dst"]=1
  mkdir -p "$(dirname "$BACKUP_ROOT/$rel")"
  cp -a -- "$dst" "$BACKUP_ROOT/$rel"
  printf 'backup: %s\n' "$dst" >> "$BACKUP_ROOT/manifest.txt"
}

import_file() {
  local src="$1"
  local dst="$2"
  local rel="$3"
  assert_source "$src"
  [[ -f "$src" ]] || die "solo se importan archivos regulares: $src"
  if [[ "$MODE" == "plan" ]]; then
    printf 'plan: %s -> %s\n' "$src" "$dst"
    return 0
  fi
  backup_existing "$dst" "$rel"
  mkdir -p "$(dirname "$dst")"
  local tmp
  tmp="$(mktemp "$(dirname "$dst")/.agent-harness-import.XXXXXX")"
  cp --preserve=mode,timestamps -- "$src" "$tmp"
  mv -T -- "$tmp" "$dst"
  sha256sum "$dst" >> "$BACKUP_ROOT/manifest.txt"
  printf 'importado: %s\n' "$dst"
}

if [[ "$SOURCE_PROVIDER" == "antigravity" ]]; then
  SOURCE_SKILLS="$USER_HOME/.agents/skills"
else
  SOURCE_SKILLS="$SOURCE_ROOT/skills"
fi

# Allowlist deliberada: solo componentes que pertenecen a este harness.
for agent in architect auditor orchestrator supervisor worker; do
  import_file "$SOURCE_ROOT/agents/$agent.md" "$REPO_DIR/agents/$agent.md" "agents/$agent.md"
done
for skill in architect-orchestrator supabase-postgres-best-practices task-router; do
  if [[ -f "$SOURCE_SKILLS/$skill/SKILL.md" ]]; then
    if [[ "$skill" == "task-router" ]]; then
      import_file "$SOURCE_SKILLS/$skill/SKILL.md" "$REPO_DIR/router/SKILL.md" "router/SKILL.md"
    else
      import_file "$SOURCE_SKILLS/$skill/SKILL.md" "$REPO_DIR/skills/$skill/SKILL.md" "skills/$skill/SKILL.md"
    fi
  else
    printf 'skip: skill no instalada en el provider: %s\n' "$skill"
  fi
done

if [[ "$WITH_SETTINGS" == "true" ]]; then
  printf 'ADVERTENCIA: settings.json puede contener hooks y preferencias de máquina.\n'
  import_file "$SOURCE_ROOT/settings.json" "$REPO_DIR/settings.json" "settings.json"
fi
if [[ "$WITH_HOOK" == "true" ]]; then
  import_file "$SOURCE_ROOT/hooks/precompact-memory.sh" "$REPO_DIR/hooks/precompact-memory.sh" "hooks/precompact-memory.sh"
fi
if [[ "$WITH_GUIDES" == "true" ]]; then
  for guide in AGENTS.md CLAUDE.md CODEX.md; do
    import_file "$USER_HOME/$guide" "$REPO_DIR/$guide" "$guide"
  done
fi

if [[ "$MODE" == "plan" ]]; then
  printf 'Plan terminado. No se modificó el repositorio.\n'
else
  printf 'Importación aplicada con allowlist. Revisa git diff antes de commit.\n'
fi
