#!/usr/bin/env bash
# Importa solo componentes canónicos desde un provider; por defecto plan.
# Nunca importa settings.local, secretos ni directorios arbitrarios.
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
[[ ! -L "$USER_HOME" ]] || die "la raíz de usuario symlink se rechaza: $USER_HOME"
USER_HOME="$(cd "$USER_HOME" && pwd -P)"
assert_no_symlink_components() {
  local current="$1"
  while [[ "$current" != "/" && "$current" != "." && -n "$current" ]]; do
    [[ ! -L "$current" ]] || die "componente symlink rechazado: $current"
    current="$(dirname -- "$current")"
  done
}
case "$SOURCE_PROVIDER" in
  claude) SOURCE_ROOT="$USER_HOME/.claude"; SOURCE_SKILLS="$SOURCE_ROOT/skills" ;;
  codex) SOURCE_ROOT="$USER_HOME/.codex"; SOURCE_SKILLS="$SOURCE_ROOT/skills" ;;
  antigravity) SOURCE_ROOT="$USER_HOME/.gemini/antigravity-cli"; SOURCE_SKILLS="$USER_HOME/.agents/skills" ;;
  *) die "provider inválido: $SOURCE_PROVIDER" ;;
esac
[[ -d "$SOURCE_ROOT" ]] || die "no existe el target del provider: $SOURCE_ROOT"

if [[ "$MODE" == "plan" ]]; then
  printf 'MODO PLAN: no se escribirán archivos. Usa --apply para aplicar.\n'
else
  if [[ -z "$BACKUP_ROOT" ]]; then
    BACKUP_ROOT="$REPO_DIR/backups/update-$(date +%Y%m%d-%H%M%S)"
  fi
  assert_no_symlink_components "$BACKUP_ROOT"
  mkdir -p "$BACKUP_ROOT"
  printf 'provider=%s\ndate=%s\n' "$SOURCE_PROVIDER" "$(date --iso-8601=seconds)" > "$BACKUP_ROOT/manifest.txt"
fi

declare -A BACKED_UP=()

assert_source() {
  local path="$1"
  assert_no_symlink_components "$path"
  [[ -e "$path" ]] || die "fuente ausente: $path"
}

backup_existing() {
  local dst="$1"
  local rel="$2"
  [[ -e "$dst" || -L "$dst" ]] || return 0
  [[ ! -L "$dst" ]] || die "destino symlink rechazado: $dst"
  [[ -f "$dst" ]] || die "destino existente no es un archivo regular: $dst"
  [[ -n "${BACKED_UP[$dst]+yes}" ]] && return 0
  BACKED_UP["$dst"]=1
  local backup_path="$BACKUP_ROOT/$rel"
  assert_no_symlink_components "$backup_path"
  [[ ! -e "$backup_path" && ! -L "$backup_path" ]] || die "destino de backup ya existe: $backup_path"
  mkdir -p "$(dirname "$backup_path")"
  cp -a -- "$dst" "$backup_path"
  printf 'backup path=%s destination=%s original_sha256=%s backup_sha256=%s\n' \
    "$backup_path" "$dst" "$(sha256sum -- "$dst" | awk '{print $1}')" \
    "$(sha256sum -- "$backup_path" | awk '{print $1}')" >> "$BACKUP_ROOT/manifest.txt"
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
  local before_state="absent"
  [[ -e "$dst" ]] && before_state="present"
  local source_hash
  source_hash="$(sha256sum -- "$src" | awk '{print $1}')"
  backup_existing "$dst" "$rel"
  mkdir -p "$(dirname "$dst")"
  local tmp
  tmp="$(mktemp "$(dirname "$dst")/.agent-harness-import.XXXXXX")"
  cp --preserve=mode,timestamps -- "$src" "$tmp"
  mv -T -- "$tmp" "$dst"
  printf 'copy source=%s destination=%s before_state=%s source_sha256=%s backup=%s destination_sha256=%s\n' \
    "$src" "$dst" "$before_state" "$source_hash" \
    "$([[ "$before_state" == "present" ]] && printf '%s' "$BACKUP_ROOT/$rel" || printf '%s' none)" \
    "$(sha256sum -- "$dst" | awk '{print $1}')" >> "$BACKUP_ROOT/manifest.txt"
  printf 'importado: %s\n' "$dst"
}

# Allowlist: solo agentes adaptativos de Claude; Codex/Antigravity no son
# fuentes de la jerarquía. Los archivos ausentes se omiten con evidencia.
if [[ "$SOURCE_PROVIDER" == "claude" ]]; then
  for agent in architect auditor orchestrator supervisor worker; do
    if [[ -f "$SOURCE_ROOT/agents/$agent.md" ]]; then
      import_file "$SOURCE_ROOT/agents/$agent.md" "$REPO_DIR/agents/$agent.md" "agents/$agent.md"
    else
      printf 'skip: agente no instalado: %s\n' "$agent"
    fi
  done
fi

for skill in architect-orchestrator supabase-postgres-best-practices; do
  if [[ -f "$SOURCE_SKILLS/$skill/SKILL.md" ]]; then
    import_file "$SOURCE_SKILLS/$skill/SKILL.md" "$REPO_DIR/skills/$skill/SKILL.md" "skills/$skill/SKILL.md"
  else
    printf 'skip: skill no instalada: %s\n' "$skill"
  fi
done
if [[ -f "$SOURCE_SKILLS/task-router/SKILL.md" ]]; then
  import_file "$SOURCE_SKILLS/task-router/SKILL.md" "$REPO_DIR/router/SKILL.md" "router/SKILL.md"
else
  printf 'skip: task-router no instalado en el provider\n'
fi

if [[ "$WITH_SETTINGS" == "true" ]]; then
  [[ "$SOURCE_PROVIDER" == "claude" ]] || die "settings solo se importa desde Claude"
  printf 'ADVERTENCIA: settings.json puede contener hooks y preferencias de máquina.\n'
  import_file "$SOURCE_ROOT/settings.json" "$REPO_DIR/settings.json" "settings.json"
fi
if [[ "$WITH_HOOK" == "true" ]]; then
  [[ "$SOURCE_PROVIDER" == "claude" ]] || die "hook solo se importa desde Claude"
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
