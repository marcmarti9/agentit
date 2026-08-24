#!/usr/bin/env bash
# Despliegue reversible y separado por proveedor.
# Por defecto solo muestra el plan. --apply es obligatorio para escribir.
# Nunca elimina archivos existentes salvo con --prune-on-demand; incluso esa
# opción exige copia exacta del repositorio, backup y --apply explícito.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
USER_HOME="${HOME:?HOME must be set}"
MODE="plan"
PROVIDER="all"
WITH_SETTINGS="false"
WITH_LOCAL_SETTINGS="false"
WITH_HOOK="false"
WITH_GUIDES="false"
PRUNE_ON_DEMAND="false"
BACKUP_ROOT=""
CODEX_AGENT_PROFILES=("luna-worker.toml" "terra-worker.toml")
CORE_SKILLS=()
ON_DEMAND_SKILLS=()
declare -A CORE_SKILL_SET=()

usage() {
  cat <<'EOF'
Uso: bash install.sh [opciones]

Por defecto no modifica nada y muestra el plan.

  --apply                    aplicar cambios (requiere backup automático)
  --provider NAME            all|claude|codex|antigravity (por defecto: all)
  --home DIR                 raíz de usuario alternativa para pruebas
  --with-settings            copiar settings.json de Claude (revisar antes)
  --with-local-settings      copiar la plantilla local explícita a settings.local.json (no recomendado)
  --with-hook                copiar el hook de Claude (opt-in)
  --with-guides              copiar las guías globales a DIR
  --prune-on-demand          retirar copias Agentit exactas fuera de core
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
    --prune-on-demand) PRUNE_ON_DEMAND="true" ;;
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
[[ "$WITH_SETTINGS" == "false" || "$PROVIDER" == "all" || "$PROVIDER" == "claude" ]] || \
  die "settings solo aplica al provider claude"
[[ "$WITH_LOCAL_SETTINGS" == "false" || "$WITH_SETTINGS" == "true" ]] || \
  die "--with-local-settings requiere --with-settings"
[[ "$WITH_HOOK" == "false" || "$PROVIDER" == "all" || "$PROVIDER" == "claude" ]] || \
  die "hook solo aplica al provider claude"

[[ -d "$USER_HOME" ]] || die "la raíz de usuario no existe: $USER_HOME"
[[ ! -L "$USER_HOME" ]] || die "la raíz de usuario symlink se rechaza: $USER_HOME"
USER_HOME="$(cd "$USER_HOME" && pwd -P)"

load_global_skills() {
  local listed_skills skill
  listed_skills="$(python3 "$REPO_DIR/router/profiles.py" \
    --repo-root "$REPO_DIR" --profile core --format ids)" || \
    die "no se pudo cargar el perfil global core; instala Python 3 y PyYAML"
  while IFS= read -r skill; do
    [[ -n "$skill" ]] || continue
    [[ "$skill" =~ ^[a-z0-9][a-z0-9-]*$ ]] || die "id de skill inválido en core: $skill"
    [[ -f "$REPO_DIR/skills/$skill/SKILL.md" ]] || \
      die "skill del perfil core no encontrada: $skill"
    CORE_SKILLS+=("$skill")
    CORE_SKILL_SET["$skill"]=1
  done <<< "$listed_skills"
  ((${#CORE_SKILLS[@]} > 0)) || die "el perfil global core no contiene skills"
}

load_global_skills

load_on_demand_skills() {
  local listed_skills skill
  listed_skills="$(python3 "$REPO_DIR/router/profiles.py" \
    --repo-root "$REPO_DIR" --profile all --format ids)" || \
    die "no se pudo cargar el perfil all para la poda segura"
  while IFS= read -r skill; do
    [[ -n "$skill" ]] || continue
    if [[ -z "${CORE_SKILL_SET[$skill]+yes}" ]]; then
      ON_DEMAND_SKILLS+=("$skill")
    fi
  done <<< "$listed_skills"
}

load_on_demand_skills

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

assert_safe_directory_path() {
  local current="$1"
  assert_no_symlink_components "$current"
  while [[ "$current" != "/" && "$current" != "." && -n "$current" ]]; do
    if [[ -e "$current" || -L "$current" ]]; then
      [[ -d "$current" && ! -L "$current" ]] || \
        die "componente existente no es un directorio seguro: $current"
    fi
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

declare -A BACKED_UP=()

assert_safe_source() {
  local path="$1"
  assert_no_symlink_components "$path"
  [[ -e "$path" ]] || die "fuente ausente: $path"
}

assert_safe_destination() {
  local path="$1"
  assert_no_symlink_components "$path"
  assert_safe_directory_path "$(dirname -- "$path")"
}

backup_existing() {
  local dst="$1"
  local rel="$2"
  assert_manifest_path "$dst"
  [[ -e "$dst" || -L "$dst" ]] || return 0
  assert_safe_destination "$dst"
  [[ -f "$dst" ]] || die "destino existente no es un archivo regular: $dst"
  [[ -n "${BACKED_UP[$dst]+yes}" ]] && return 0
  BACKED_UP["$dst"]=1
  local backup_path="$BACKUP_ROOT/$rel"
  assert_manifest_path "$backup_path"
  assert_no_symlink_components "$backup_path"
  [[ ! -e "$backup_path" && ! -L "$backup_path" ]] || die "destino de backup ya existe: $backup_path"
  local original_mode
  original_mode="$(stat -c '%a' -- "$dst")"
  (umask 077; mkdir -p "$(dirname "$backup_path")")
  (umask 077; cp --preserve=timestamps -- "$dst" "$backup_path")
  chmod 0600 "$backup_path"
  printf 'backup path=%s destination=%s original_mode=%s original_sha256=%s backup_sha256=%s\n' \
    "$backup_path" "$dst" "$original_mode" "$(sha256sum -- "$dst" | awk '{print $1}')" \
    "$(sha256sum -- "$backup_path" | awk '{print $1}')" >> "$BACKUP_ROOT/manifest.txt"
}

copy_file() {
  local src="$1"
  local dst="$2"
  local rel="$3"
  assert_manifest_path "$src"
  assert_manifest_path "$dst"
  assert_safe_source "$src"
  [[ -f "$src" ]] || die "solo se copian archivos regulares: $src"
  assert_safe_destination "$dst"
  if [[ -e "$dst" || -L "$dst" ]]; then
    [[ -f "$dst" && ! -L "$dst" ]] || \
      die "destino existente no es un archivo regular: $dst"
  fi
  if [[ "$MODE" == "plan" ]]; then
    note "plan: $src -> $dst"
    return 0
  fi
  local before_state="absent"
  [[ -e "$dst" ]] && before_state="present"
  local source_hash
  source_hash="$(sha256sum -- "$src" | awk '{print $1}')"
  backup_existing "$dst" "$rel"
  mkdir -p "$(dirname "$dst")"
  local tmp
  tmp="$(mktemp "$(dirname "$dst")/.agentit-copy.XXXXXX")"
  cp --preserve=mode,timestamps -- "$src" "$tmp"
  mv -T -- "$tmp" "$dst"
  printf 'copy source=%s destination=%s before_state=%s source_sha256=%s backup=%s destination_sha256=%s\n' \
    "$src" "$dst" "$before_state" "$source_hash" \
    "$([[ "$before_state" == "present" ]] && printf '%s' "$BACKUP_ROOT/$rel" || printf '%s' none)" \
    "$(sha256sum -- "$dst" | awk '{print $1}')" >> "$BACKUP_ROOT/manifest.txt"
  note "instalado: $dst"
}

copy_codex_agent_profiles() {
  local target_root="$1"
  local profile_name
  for profile_name in "${CODEX_AGENT_PROFILES[@]}"; do
    copy_file \
      "$REPO_DIR/.codex/agents/$profile_name" \
      "$target_root/agents/$profile_name" \
      "codex/agents/$profile_name"
  done
}

copy_tree() {
  local src_root="$1"
  local dst_root="$2"
  local rel_prefix="$3"
  assert_safe_source "$src_root"
  [[ -d "$src_root" ]] || die "fuente no es directorio: $src_root"
  local symlink_path
  if ! symlink_path="$(find -P "$src_root" -type l -print -quit)"; then
    die "no se pudo inspeccionar symlinks de la fuente: $src_root"
  fi
  [[ -z "$symlink_path" ]] || die "la fuente contiene symlinks y se rechaza: $src_root"
  local file_list
  file_list="$(mktemp /tmp/agentit-install-find.XXXXXX)"
  if ! find -P "$src_root" -type f -print0 > "$file_list"; then
    rm -f -- "$file_list"
    die "no se pudo enumerar completamente la fuente: $src_root"
  fi
  while IFS= read -r -d '' src; do
    local rel="${src#"$src_root"/}"
    copy_file "$src" "$dst_root/$rel" "$rel_prefix/$rel"
  done < "$file_list"
  rm -f -- "$file_list"
}

copy_shared_skills() {
  local provider="$1"
  local target="$2"
  local skill
  for skill in "${CORE_SKILLS[@]}"; do
    copy_tree "$REPO_DIR/skills/$skill" "$target/skills/$skill" "$provider/skills/$skill"
  done
}

preflight_prune_on_demand() {
  local provider="$1"
  local target="$2"
  local skill destination extra
  for skill in "${ON_DEMAND_SKILLS[@]}"; do
    destination="$target/skills/$skill/SKILL.md"
    [[ -e "$destination" || -L "$destination" ]] || continue
    assert_manifest_path "$destination"
    assert_safe_destination "$destination"
    [[ -f "$destination" && ! -L "$destination" ]] || \
      die "no se puede podar un destino no regular: $destination"
    cmp -s "$REPO_DIR/skills/$skill/SKILL.md" "$destination" || \
      die "se rechaza podar una skill modificada: $destination"
    extra="$(find -P "$(dirname -- "$destination")" -mindepth 1 -maxdepth 1 \
      ! -name SKILL.md -print -quit)"
    [[ -z "$extra" ]] || die "se rechaza podar una skill con archivos extra: $extra"
    note "plan: prune $destination ($provider)"
  done
}

prune_on_demand() {
  local provider="$1"
  local target="$2"
  local skill destination
  for skill in "${ON_DEMAND_SKILLS[@]}"; do
    destination="$target/skills/$skill/SKILL.md"
    [[ -e "$destination" || -L "$destination" ]] || continue
    assert_safe_destination "$destination"
    [[ -f "$destination" && ! -L "$destination" ]] || \
      die "la skill cambió a un destino no regular; se detiene: $destination"
    cmp -s "$REPO_DIR/skills/$skill/SKILL.md" "$destination" || \
      die "la skill cambió después del preflight; se detiene: $destination"
    backup_existing "$destination" "$provider/skills/$skill/SKILL.md"
    rm -f -- "$destination"
    rmdir -- "$(dirname -- "$destination")" 2>/dev/null || true
    note "retirada: $destination"
  done
}

preflight_copy_file() {
  local src="$1"
  local dst="$2"
  assert_manifest_path "$src"
  assert_manifest_path "$dst"
  assert_safe_source "$src"
  [[ -f "$src" ]] || die "solo se copian archivos regulares: $src"
  assert_safe_destination "$dst"
  if [[ -e "$dst" || -L "$dst" ]]; then
    [[ -f "$dst" && ! -L "$dst" ]] || \
      die "destino existente no es un archivo regular: $dst"
  fi
}

preflight_copy_codex_agent_profiles() {
  local target_root="$1"
  local profile_name
  for profile_name in "${CODEX_AGENT_PROFILES[@]}"; do
    preflight_copy_file \
      "$REPO_DIR/.codex/agents/$profile_name" \
      "$target_root/agents/$profile_name"
  done
}

preflight_copy_tree() {
  local src_root="$1"
  local dst_root="$2"
  assert_safe_source "$src_root"
  [[ -d "$src_root" ]] || die "fuente no es directorio: $src_root"

  local -a source_symlinks=()
  find -P "$src_root" -type l -print0 > /dev/null || \
    die "no se pudo inspeccionar symlinks de la fuente: $src_root"
  mapfile -d '' -n 1 source_symlinks < <(find -P "$src_root" -type l -print0)
  ((${#source_symlinks[@]} == 0)) || \
    die "la fuente contiene symlinks y se rechaza: $src_root"

  local -a source_files=()
  find -P "$src_root" -type f -print0 > /dev/null || \
    die "no se pudo enumerar completamente la fuente: $src_root"
  mapfile -d '' source_files < <(find -P "$src_root" -type f -print0)
  local src
  for src in "${source_files[@]}"; do
    local rel="${src#"$src_root"/}"
    preflight_copy_file "$src" "$dst_root/$rel"
  done
}

preflight_shared_skills() {
  local target="$1"
  local skill
  for skill in "${CORE_SKILLS[@]}"; do
    preflight_copy_tree "$REPO_DIR/skills/$skill" "$target/skills/$skill"
  done
}

preflight_install() {
  if [[ "$PROVIDER" == "all" || "$PROVIDER" == "claude" ]]; then
    preflight_copy_tree "$REPO_DIR/agents" "$USER_HOME/.claude/agents"
    preflight_shared_skills "$USER_HOME/.claude"
  fi
  if [[ "$PROVIDER" == "all" || "$PROVIDER" == "codex" ]]; then
    preflight_shared_skills "$USER_HOME/.codex"
    preflight_copy_codex_agent_profiles "$USER_HOME/.codex"
  fi
  if [[ "$PROVIDER" == "all" || "$PROVIDER" == "antigravity" ]]; then
    preflight_shared_skills "$USER_HOME/.agents"
  fi
  if [[ "$PRUNE_ON_DEMAND" == "true" ]]; then
    if [[ "$PROVIDER" == "all" || "$PROVIDER" == "claude" ]]; then
      preflight_prune_on_demand "claude" "$USER_HOME/.claude"
    fi
    if [[ "$PROVIDER" == "all" || "$PROVIDER" == "codex" ]]; then
      preflight_prune_on_demand "codex" "$USER_HOME/.codex"
    fi
    if [[ "$PROVIDER" == "all" || "$PROVIDER" == "antigravity" ]]; then
      preflight_prune_on_demand "antigravity" "$USER_HOME/.agents"
    fi
  fi
  if [[ "$WITH_SETTINGS" == "true" ]]; then
    preflight_copy_file "$REPO_DIR/settings.json" "$USER_HOME/.claude/settings.json"
  fi
  if [[ "$WITH_LOCAL_SETTINGS" == "true" ]]; then
    preflight_copy_file "$REPO_DIR/templates/claude/settings.local.example.json" "$USER_HOME/.claude/settings.local.json"
  fi
  if [[ "$WITH_HOOK" == "true" ]]; then
    preflight_copy_file "$REPO_DIR/hooks/precompact-memory.sh" "$USER_HOME/.claude/hooks/precompact-memory.sh"
  fi
  if [[ "$WITH_GUIDES" == "true" ]]; then
    local -a guides=()
    case "$PROVIDER" in
      claude) guides=(AGENTS.md CLAUDE.md) ;;
      codex) guides=(AGENTS.md CODEX.md) ;;
      antigravity) guides=(AGENTS.md) ;;
      all) guides=(AGENTS.md CLAUDE.md CODEX.md) ;;
    esac
    local guide
    for guide in "${guides[@]}"; do
      [[ -f "$REPO_DIR/$guide" ]] || continue
      preflight_copy_file "$REPO_DIR/$guide" "$USER_HOME/$guide"
    done
  fi
}

preflight_install

if [[ "$MODE" == "plan" ]]; then
  note "MODO PLAN: no se escribirán archivos. Usa --apply para aplicar."
else
  if [[ -z "$BACKUP_ROOT" ]]; then
    BACKUP_ROOT="$USER_HOME/backups/agentit-pre-install-$(date +%Y%m%d-%H%M%S)"
  fi
  assert_manifest_path "$REPO_DIR"
  assert_manifest_path "$BACKUP_ROOT"
  assert_safe_directory_path "$BACKUP_ROOT"
  [[ ! -e "$BACKUP_ROOT" && ! -L "$BACKUP_ROOT" ]] || \
    die "la raíz de backup debe ser nueva: $BACKUP_ROOT"
  manifest_path="$BACKUP_ROOT/manifest.txt"
  assert_manifest_path "$manifest_path"
  assert_no_symlink_components "$manifest_path"
  [[ ! -e "$manifest_path" && ! -L "$manifest_path" ]] || \
    die "manifest ya existe; se rechaza sobrescribirlo: $manifest_path"
  (umask 077; mkdir -p "$BACKUP_ROOT")
  [[ -O "$BACKUP_ROOT" ]] || die "backup no pertenece al usuario actual: $BACKUP_ROOT"
  chmod 0700 "$BACKUP_ROOT"
  create_manifest "$manifest_path"
  note "Backup: $BACKUP_ROOT"
  {
    printf 'repo=%s\n' "$REPO_DIR"
    printf 'provider=%s\n' "$PROVIDER"
    printf 'date=%s\n' "$(date --iso-8601=seconds)"
  } >> "$manifest_path"
fi

if [[ "$PRUNE_ON_DEMAND" == "true" && "$MODE" == "apply" ]]; then
  if [[ "$PROVIDER" == "all" || "$PROVIDER" == "claude" ]]; then
    prune_on_demand "claude" "$USER_HOME/.claude"
  fi
  if [[ "$PROVIDER" == "all" || "$PROVIDER" == "codex" ]]; then
    prune_on_demand "codex" "$USER_HOME/.codex"
  fi
  if [[ "$PROVIDER" == "all" || "$PROVIDER" == "antigravity" ]]; then
    prune_on_demand "antigravity" "$USER_HOME/.agents"
  fi
fi

# Claude conserva los agentes adaptativos y el perfil global core. Los demás
# cuerpos permanecen en el repositorio y se activan bajo demanda por proyecto.
if [[ "$PROVIDER" == "all" || "$PROVIDER" == "claude" ]]; then
  note "[claude] agentes adaptativos + perfil global core"
  copy_tree "$REPO_DIR/agents" "$USER_HOME/.claude/agents" "claude/agents"
  copy_shared_skills "claude" "$USER_HOME/.claude"
fi

# Codex recibe solo el perfil global core y los workers portables; no se impone
# la jerarquía de Claude en ~/.codex/agents. Los archivos antiguos no se eliminan.
if [[ "$PROVIDER" == "all" || "$PROVIDER" == "codex" ]]; then
  note "[codex] perfil global core; sin jerarquía obligatoria"
  copy_shared_skills "codex" "$USER_HOME/.codex"
  copy_codex_agent_profiles "$USER_HOME/.codex"
fi

# Antigravity/Gemini descubre Open Skills desde ~/.agents/skills; no se
# presupone un wrapper ni un runtime específico adicional.
if [[ "$PROVIDER" == "all" || "$PROVIDER" == "antigravity" ]]; then
  note "[antigravity] perfil global core en ~/.agents/skills"
  copy_shared_skills "antigravity" "$USER_HOME/.agents"
fi

if [[ "$WITH_SETTINGS" == "true" ]]; then
  note "ADVERTENCIA: settings.json puede activar hooks/configuración global; revisa el backup y el diff."
  copy_file "$REPO_DIR/settings.json" "$USER_HOME/.claude/settings.json" "claude/settings.json"
fi
if [[ "$WITH_LOCAL_SETTINGS" == "true" ]]; then
  note "ADVERTENCIA: la plantilla settings.local.example.json se copia a estado local solo por petición explícita."
  copy_file "$REPO_DIR/templates/claude/settings.local.example.json" "$USER_HOME/.claude/settings.local.json" "claude/settings.local.json"
fi
if [[ "$WITH_HOOK" == "true" ]]; then
  note "ADVERTENCIA: hook opt-in; no se activa ninguna referencia adicional automáticamente."
  copy_file "$REPO_DIR/hooks/precompact-memory.sh" "$USER_HOME/.claude/hooks/precompact-memory.sh" "claude/hooks/precompact-memory.sh"
  if [[ "$MODE" == "apply" ]]; then
    chmod 0755 "$USER_HOME/.claude/hooks/precompact-memory.sh"
  fi
fi
if [[ "$WITH_GUIDES" == "true" ]]; then
  case "$PROVIDER" in
    claude) guides=(AGENTS.md CLAUDE.md) ;;
    codex) guides=(AGENTS.md CODEX.md) ;;
    antigravity) guides=(AGENTS.md) ;;
    all) guides=(AGENTS.md CLAUDE.md CODEX.md) ;;
  esac
  for guide in "${guides[@]}"; do
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
