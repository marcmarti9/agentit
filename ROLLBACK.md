# Rollback

## Compatibilidad

Los scripts y el formato de evidencia están dirigidos a Linux con Bash 4+ y utilidades GNU. No automatices este procedimiento con un parser no revisado ni trates el manifiesto como código shell.

## Cambios del repositorio

Antes de descartar cambios, revisa `git status`, `git diff` y el historial. Conserva trabajo del usuario y evita `git reset --hard`; cambiar o eliminar una rama requiere confirmar primero que no contiene cambios necesarios.

## Evidencia de instalación o actualización

Con `--apply`, `install.sh` y `update.sh` crean una raíz de backup modo `0700`. Cada copia de un archivo preexistente queda modo `0600` y el manifiesto registra:

- `backup_sha256` y `original_sha256`;
- `original_mode`, que debe reaplicarse al restaurar;
- por cada copia, `before_state` y `destination_sha256`.

## Procedimiento por archivo

1. Detén el provider afectado y revisa manualmente el destino exacto y su línea de manifiesto.
2. Rechaza symlinks, archivos no regulares, rutas ambiguas o hashes que no coincidan.
3. Si `before_state=present`, verifica `backup_sha256` y que el destino actual conserva `destination_sha256`. Restaura primero a un temporal, mueve el archivo individualmente y aplica `original_mode`. Si el destino cambió después de la instalación, no lo sobrescribas: conserva ambos y resuelve el conflicto manualmente.
4. Si `before_state=absent`, no existe backup que restaurar. Elimina únicamente ese archivo si sigue siendo regular, no es symlink y su SHA-256 actual coincide exactamente con `destination_sha256`. Si difiere, consérvalo para revisión.
5. No elimines directorios de forma recursiva ni archivos extra; el manifiesto no demuestra ownership de directorios.
6. Verifica permisos, hashes y discovery del provider después de cada restauración o retirada.

## Hardening local

`security/harden-local.sh` conserva copias privadas y `original_mode`, pero los cambios de aliases y permisos requieren revisión manual antes de restaurar. No elimines `.bashrc`, credenciales, settings, hooks o caches como mecanismo de rollback.

## Experimentos y servicios

Desactiva solo la entrada explícita de un hook, proxy, MCP o adaptador después de preservar configuración y logs. Si el original no puede recuperarse o el hash no coincide, detén el rollback y solicita revisión humana.
