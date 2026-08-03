# Inventario portable y observación local

Este archivo describe el método de inventario. No conserva rutas, versiones ni estados observados de una máquina concreta.

## Fuentes separadas

- `registry.yaml` es el catálogo versionado y la política operativa portable. Sus estados, prioridades, triggers y rutas `${HOME}`/`${REPO_ROOT}` no prueban que un componente esté instalado o sea utilizable.
- `reports/local/inventory.yaml` es una observación por máquina, generada bajo demanda e ignorada por Git.
- El router combina política y comprobaciones acotadas de rutas y dependencias para separar `skills_available` de `skills_recommended_missing`; el alias heredado `skills` contiene solo las disponibles.

## Generación

Desde la raíz del repositorio:

```bash
python3 -m router.inventory
```

El comando solo escribe el informe local; no instala componentes ni modifica configuración de proveedores. Se puede elegir otro destino con `--output`, otro catálogo con `--registry` y una raíz de usuario desechable con `--home`.

## Esquema local

| Campo | Significado |
|---|---|
| `generated_at` | instante UTC de la observación |
| `catalog`, `home` | rutas resueltas de esa ejecución; son datos locales |
| `providers[].executables[]` | nombre, ruta resuelta por `PATH` y `version`; la versión puede quedar sin observar |
| `providers[].target_roots[]` | plantillas portables resueltas para esa máquina |
| `entries.<id>.catalog_state` | estado de política copiado del catálogo, no prueba de disponibilidad |
| `entries.<id>.paths[]` | ruta resuelta, existencia, tipo y SHA-256 solo para archivos regulares que no sean symlinks |

## Límites

El resultado depende del `PATH`, HOME y sistema de archivos del momento. La ausencia de una ruta o versión no demuestra que el componente no exista en otra ubicación; la presencia tampoco valida su seguridad o compatibilidad. El informe puede contener rutas y hashes locales: revísalo antes de compartirlo y no lo añadas al control de versiones.
