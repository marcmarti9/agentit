# Inventario del harness local

**Fecha de evidencia:** 2026-08-03 (Europe/Madrid)
**Ámbito:** `/home/Marc`, con foco en Codex CLI, Claude Code, Antigravity/Gemini CLI, OpenCode y `/home/Marc/agents-config`.
**Regla de privacidad:** no se copiaron valores de secretos, cookies, tokens ni contenido de memorias; solo nombres, rutas, versiones, hashes y forma de configuración.

## Resumen ejecutivo

- El repositorio de trabajo es `/home/Marc/agents-config`, en la rama `feature/safe-context-harness-audit`, que integra `origin/main@eab20ca` sobre `main@4e6db85`.
- Codex, Claude Code, Gemini CLI, el wrapper local `agy` y OpenCode están instalados. No existe un ejecutable independiente llamado `antigravity`; el entrypoint Antigravity observado es `/home/Marc/.local/bin/agy`, mientras Gemini CLI está en `/home/Marc/.npm-global/bin/gemini`.
- Codex usa `gpt-5.6-luna` con razonamiento `max` en `/home/Marc/.codex/config.toml:1-3`. Claude usa `sonnet` en `/home/Marc/.claude/settings.json:5`; no se debe imponer el identificador de Luna a proveedores que no lo soporten.
- Claude conserva los cinco agentes adaptativos. Las copias antiguas de esos agentes en Codex y Antigravity fueron archivadas con backup; no se eliminaron.
- Addy Agent Skills está instalado como marketplace y sus skills se exponen globalmente mediante `.agents/skills`; `.claude/skills` contiene symlinks hacia esa colección. Hay copias adicionales y drift entre `.agents`, `.claude` y `.codex`.
- No hay MCP configurado en Codex ni Gemini, y no hay extensiones Gemini instaladas. Esto reduce superficie de ataque, aunque algunas skills anuncian dependencias MCP que no están disponibles.
- Cursor conserva seis `mcp_auth.json`, ahora con permisos `600`; solo se inspeccionó metadata y no se leyó ningún valor.
- `/home/Marc/.bashrc` conserva una variable con apariencia de credencial cuyo valor no se reproduce; los tres aliases bypass fueron comentados y el archivo quedó en modo `600`.
- OmniRoute `3.8.48` está instalado como paquete Node y contiene catálogo de compresión, pero `127.0.0.1:20128` no responde en la inspección. Su estado operativo es `UNKNOWN/NOT_RUNNING`, no `ACTIVE`.
- Antes de esta rama, `install.sh` sobrescribía destinos con `rm -rf` y copiaba settings/hooks sin una activación separada. La rama actual reemplaza ese comportamiento por plan por defecto, backups estructurados y allowlist.
- El 2026-08-03 se aplicó al HOME real el baseline de proveedor con `install.sh --apply --provider all --with-settings`. El backup está en `/home/Marc/backups/agent-harness-pre-install-20260803-160912`.
- Tras la aplicación, Claude tiene la arquitectura adaptativa y settings seguro; Codex tiene skills compartidas y `task-router`; Antigravity/Gemini descubre `task-router` desde `/home/Marc/.agents/skills`.

## Ejecutables y proveedores

| Elemento | Ruta | Versión observada | Estado | Notas |
|---|---|---:|---|---|
| Codex CLI | `/home/Marc/.local/bin/codex` | `0.146.0` | ACTIVE_GLOBAL | MCP: ninguno |
| Claude Code | `/home/Marc/.local/bin/claude` | `2.1.220` | ACTIVE_GLOBAL | hook PreCompact existente como artefacto, no referenciado |
| Gemini CLI / Antigravity | `/home/Marc/.npm-global/bin/gemini` | `0.47.0` | ACTIVE_GLOBAL | proyecto `/home/Marc` marcado no confiable para agents/hooks |
| Antigravity wrapper | `/home/Marc/.local/bin/agy` | por verificar | ACTIVE_GLOBAL | usa settings de `.gemini/antigravity-cli` |
| OpenCode | `/home/Marc/.opencode/bin/opencode` | `1.17.20` | AVAILABLE_ON_DEMAND | fuera del despliegue inicial |
| RTK | — | — | AVAILABLE_ON_DEMAND | no instalado como comando |
| Caveman | — | — | AVAILABLE_ON_DEMAND | no instalado como comando |
| Headroom | — | — | AVAILABLE_ON_DEMAND | no instalado como comando |
| tokless | — | — | AVAILABLE_ON_DEMAND | no instalado como comando |

## Rutas inspeccionadas

| Ruta | Tipo/estado | Evidencia y función |
|---|---|---|
| `/home/Marc/.codex` | global activo | `config.toml` y skills; agentes antiguos archivados |
| `/home/Marc/.claude` | global activo | settings, agentes, skills, plugins, hook y memorias |
| `/home/Marc/.gemini/antigravity-cli` | global disponible | settings; agentes antiguos archivados; discovery de skills en `.agents` |
| `/home/Marc/.agents` | global activo | 29 carpetas/66 archivos de skills; Gemini las descubre globalmente |
| `/home/Marc/.cursor` | existente | no se encontró una configuración de harness equivalente en el primer recorrido |
| `/home/Marc/.config`, `/home/Marc/.local/share` | existentes | inspeccionados como ubicaciones probables; sin activar rutas de compresión identificadas |
| `/home/Marc/.opencode` | existente | binario instalado; no integrado en el instalador inicial |
| `/home/Marc/.omniroute` | existente | configuración local potencial; no se asumió que el gateway estuviera activo |
| `/home/Marc/agents-config` | repositorio git | fuente canónica de esta implementación |
| `/home/Marc/code`, `/home/Marc/Digitem` | proyectos | contienen instrucciones por proyecto; no se modificaron |

## Configuración relevante

### Codex

`/home/Marc/.codex/config.toml:1-12` declara el modelo Luna Max y confianza en `/home/Marc`, `code/calydex` y `code/fullStack`. Esa confianza amplia debe tratarse como una decisión de seguridad independiente del ahorro de contexto.

### Claude Code

La configuración previa de `/home/Marc/.claude/settings.json` seleccionaba `architect`, permitía saltar el aviso de modo peligroso, activaba la subida automática de sesiones y registraba `PreCompact`; esas observaciones están conservadas como evidencia histórica en el backup de instalación. La versión actualmente aplicada mantiene profundidad de subagentes `2` y modelo `sonnet` en `:3-5`, conserva `agent: architect` en `:32`, fija `skipDangerousModePermissionPrompt: false` en `:33`, usa retención de 90 días, checkpoints y compactación automática en `:36-38`, fija `autoUploadSessions: false` en `:39` y no declara hooks.

El archivo local `/home/Marc/.claude/settings.local.json` solo se inventarió por forma; no se reportan sus valores. El actualizador seguro nunca lo importa.

### Gemini / Antigravity

`/home/Marc/.gemini/antigravity-cli/settings.json:2-10` selecciona `Gemini 3.6 Flash (High)` y confía en `/home/Marc` y varios proyectos. `gemini skills list` descubrió las skills globales de `/home/Marc/.agents/skills`, pero informó que los agents/hooks de proyecto se omiten porque `/home/Marc` no está confiable. `gemini mcp list` informó cero servidores y `gemini extensions list` cero extensiones.

## Agentes y skills duplicados

Los cinco agentes `architect`, `auditor`, `orchestrator`, `supervisor` y `worker` existen activamente en:

- `/home/Marc/agents-config/agents`
- `/home/Marc/.claude/agents`

Las copias antiguas de Codex y Antigravity están en `/home/Marc/backups/agent-harness-archive-old-provider-agents-20260803`, con manifiesto y hashes.

Los hashes del repositorio y de Claude coinciden en los cinco archivos durante la inspección. `architect-orchestrator` y `supabase-postgres-best-practices` también coinciden entre el repositorio y los destinos inspeccionados.

La colección Addy se encontró en `/home/Marc/.claude/plugins/marketplaces/addy-agent-skills` en el commit `7829ffd90d973b6325f5f12f1b1226dcace74443`. Sus copias expuestas mediante `.agents`, `.claude` y `.codex` no deben considerarse automáticamente una sola fuente: se observaron diferencias de hash entre algunas skills de TDD/incremental-implementation.

## Plugins y repositorios externos

Claude tiene instalados pero deshabilitados plugins oficiales, `pm-skills`, `security-guidance`, `supabase` y `superpowers 6.2.0`. La instalación local de `pm-skills` es `phuryn/pm-skills`, no `coreyhaines31/marketingskills`.

El `origin/main` remoto avanzó a `eab20ca` con `docs/ADAPTIVE_AGENT_ARCHITECTURE.md` y cambia la jerarquía fija por routing adaptativo. Es una actualización válida del portátil que esta máquina aún no tenía; debe integrarse, no sobrescribirse.

No se encontraron clones locales de ECC, `coreyhaines31/marketingskills`, Hallmark, No AI Slop, Caveman, Headroom, tokless o `vidanov/context-compress`. Se evaluaron sus fuentes públicas y refs remotos, pero eso no equivale a una auditoría de código local instalada.

## Hooks, memoria y red

Existe un único hook de Claude como artefacto en `/home/Marc/.claude/hooks/precompact-memory.sh`, pero la configuración aplicada no lo referencia. Hay memorias bajo `/home/Marc/.claude/projects/*/memory/MEMORY.md`; no se leyó su contenido.

El hook recibe JSONL de transcript, toma las últimas 400 líneas, construye un prompt y llama a Claude headless; el análisis de seguridad está en `reports/security-review.md`. No se ha activado ningún hook nuevo por esta rama.

No hay listener en `127.0.0.1:20128` y `curl` devolvió conexión rechazada; por tanto no se debe enrutar ni probar contra OmniRoute como si estuviera disponible.

## Estado de inventario

| Estado | Elementos |
|---|---|
| ACTIVE_GLOBAL | Codex, Claude, Gemini global skills, agentes adaptativos de Claude, Addy skills expuestas, task-router |
| ACTIVE_PROJECT | instrucciones `CLAUDE.md`/`AGENTS.md` en varios proyectos; deben resolverse por alcance |
| AVAILABLE_ON_DEMAND | OpenCode, repositorios externos no instalados, optimizadores no instalados |
| DUPLICATED | copias de skills y `superpowers` 6.1.1/6.2.0 en cache |
| SECURITY_REVIEW_REQUIRED | hook archivado, proxy no disponible, directorios confiados, terceros |
| UNKNOWN | estado de OmniRoute, algunos wrappers fuera de las rutas iniciales, procedencia exacta de todas las copias del Codex |

## Límites del descubrimiento

No se hizo una búsqueda indiscriminada de todo el disco, no se inspeccionaron valores secretos ni memorias, y no se instalaron repositorios remotos. Antes de activar un componente externo debe hacerse una revisión de commit, scripts de instalación, permisos, red y rollback.
