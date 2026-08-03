# Resultados de evaluación ejecutados

**Fecha:** 2026-08-03
**Entorno:** `/home/Marc/agents-config`, un HOME temporal bajo `/tmp` y post-checks limitados sobre el HOME real; no se tocaron bases de datos, producción ni proveedores externos.

## Pasados

| Prueba | Comando/alcance | Resultado |
|---|---|---|
| Router unitario | `python3 -m unittest discover -s router -p 'test_*.py' -v` | 13/13 OK |
| Import reproducible | `python3 -B -m unittest -v router.test_route router.test_registry` | 13/13 OK |
| Riesgo alto | auth, producción, explicit risk bajo | clasificación y revisión independiente correctas en tests |
| Contenido crítico | git diff + pipeline | compresión desactivada en test |
| Registry | `yaml.safe_load('registry.yaml')` | OK; 23 entradas |
| Sintaxis shell | `bash -n install.sh update.sh security/harden-local.sh` | OK |
| Instalador sandbox | `install.sh --apply --home /tmp/... --provider all` | agentes/skills/task-router en Claude, Codex, Antigravity y `.agents`; backup/hash creado |
| Preservación | archivo no relacionado en `.claude` del sandbox | conservado |
| Actualizador | `update.sh --home /tmp/... --provider claude` sin `--apply` | mostró plan; no escribió repo |
| Arquitectura remota | `git fetch --no-tags origin main`; comparación con `origin/main@eab20ca` | integrada; single-agent-first y providers aislados conservados |
| Aplicación real | `bash install.sh --apply --provider all --with-settings` | completada con backup; no se copiaron guías globales, settings.local, hook ni compresores |
| Post-check real | `jq` sobre `~/.claude/settings.json`, hashes de agentes, `gemini skills list` | danger prompt false, auto-upload false, hooks ausentes, hashes coincidentes, `task-router` Enabled |
| Separación final | archive explícito de `~/.codex/agents` y `~/.gemini/antigravity-cli/agents` | backup/hash creado; ningún archivo eliminado |
| Symlink adversarial | sandbox con `.codex/skills` como symlink | instalación rechazada antes de escribir |
| Manifest collision | backup con `manifest.txt` preexistente | instalación rechazada sin sobrescribirlo |
| Destination parent symlink | fixture de `update.sh` con `agents/` symlink | importación rechazada antes de crear temporal |
| Find error propagation | fixture con fuente ilegible | instalación rechazada; no se ignora el error de `find` |
| NUL-safe MCP paths | fixture con directorio con salto de línea | hardening rechazado sin reinterpretar la ruta |
| Guide separation | `install.sh --provider codex --with-guides` en sandbox | solo `AGENTS.md` y `CODEX.md` instalados |
| Hardening local | `security/harden-local.sh` sobre HOME real | aliases ausentes; seis MCP confirmados en modo 600; plan no escribió |
| OmniRoute estado | `curl --max-time 2 http://127.0.0.1:20128/` | no disponible; no se asumió activo |

Durante TDD, dos tests fallaron inicialmente por expresiones regulares singleton sin coma: el código iteraba caracteres en vez de tratar una tupla de patrones. La causa se corrigió; después se añadieron pruebas de routing adaptativo, señales RISK_4, registry y fixtures de seguridad; la suite actual pasa con 13 tests. No se ocultaron excepciones del test.

## No ejecutadas todavía

- A/B real de Caveman, RTK, Headroom, context-compress, tokless o LLMLingua-2;
- comparación de stdout/stderr/exit code de wrappers;
- pruebas de browser, DB desechable o proxy;
- carga con cada proveedor real y medición de tokens facturados;
- auditoría independiente final de la rama después de estos últimos cambios.

No se declara ahorro neto. Las evaluaciones extensivas quedan preparadas en `evaluation-plan.md` y requieren instalaciones aisladas y fixtures.
