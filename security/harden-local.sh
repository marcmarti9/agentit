#!/usr/bin/env bash
# Hardening local, reversible y sin leer valores de credenciales.
# Por defecto muestra el plan; --apply hace cambios y crea backup.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
USER_HOME="${HOME:?HOME must be set}"
MODE="plan"
BACKUP_ROOT=""

usage() {
  cat <<'EOF'
Uso: bash security/harden-local.sh [--apply] [--home DIR] [--backup-dir DIR]

Acciones:
  - comenta aliases conocidos que desactivan permisos/sandbox;
  - fija ~/.bashrc y ficheros Cursor mcp_auth.json a modo 600;
  - no lee ni imprime valores de secretos;
  - no cambia ANTHROPIC_BASE_URL, tokens, providers ni workspaces confiados.
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 2
}

while (($#)); do
  case "$1" in
    --apply) MODE="apply" ;;
    --home)
      (($# >= 2)) || die "--home requiere un valor"
      USER_HOME="$2"
      shift
      ;;
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

[[ -d "$USER_HOME" ]] || die "HOME inexistente: $USER_HOME"
[[ ! -L "$USER_HOME" ]] || die "se rechaza HOME symlink: $USER_HOME"
USER_HOME="$(cd "$USER_HOME" && pwd -P)"
[[ -f "$USER_HOME/.bashrc" ]] || die "no existe .bashrc en $USER_HOME"
[[ ! -L "$USER_HOME/.bashrc" ]] || die "se rechaza .bashrc symlink"

assert_no_symlink_components() {
  local current="$1"
  while [[ "$current" != "/" && "$current" != "." && -n "$current" ]]; do
    [[ ! -L "$current" ]] || die "componente symlink rechazado: $current"
    current="$(dirname -- "$current")"
  done
}

create_manifest() {
  local path="$1"
  assert_no_symlink_components "$path"
  [[ ! -e "$path" && ! -L "$path" ]] || die "manifest ya existe; se rechaza sobrescribirlo: $path"
  (set -o noclobber; : > "$path") || die "no se pudo crear manifest de forma exclusiva: $path"
}

if [[ "$MODE" == "apply" ]]; then
  if [[ -z "$BACKUP_ROOT" ]]; then
    BACKUP_ROOT="$USER_HOME/backups/agent-harness-local-hardening-$(date +%Y%m%d-%H%M%S)"
  fi
  assert_no_symlink_components "$BACKUP_ROOT"
  mkdir -p "$BACKUP_ROOT"
  create_manifest "$BACKUP_ROOT/manifest.txt"
  printf 'date=%s\n' "$(date --iso-8601=seconds)" >> "$BACKUP_ROOT/manifest.txt"
fi

backup_file() {
  local src="$1"
  local rel="${src#"$USER_HOME"/}"
  [[ ! -L "$src" ]] || die "se rechaza symlink: $src"
  local dst="$BACKUP_ROOT/$rel"
  assert_no_symlink_components "$dst"
  [[ ! -e "$dst" && ! -L "$dst" ]] || die "destino de backup ya existe: $dst"
  mkdir -p "$(dirname "$dst")"
  cp --preserve=mode,timestamps -- "$src" "$dst"
  sha256sum "$src" >> "$BACKUP_ROOT/manifest.txt"
}

if grep -Eq '^alias (clauded|agyd|codexd)=' "$USER_HOME/.bashrc"; then
  if [[ "$MODE" == "plan" ]]; then
    printf 'plan: comentar aliases bypass en %s\n' "$USER_HOME/.bashrc"
  else
    backup_file "$USER_HOME/.bashrc"
    tmp="$(mktemp "$USER_HOME/.bashrc.agent-harness.XXXXXX")"
    awk '
      /^alias (clauded|agyd|codexd)=/ {
        print "# disabled by agents-config security/harden-local.sh: " $0
        next
      }
      { print }
    ' "$USER_HOME/.bashrc" > "$tmp"
    mv -T -- "$tmp" "$USER_HOME/.bashrc"
    chmod 0600 "$USER_HOME/.bashrc"
    printf 'hardening: aliases bypass comentados; .bashrc mode=600\n'
  fi
else
  printf 'ok: no hay aliases bypass activos\n'
  if [[ "$MODE" == "apply" ]]; then
    backup_file "$USER_HOME/.bashrc"
    chmod 0600 "$USER_HOME/.bashrc"
  fi
fi

auth_files=()
auth_root="$USER_HOME/.cursor"
if [[ -e "$auth_root" && ! -d "$auth_root" ]]; then
  die "~/.cursor existe pero no es un directorio"
fi
if [[ -L "$auth_root" ]]; then
  die "se rechaza ~/.cursor symlink"
fi
auth_list=""
if [[ -d "$auth_root" ]]; then
  symlink_path="$(find -P "$auth_root" -type l -print -quit)" || die "no se pudo inspeccionar symlinks de ~/.cursor; no se aplica hardening"
  [[ -z "$symlink_path" ]] || die "se rechazan symlinks bajo ~/.cursor"
  auth_list_file="$(mktemp /tmp/agent-harness-cursor-find.XXXXXX)"
  if ! find -P "$auth_root" -type f -name 'mcp_auth.json' -print0 > "$auth_list_file"; then
    rm -f -- "$auth_list_file"
    die "no se pudo inspeccionar ~/.cursor; no se aplica hardening"
  fi
  if ! mapfile -d '' auth_files < "$auth_list_file"; then
    rm -f -- "$auth_list_file"
    die "no se pudo leer la lista de ~/.cursor; no se aplica hardening"
  fi
  rm -f -- "$auth_list_file"
fi
if ((${#auth_files[@]} == 0)); then
  printf 'ok: no se encontraron mcp_auth.json bajo .cursor\n'
else
  for auth_file in "${auth_files[@]}"; do
    [[ "$auth_file" != *$'\n'* ]] || die "ruta MCP con salto de línea rechazada"
    [[ ! -L "$auth_file" ]] || die "se rechaza symlink: $auth_file"
    if [[ "$MODE" == "plan" ]]; then
      printf 'plan: mode 600 %s\n' "${auth_file#"$USER_HOME"/}"
    else
      backup_file "$auth_file"
      chmod 0600 "$auth_file"
    fi
  done
fi

if [[ "$MODE" == "plan" ]]; then
  printf 'Plan terminado. No se modificó el HOME.\n'
else
  printf 'Hardening aplicado; backup: %s\n' "$BACKUP_ROOT"
fi
