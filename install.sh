#!/usr/bin/env bash
# Despliegue reversible y separado por proveedor.
# Por defecto solo muestra el plan. --apply es obligatorio para escribir.
# Nunca elimina archivos existentes; crea backup y reemplaza archivos uno a uno.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
USER_HOME="${HOME:?HOME must be set}"
MODE="plan"
PROVIDER="all"
WITH_SETTINGS="false"
WITH_LOCAL_SETTINGS="false"
WITH_HOOK="false"
WITH_GUIDES="false"
BACKUP_ROOT=""

usage() {
  cat <<'EOF'
Uso: bash install.sh [opciones]

Por defecto no modifica nada y muestra el plan.

  --apply                    aplicar cambios (requiere backup automático)
  --provider NAME            all|claude|codex|antigravity (por defecto: all)
  --home DIR                 raíz de usuario alternativa para pruebas
  --with-settings            copiar settings.json de Claude (revisar antes)
  --with-local-settings      copiar settings.local.json (no recomendado)
  --with-hook                copiar el hook de Claude (opt-in)
  --with-guides              copiar las guías globales a DIR
  --backup-dir DIR           directorio explícito para backups
  --help                     mostrar esta ayuda
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 2
}

note() {
  printf '%s\n' "$*"
}

while (($#)); do
  case "$1" in
    --apply) MODE="apply" ;;
    --provider)
      (($# >= 2)) || die "--provider requiere un valor"
      PROVIDER="$2"
      shift
      ;;
    --home)
      (($# >= 2)) || die "--home requiere un valor"
      USER_HOME="$2"
      shift
      ;;
    --with-settings) WITH_SETTINGS="true" ;;
    --with-local-settings) WITH_LOCAL_SETTINGS="true" ;;
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

case "$PROVIDER" in
  all|claude|codex|antigravity) ;;
  *) die "provider inválido: $PROVIDER" ;;
esac

[[ -d "$USER_HOME" ]] || die "la raíz de usuario no existe: $USER_HOME"
USER_HOME="$(cd "$USER_HOME" && pwd -P)"

if [[ "$MODE" == "plan" ]]; then
  note "MODO PLAN: no se escribirán archivos. Usa --apply para aplicar."
else
  if [[ -z "$BACKUP_ROOT" ]]; then
    BACKUP_ROOT="$USER_HOME/backups/agent-harness-pre-install-$(date +%Y%m%d-%H%M%S)"
  fi
  mkdir -p "$BACKUP_ROOT"
  note "Backup: $BACKUP_ROOT"
  {
    printf 'repo=%s\n' "$REPO_DIR"
    printf 'provider=%s\n' "$PROVIDER"
    printf 'date=%s\n' "$(date --iso-8601=seconds)"
  } > "$BACKUP_ROOT/manifest.txt"
fi

declare -A BACKED_UP=()

assert_safe_source() {
  local path="$1"
  [[ -e "$path" ]] || die "fuente ausente: $path"
  [[ ! -L "$path" ]] || die "no se siguen symlinks de la fuente: $path"
}

assert_safe_destination() {
  local path="$1"
  [[ ! -L "$path" ]] || die "destino symlink rechazado: $path"
}

backup_existing() {
  local dst="$1"
  local rel="$2"
  [[ -e "$dst" || -L "$dst" ]] || return 0
  assert_safe_destination "$dst"
  [[ -n "${BACKED_UP[$dst]+yes}" ]] && return 0
  BACKED_UP["$dst"]=1
  local backup_path="$BACKUP_ROOT/$rel"
  mkdir -p "$(dirname "$backup_path")"
  cp -a -- "$dst" "$backup_path"
  printf 'backup: %s -> %s\n' "$dst" "$backup_path" >> "$BACKUP_ROOT/manifest.txt"
}

copy_file() {
  local src="$1"
  local dst="$2"
  local rel="$3"
  assert_safe_source "$src"
  [[ -f "$src" ]] || die "solo se copian archivos regulares: $src"
  assert_safe_destination "$dst"
  if [[ "$MODE" == "plan" ]]; then
    note "plan: $src -> $dst"
    return 0
  fi
  backup_existing "$dst" "$rel"
  mkdir -p "$(dirname "$dst")"
  local tmp
  tmp="$(mktemp "$(dirname "$dst")/.agent-harness-copy.XXXXXX")"
  cp --preserve=mode,timestamps -- "$src" "$tmp"
  mv -T -- "$tmp" "$dst"
  sha256sum "$dst" >> "$BACKUP_ROOT/manifest.txt"
  note "instalado: $dst"
}

copy_tree() {
  local src_root="$1"
  local dst_root="$2"
  local rel_prefix="$3"
  assert_safe_source "$src_root"
  [[ -d "$src_root" ]] || die "fuente no es directorio: $src_root"
  if find -P "$src_root" -type l -print -quit | grep -q .; then
    die "la fuente contiene symlinks y se rechaza: $src_root"
  fi
  while IFS= read -r -d '' src; do
    local rel="${src#"$src_root"/}"
    copy_file "$src" "$dst_root/$rel" "$rel_prefix/$rel"
  done < <(find -P "$src_root" -type f -print0 | sort -z)
}

copy_shared_skills() {
  local provider="$1"
  local target="$2"
  copy_tree "$REPO_DIR/skills" "$target/skills" "$provider/skills"
  copy_file "$REPO_DIR/router/SKILL.md" "$target/skills/task-router/SKILL.md" "${provider}/skills/task-router/SKILL.md"
}

# Claude conserva los agentes adaptativos y las skills.
if [[ "$PROVIDER" == "all" || "$PROVIDER" == "claude" ]]; then
  note "[claude] agentes adaptativos + skills"
  copy_tree "$REPO_DIR/agents" "$USER_HOME/.claude/agents" "claude/agents"
  copy_shared_skills "claude" "$USER_HOME/.claude"
fi

# Codex recibe la guía global y skills bajo demanda; no se impone la jerarquía
# de Claude en ~/.codex/agents. Los archivos antiguos no se eliminan.
if [[ "$PROVIDER" == "all" || "$PROVIDER" == "codex" ]]; then
  note "[codex] skills compartidas; sin jerarquía obligatoria"
  copy_shared_skills "codex" "$USER_HOME/.codex"
fi

# Antigravity/Gemini descubre Open Skills desde ~/.agents/skills. El wrapper
# local observado es agy; no se presupone un runtime específico adicional.
if [[ "$PROVIDER" == "all" || "$PROVIDER" == "antigravity" ]]; then
  note "[antigravity] Open Skills globales en ~/.agents/skills"
  copy_tree "$REPO_DIR/skills" "$USER_HOME/.agents/skills" "antigravity/skills"
  copy_file "$REPO_DIR/router/SKILL.md" "$USER_HOME/.agents/skills/task-router/SKILL.md" "antigravity/skills/task-router/SKILL.md"
fi

if [[ "$WITH_SETTINGS" == "true" ]]; then
  [[ "$PROVIDER" == "all" || "$PROVIDER" == "claude" ]] || die "settings solo aplica al provider claude"
  note "ADVERTENCIA: settings.json puede activar hooks/configuración global; revisa el backup y el diff."
  copy_file "$REPO_DIR/settings.json" "$USER_HOME/.claude/settings.json" "claude/settings.json"
fi
if [[ "$WITH_LOCAL_SETTINGS" == "true" ]]; then
  [[ "$WITH_SETTINGS" == "true" ]] || die "--with-local-settings requiere --with-settings"
  note "ADVERTENCIA: settings.local.json es específico de máquina; se copia solo por petición explícita."
  copy_file "$REPO_DIR/settings.local.json" "$USER_HOME/.claude/settings.local.json" "claude/settings.local.json"
fi
if [[ "$WITH_HOOK" == "true" ]]; then
  [[ "$PROVIDER" == "all" || "$PROVIDER" == "claude" ]] || die "hook solo aplica al provider claude"
  note "ADVERTENCIA: hook opt-in; no se activa ninguna referencia adicional automáticamente."
  copy_file "$REPO_DIR/hooks/precompact-memory.sh" "$USER_HOME/.claude/hooks/precompact-memory.sh" "claude/hooks/precompact-memory.sh"
  if [[ "$MODE" == "apply" ]]; then
    chmod 0755 "$USER_HOME/.claude/hooks/precompact-memory.sh"
  fi
fi
if [[ "$WITH_GUIDES" == "true" ]]; then
  for guide in AGENTS.md CLAUDE.md CODEX.md; do
    [[ -f "$REPO_DIR/$guide" ]] || continue
    copy_file "$REPO_DIR/$guide" "$USER_HOME/$guide" "guides/$guide"
  done
fi

if [[ "$MODE" == "plan" ]]; then
  note "Plan terminado. No se modificó el sistema."
else
  note "Instalación aplicada sin eliminar archivos existentes."
  note "Para deshacer: conserva $BACKUP_ROOT y restaura solo los destinos revisados."
fi
