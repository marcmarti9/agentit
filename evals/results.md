# Resultados de evaluación ejecutados

**Fecha:** 2026-08-03
**Entorno:** `/home/Marc/agents-config` y un HOME temporal bajo `/tmp`; no se tocaron bases de datos, producción, HOME real ni proveedores externos.

## Pasados

| Prueba | Comando/alcance | Resultado |
|---|---|---|
| Router unitario | `python3 -m unittest discover -s router -p 'test_*.py' -v` | 9/9 OK |
| Riesgo alto | auth, producción, explicit risk bajo | clasificación y revisión independiente correctas en tests |
| Contenido crítico | git diff + pipeline | compresión desactivada en test |
| Registry | `yaml.safe_load('registry.yaml')` | OK; 19 entradas |
| Sintaxis shell | `bash -n install.sh update.sh` | OK |
| Instalador sandbox | `install.sh --apply --home /tmp/... --provider all` | agentes/skills/task-router en Claude, Codex, Antigravity y `.agents`; backup/hash creado |
| Preservación | archivo no relacionado en `.claude` del sandbox | conservado |
| Actualizador | `update.sh --home /tmp/... --provider claude` sin `--apply` | mostró plan; no escribió repo |
| Arquitectura remota | `git fetch --no-tags origin main`; comparación con `origin/main@eab20ca` | integrada; single-agent-first y providers aislados conservados |
| Aplicación real | `bash install.sh --apply --provider all --with-settings` | completada con backup; no se copiaron guías globales, settings.local, hook ni compresores |
| Post-check real | `jq` sobre `~/.claude/settings.json`, hashes de agentes, `gemini skills list` | danger prompt false, auto-upload false, hooks ausentes, hashes coincidentes, `task-router` Enabled |
| OmniRoute estado | `curl --max-time 2 http://127.0.0.1:20128/` | no disponible; no se asumió activo |

Durante TDD, dos tests fallaron inicialmente por expresiones regulares singleton sin coma: el código iteraba caracteres en vez de tratar una tupla de patrones. La causa se corrigió; después se añadieron dos pruebas de routing adaptativo y los 9 tests pasan. No se ocultaron excepciones del test.

## No ejecutadas todavía

- A/B real de Caveman, RTK, Headroom, context-compress, tokless o LLMLingua-2;
- comparación de stdout/stderr/exit code de wrappers;
- pruebas de browser, DB desechable o proxy;
- carga con cada proveedor real y medición de tokens facturados;
- auditoría independiente final de la rama.

No se declara ahorro neto. Las evaluaciones extensivas quedan preparadas en `evaluation-plan.md` y requieren instalaciones aisladas y fixtures.
