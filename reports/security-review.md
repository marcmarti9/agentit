# Revisión de seguridad del diseño

**Alcance:** archivos versionados y pruebas locales de esta corrección. No es una auditoría del estado de una máquina ni una aprobación para operar en producción.

## Controles y límites

| Área | Control presente | Límite que exige revisión humana |
|---|---|---|
| Router | clasifica y propone; no ejecuta, carga skills, instala hooks ni concede permiso | las heurísticas pueden producir falsos positivos o negativos; RISK_3/RISK_4 y toda operación crítica requieren revisión |
| Catálogo | `registry.yaml` acepta rutas `${HOME}`/`${REPO_ROOT}`, estados conocidos y dependencias explícitas | es política portable, no evidencia de instalación, versión, seguridad o funcionamiento |
| Skills | separa `skills_available` y `skills_recommended_missing`; `skills` conserva solo las primeras | una ruta existente no valida por sí sola el contenido de una skill |
| Inventario | `python3 -m router.inventory` escribe una observación ignorada y calcula hashes de archivos regulares que no sean symlinks en la hoja | contiene rutas y hashes locales; debe revisarse antes de compartirlo y puede omitir versiones |
| Instalación/actualización | plan por defecto, validación temprana de opciones, rechazo de symlinks, copia atómica por archivo y manifiesto | `--apply` sigue siendo una mutación explícita que debe revisarse antes y después |
| Backups | raíz modo `0700`, copias modo `0600`, SHA-256 y `original_mode` registrados | el rollback no debe automatizarse con datos ambiguos ni sobrescribir cambios posteriores |
| Hardening | inspección acotada y NUL-safe de `mcp_auth.json`; calcula hashes, pero no analiza ni imprime sus valores | cambia permisos y aliases solo con `--apply`; requiere destino y backup confirmados |

## Rollback seguro

Las líneas `copy` del manifiesto registran `before_state` y `destination_sha256`. Un destino creado por el script (`before_state=absent`) solo puede eliminarse si continúa siendo un archivo regular, no es symlink y su hash actual coincide exactamente con `destination_sha256`. Si cambió, se conserva para revisión manual. Para un destino reemplazado, verifica `backup_sha256`, restaura el contenido de forma individual y reaplica `original_mode`; nunca uses eliminación recursiva.

## Hooks, red y terceros

El hook PreCompact conservado como artefacto procesa transcript y puede introducir fuga de datos, prompt injection o memoria incorrecta. Debe permanecer opt-in hasta disponer de límites de bytes, filtrado, procedencia, escritura atómica y fixtures adversariales. Proxies, MCP, wrappers y componentes externos requieren preflight y revisión de supply chain; el catálogo no prueba que estén disponibles o sean seguros.

## Compatibilidad

`install.sh`, `update.sh` y `security/harden-local.sh` dependen de Linux, Bash 4+ y comportamiento GNU (`stat -c`, `date --iso-8601`, `sha256sum`, `find -print0`, `mv -T`). No se afirma portabilidad shell fuera de ese entorno.

## Evidencia pendiente

- No se ejecutó GitHub Actions durante esta corrección.
- No se probaron operaciones destructivas, producción, bases de datos ni proveedores externos.
- No se midió reducción de tokens o coste.
- Esta corrección no ejecutó scripts con `--apply` ni modificó el HOME real.
