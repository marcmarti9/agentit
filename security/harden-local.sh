#!/usr/bin/env bash
# Hardening local y reversible; no analiza ni imprime valores de credenciales.
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
  - no analiza ni imprime valores de secretos; calcula hashes de los archivos;
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

assert_manifest_path() {
  local path="$1"
  [[ "$path" != *$'\n'* && "$path" != *$'\r'* ]] || \
    die "ruta con CR/LF rechazada para manifest"
}

assert_no_symlink_components() {
  local current="$1"
  while [[ "$current" != "/" && "$current" != "." && -n "$current" ]]; do
    [[ ! -L "$current" ]] || die "componente symlink rechazado: $current"
    current="$(dirname -- "$current")"
  done
}

create_manifest() {
  local path="$1"
  assert_manifest_path "$path"
  assert_no_symlink_components "$path"
  [[ ! -e "$path" && ! -L "$path" ]] || die "manifest ya existe; se rechaza sobrescribirlo: $path"
  (umask 077; set -o noclobber; : > "$path") || die "no se pudo crear manifest de forma exclusiva: $path"
}

assert_manifest_path "$USER_HOME/.bashrc"

auth_files=()
auth_root="$USER_HOME/.cursor"
assert_manifest_path "$auth_root"
if [[ -e "$auth_root" && ! -d "$auth_root" ]]; then
  die "~/.cursor existe pero no es un directorio"
fi
if [[ -L "$auth_root" ]]; then
  die "se rechaza ~/.cursor symlink"
fi
if [[ -d "$auth_root" ]]; then
  assert_no_symlink_components "$auth_root"
  symlink_list_file="$(mktemp /tmp/agent-harness-cursor-symlinks.XXXXXX)"
  if ! find -P "$auth_root" -type l -print0 > "$symlink_list_file"; then
    rm -f -- "$symlink_list_file"
    die "no se pudo inspeccionar symlinks de ~/.cursor; no se aplica hardening"
  fi
  if [[ -s "$symlink_list_file" ]]; then
    rm -f -- "$symlink_list_file"
    die "se rechazan symlinks bajo ~/.cursor"
  fi
  rm -f -- "$symlink_list_file"

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

  for auth_file in "${auth_files[@]}"; do
    assert_manifest_path "$auth_file"
    [[ "$auth_file" == "$auth_root/"* ]] || die "ruta MCP fuera de ~/.cursor rechazada"
    [[ -f "$auth_file" && ! -L "$auth_file" ]] || die "ruta MCP no es un archivo regular"
  done
fi

if [[ "$MODE" == "apply" ]]; then
  if [[ -z "$BACKUP_ROOT" ]]; then
    BACKUP_ROOT="$USER_HOME/backups/agent-harness-local-hardening-$(date +%Y%m%d-%H%M%S)"
  fi
  assert_manifest_path "$BACKUP_ROOT"
  assert_no_symlink_components "$BACKUP_ROOT"
  (umask 077; mkdir -p "$BACKUP_ROOT")
  [[ -O "$BACKUP_ROOT" ]] || die "backup no pertenece al usuario actual: $BACKUP_ROOT"
  chmod 0700 "$BACKUP_ROOT"
  create_manifest "$BACKUP_ROOT/manifest.txt"
  printf 'date=%s\n' "$(date --iso-8601=seconds)" >> "$BACKUP_ROOT/manifest.txt"
fi

backup_file() {
  local src="$1"
  local rel="${src#"$USER_HOME"/}"
  assert_manifest_path "$src"
  [[ ! -L "$src" ]] || die "se rechaza symlink: $src"
  [[ -f "$src" ]] || die "solo se respaldan archivos regulares: $src"
  local dst="$BACKUP_ROOT/$rel"
  assert_manifest_path "$dst"
  assert_no_symlink_components "$dst"
  [[ ! -e "$dst" && ! -L "$dst" ]] || die "destino de backup ya existe: $dst"
  local original_mode
  original_mode="$(stat -c '%a' -- "$src")"
  (umask 077; mkdir -p "$(dirname "$dst")")
  (umask 077; cp --preserve=timestamps -- "$src" "$dst")
  chmod 0600 "$dst"
  printf 'backup path=%s source=%s original_mode=%s original_sha256=%s backup_sha256=%s\n' \
    "$dst" "$src" "$original_mode" "$(sha256sum -- "$src" | awk '{print $1}')" \
    "$(sha256sum -- "$dst" | awk '{print $1}')" >> "$BACKUP_ROOT/manifest.txt"
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
  bashrc_mode="$(stat -c '%a' -- "$USER_HOME/.bashrc")"
  if [[ "$MODE" == "plan" && "$bashrc_mode" != "600" ]]; then
    printf 'plan: mode 600 %s\n' "$USER_HOME/.bashrc"
  elif [[ "$MODE" == "apply" && "$bashrc_mode" != "600" ]]; then
    backup_file "$USER_HOME/.bashrc"
    chmod 0600 "$USER_HOME/.bashrc"
  fi
fi

if ((${#auth_files[@]} == 0)); then
  printf 'ok: no se encontraron mcp_auth.json bajo .cursor\n'
else
  for auth_file in "${auth_files[@]}"; do
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
