# Plan de migración segura

## Estado actual

La implementación está en la rama `feature/safe-context-harness-audit` del repositorio `agents-config`. Los commits son rollbackables. El baseline se aplicó al HOME real el 2026-08-03 con backup en `/home/Marc/backups/agent-harness-pre-install-20260803-160912`.

## Etapas

1. **Descubrimiento:** completado; inventario en `reports/inventory.md`.
2. **Auditoría:** inventario, auditoría local y revisión de los cambios principales completados; la auditoría independiente final aprobó `299f2db` sin hallazgos críticos ni no críticos.
3. **Backup:** para cada aplicación real, usar `install.sh --apply`, que exige y genera backup/manifiesto/hash. Mantener el commit anterior.
4. **Baseline provider-neutral:** desplegar solo agentes, skills locales y `task-router` con:

   ```bash
   bash install.sh --provider all
   bash install.sh --apply --provider all
   ```

   El primer comando es plan; revisar rutas. El segundo no copia settings, guías ni hook.

5. **Provider check:** comprobar discovery en Codex, Claude y Gemini/Antigravity; verificar que cada skill apunta al hash esperado.
6. **Settings:** el `settings.json` versionado es el baseline seguro (aviso peligroso, sin auto-upload, retención de 90 días y sin hook) y ya se aplicó en esta máquina con backup. En otra máquina, aplicarlo con `--with-settings` solo después de revisar el backup y el diff.
7. **Hook:** mantener desactivado hasta tener scrub, límites de bytes, escritura atómica, procedencia y tests adversariales.
8. **Optimización:** probar únicamente perfiles aislados; activar Caveman solo para output `TERSE_SAFE` si la medición neta lo justifica.
9. **Compresión de herramientas:** RTK/Headroom/LLMLingua nunca se activan globalmente en la primera migración.
10. **Evaluación:** ejecutar Fase A y luego una muestra de Fase B/C; guardar resultados, no claims.

## Restricciones

- no instalar upstream automáticamente;
- no ejecutar `curl | bash`;
- no activar proxy/MCP/hook global;
- no copiar `settings.local.json` salvo petición explícita;
- no tocar proyectos, bases de datos ni producción;
- si un destino es symlink o ambiguo, detenerse.
