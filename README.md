# claude-config

Configuración personal de Claude Code (agentes, settings, hooks, skills),
sincronizada entre mis máquinas vía este repo privado.

## Qué incluye

- `agents/` — jerarquía de agentes personalizada (architect, orchestrator,
  supervisor, worker, auditor) que reemplaza el flujo por defecto.
- `settings.json` — configuración global de `~/.claude/settings.json`
  (modelo, hooks, persistencia de sesiones, etc.).
- `settings.local.json` — overrides menores de permisos.
- `hooks/precompact-memory.sh` — hook `PreCompact` que, antes de que el
  contexto se compacte, usa un `claude -p` headless con Haiku para
  actualizar la memoria del proyecto con lo imprescindible para retomar
  el trabajo sin fricción.
- `skills/supabase-postgres-best-practices/` — skill personal.

## Qué NO incluye (deliberado)

Nunca se sincroniza nada de esto — vive solo en cada máquina:

- `.credentials.json`, tokens, `daemon*` — credenciales/estado de sesión.
- `history.jsonl`, `projects/`, `sessions/` — transcripciones y memoria
  auto-generada por proyecto (contienen conversaciones reales).
- `cache/`, `plugins/`, `telemetry/`, `stats-cache.json`, etc. — cachés
  regenerables, no configuración.

## Instalar en una máquina nueva

```bash
git clone https://github.com/<tu-usuario>/claude-config.git ~/claude-config
cd ~/claude-config
bash install.sh
```

Esto copia todo a `~/.claude/`, haciendo antes una copia de seguridad de lo
que hubiera en `~/.claude/backups/pre-install-<fecha>/`. **Sobrescribe
`settings.json` entero** — si esa máquina tenía algo específico ahí (una
env var local, un plugin propio de esa máquina), revísalo después con
`git diff` antes de confiar ciegamente.

## Actualizar el repo tras cambiar algo localmente

Cuando edites un agente, `settings.json`, etc. directamente en
`~/.claude/` de cualquier máquina:

```bash
cd ~/claude-config
bash update.sh      # copia ~/.claude/ -> este repo
git diff             # revisa qué cambió
git add -A && git commit -m "..." && git push
```

Y en la otra máquina, para traer esos cambios:

```bash
cd ~/claude-config
git pull
bash install.sh
```

No hay sincronización automática — es intencionadamente manual (pull +
install), para no arriesgarte a que un cambio a medias en una máquina se
propague solo a la otra.
