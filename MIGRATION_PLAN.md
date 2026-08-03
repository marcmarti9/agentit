# Plan de migración segura

## Estado actual

La implementación está en la rama `feature/safe-context-harness-audit` del repositorio `agents-config`. Los commits son rollbackables. La instalación real no se ha aplicado; solo se validó un HOME temporal.

## Etapas

1. **Descubrimiento:** completado; inventario en `reports/inventory.md`.
2. **Auditoría:** local completada; auditoría delegada y revisión independiente deben integrarse antes de settings/hooks.
3. **Backup:** para cada aplicación real, usar `install.sh --apply`, que exige y genera backup/manifiesto/hash. Mantener el commit anterior.
4. **Baseline provider-neutral:** desplegar solo agentes, skills locales y `task-router` con:

   ```bash
   bash install.sh --provider all
   bash install.sh --apply --provider all
   ```

   El primer comando es plan; revisar rutas. El segundo no copia settings, guías ni hook.

5. **Provider check:** comprobar discovery en Codex, Claude y Gemini/Antigravity; verificar que cada skill apunta al hash esperado.
6. **Settings:** no aplicar `--with-settings` hasta revisar `skipDangerousModePermissionPrompt`, auto-upload y hooks; preferir un settings seguro separado.
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
