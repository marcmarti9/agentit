# Revisión de seguridad, hooks, scripts y MCP

**Fecha:** 2026-08-03
**Criterio:** una salida o configuración de un agente es input no confiable hasta verificarla. El ahorro de tokens nunca puede reducir la fidelidad necesaria para una acción.

## Hallazgos

| ID | Severidad | Evidencia | Riesgo | Estado/acción |
|---|---|---|---|---|
| SEC-01 | Alta | `/home/Marc/.claude/settings.json:40-53` activa `PreCompact`; `.claude/hooks/precompact-memory.sh:8-41` envía transcript reciente a Claude y escribe memoria | fuga de datos sensibles, prompt injection desde transcript, memoria incorrecta o pérdida silenciosa | `SECURITY_REVIEW_REQUIRED`; no se despliega por el instalador seguro |
| SEC-02 | Alta | baseline `install.sh` en `4e6db85` usaba `rm -rf` para reemplazar destinos y copiaba settings/hooks sin opt-in | pérdida o activación accidental de configuración | corregido en esta rama con plan por defecto, backup, symlink refusal y copia individual |
| SEC-03 | Alta | `/home/Marc/.claude/settings.json:32-33` selecciona `architect` y `skipDangerousModePermissionPrompt: true` | reduce fricción antes de operaciones peligrosas | mantener fuera del baseline recomendado; requiere decisión explícita |
| SEC-04 | Alta | `/home/Marc/.claude/settings.json:37-39` activa `autoUploadSessions: true` | posible exfiltración/retención de conversaciones y secretos | recomendar desactivar en configuración segura o documentar consentimiento |
| SEC-05 | Media | `/home/Marc/.codex/config.toml:5-12` confía en `/home/Marc` y dos proyectos | carga automática de instrucciones/hooks en un ámbito amplio | reducir confianza al mínimo necesario por proyecto |
| SEC-06 | Media | `.claude/skills/*` contiene symlinks hacia `.agents/skills`; hay copias con drift en `.codex` | cambio de skill por ruta, versión o symlink no auditado | una fuente canónica y manifiesto de hashes; no seguir symlinks al instalar |
| SEC-07 | Media | plugins externos instalados aunque deshabilitados; no se instalaron ECC/optimizers | supply chain, hooks o scripts transitorios | mantener deshabilitados y revisar commit/installer antes de activar |
| SEC-08 | Baja/positiva | `codex mcp list` y `gemini mcp list` devuelven cero servidores; extensiones Gemini: cero | no hay superficie MCP activa que auditar ahora | conservar mínimo hasta necesitar una integración |
| SEC-09 | Media | OmniRoute instalado pero `20128` rechazó conexión | riesgo de asumir un proxy inexistente o duplicar wrappers | estado `UNKNOWN`; no modificar ni enrutar a él |
| SEC-10 | Alta | `/home/Marc/.bashrc:34-36` define `clauded`, `agyd` y `codexd` con bypasses peligrosos | convierte un alias cómodo en una ruta global que puede saltar permisos/sandbox | no ejecutar; sustituir por comandos explícitos o alias que no omitan confirmaciones |
| SEC-11 | Alta | seis `/home/Marc/.cursor/**/mcp_auth.json` tienen modo `644` | secretos MCP legibles por otros usuarios del sistema | revisar y endurecer a mínimo privilegio sin imprimir valores |
| SEC-12 | Media | `/home/Marc/.gemini/antigravity-cli/settings.json:3-10` confía en `/home/Marc` y varios proyectos | agents/hooks de proyecto pueden cargarse en un ámbito amplio | reducir a proyectos necesarios y revisar cada raíz |
| SEC-13 | Media | Superpowers `6.2.0/hooks/hooks.json:3-12` y Addy `hooks/session-start.sh:1-21` inyectan contexto en cada sesión | coste fijo, duplicación y contenido externo no seleccionado por tarea | una sola fuente de meta-skill; hooks desactivados hasta revisión |
| SEC-14 | Alta | `/home/Marc/.bashrc:70` y numerosos perfiles Claude declaran `ANTHROPIC_BASE_URL=http://localhost:20128`, pero el listener no existe | Claude puede fallar o depender de un gateway no verificado; las condiciones de red del gateway también aplican a la sesión | no se eliminó porque cambiar routing/auth requiere decisión; se documenta como preflight obligatorio |

## Hook PreCompact

El hook usa `jq`, `sed`, `tail`, `mkdir` y `claude -p`. Aunque limita por líneas a 400, no limita bytes, no filtra secretos ni separa datos de instrucciones, descarta el error de Claude con `2>/dev/null`, y escribe el resultado directamente con `>` en vez de usar una sustitución atómica. La ruta de memoria deriva de `cwd` con una sustitución simple de `/`, por lo que no es una política completa de aislamiento.

No se debe corregir el hook suponiendo que el resumen es verdad. Un resumen es una vista derivada: debe contener procedencia, timestamp, hash o referencia al transcript, y nunca sustituir errores, comandos, diffs, números o decisiones críticas.

## Barreras implementadas en esta rama

- `install.sh` funciona en modo plan por defecto y exige `--apply` para escribir.
- No elimina archivos existentes ni sigue symlinks de origen/destino.
- Hace backup antes de reemplazar un destino, genera `manifest.txt` y añade SHA-256.
- Settings, settings.local, guías y hook son opt-in; el actualizador no importa `settings.local`.
- `update.sh` usa allowlist de agentes y skills, no copia un directorio arbitrario ni ejecuta hooks.
- El router prohíbe compresión para riesgo alto y contenido crítico; no ejecuta comandos.
- `settings.json` del repositorio ya no omite el aviso de modo peligroso, desactiva la subida automática de sesiones, limita retención a 90 días y no declara `PreCompact`. El hook se conserva solo como artefacto pendiente de revisión.
- `security/harden-local.sh` hace reproducibles las correcciones locales de aliases y permisos sin leer valores sensibles; funciona en modo plan por defecto.

## Amenazas del modelo

1. **Prompt injection en salida de herramientas o transcript:** tratar texto recuperado como datos, no instrucciones; separar metadatos y contenido.
2. **Pérdida por truncado:** conservar original, ID estable y recuperación; RISK_4 no comprime.
3. **Supply chain:** no ejecutar `curl | bash`, hooks o wrappers de upstream sin revisar commit, permisos y red.
4. **Confusión de proveedor:** no usar el model ID de Codex en Claude/Gemini sin comprobar disponibilidad.
5. **Escalada por confianza global:** reducir raíces confiadas y no instalar reglas globales innecesarias.
6. **Fuga por memoria/session upload:** no guardar secretos; hacer opt-in explícito para subir sesiones.

## Gaps pendientes

- No hay todavía un hook seguro alternativo validado con fixtures de secretos y prompt injection.
- No hay pruebas de fidelidad de RTK/Headroom/LLMLingua porque no están instalados ni activados.
- No se ha hecho una revisión independiente final de esta rama; debe actuar un Auditor antes de integrar cambios de settings/hooks.
- Los permisos de `mcp_auth.json`, aliases peligrosos y confianza de Antigravity requieren una intervención separada y reversible; este trabajo no los ha modificado.
- La configuración segura de Claude aún debe aplicarse al HOME real con backup y revisión de diff; hasta entonces el inventario local sigue describiendo la configuración anterior.
- Se realizó una corrección local reversible fuera del repo: backup versionado del `.bashrc`, aliases bypass comentados, `.bashrc` en modo `600` y seis `mcp_auth.json` en modo `600`. No se leyó ni mostró ningún secreto.
