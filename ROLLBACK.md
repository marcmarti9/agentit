# Rollback

## Rollback del código

La rama conserva commits pequeños y reversibles. Antes de integrar, revisar:

```bash
git log --oneline --decorate -8
git diff main...HEAD
git status --short
```

Para abandonar la integración local, cambiar a otra rama o eliminar la rama solo después de confirmar que no contiene cambios del usuario. No se debe usar `git reset --hard` sobre trabajo no revisado.

## Rollback de una instalación

`install.sh --apply` crea un directorio `backups/agent-harness-pre-install-<timestamp>` o el indicado por `--backup-dir`, guarda destinos reemplazados, `manifest.txt` y SHA-256. El instalador no elimina archivos extra, por lo que el rollback consiste en restaurar únicamente los destinos listados en el manifiesto, después de comprobar que siguen perteneciendo a esta instalación.

Procedimiento seguro:

1. detener el uso del provider afectado;
2. revisar el manifiesto y los hashes;
3. comparar backup, destino y fuente actual;
4. restaurar archivos uno por uno a un directorio temporal;
5. comprobar permisos y contenido;
6. moverlos al destino solo después de la revisión;
7. verificar discovery del provider y ejecutar una prueba mínima.

No restaurar automáticamente settings, hooks, credenciales ni archivos que hayan cambiado posteriormente. No se usa una eliminación recursiva como mecanismo de rollback.

## Rollback de experimentos

- Caveman/RTK/Headroom/LLMLingua: apagar el perfil/adaptador y usar stdout/original local.
- CCR: conservar el almacén y recuperar por ID; si la recuperación falla, detener la acción y no improvisar.
- Hook de memoria: deshabilitar la entrada `PreCompact`, preservar las memorias para revisión y volver a la última configuración conocida.
- MCP/proxy: quitar solo la entrada explícita tras capturar configuración y logs; no borrar caches de terceros.
