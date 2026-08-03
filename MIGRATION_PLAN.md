# Plan de migración segura

## Estado

Esta corrección actualiza el repositorio y genera un inventario local ignorado. No ejecutó `install.sh --apply`, `update.sh --apply` ni `security/harden-local.sh --apply` sobre el HOME real, y no constituye aprobación para producción.

## Requisitos

- Linux con Bash 4+ y utilidades GNU (`coreutils`, `findutils`);
- Python 3 con PyYAML para router, catálogo e inventario;
- destino, provider y backup revisados antes de aplicar;
- revisión humana para RISK_3/RISK_4 y cualquier operación crítica.

## Etapas

1. **Inventario:** ejecutar `python3 -m router.inventory`; revisar `reports/local/inventory.yaml` sin versionarlo. Las versiones pueden quedar sin observar.
2. **Validación local:** ejecutar las suites y comprobaciones listadas en `evals/results.md`; comprobar GitHub Actions por separado cuando se publique la rama.
3. **Plan:** ejecutar `bash install.sh --provider <provider>` sin `--apply` y revisar todas las rutas.
4. **Backup:** elegir un directorio privado y confirmar que no existe ni contiene symlinks. El script crea raíz `0700`, copias `0600` y registra hashes más `original_mode`.
5. **Aplicación:** usar `--apply` solo tras la revisión. Settings, guías y hook siguen siendo opt-in.
6. **Post-check:** comparar destinos con el manifiesto y verificar discovery del provider sin asumir que el catálogo demuestra disponibilidad.
7. **Rollback:** ensayar [`ROLLBACK.md`](ROLLBACK.md). Un destino nuevo solo puede eliminarse si conserva exactamente el hash registrado.

## Restricciones

- no instalar upstream automáticamente ni ejecutar `curl | bash`;
- no activar proxy, MCP, hook o compresión global sin revisión independiente;
- no copiar `settings.local.json` salvo petición explícita;
- no tocar proyectos, bases de datos ni producción durante la evaluación;
- detenerse ante symlinks, rutas ambiguas, hash distinto o backup no verificable.
