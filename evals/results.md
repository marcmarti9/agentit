# Resultados locales de esta corrección

**Fecha:** 2026-08-03

**Alcance:** repositorio y directorios temporales. No se ejecutaron operaciones de producción, bases de datos, proveedores externos ni scripts con `--apply` sobre el HOME real.

## Comandos ejecutados

| Comando | Resultado local observado |
|---|---|
| `python3 -m unittest discover -s router -p 'test_*.py' -v` | 61/61 tests OK |
| `python3 -B -m unittest -v router.test_route router.test_registry router.test_inventory router.test_profiles` | 61/61 tests OK como módulos |
| suite del router con un `HOME` temporal vacío | 61/61 tests OK; no depende del inventario del autor |
| `python3 -m unittest discover -s tests -p 'test_*.py' -v` | 17/17 tests OK; los cambios se realizaron en fixtures temporales |
| `bash -n install.sh update.sh security/harden-local.sh` | exit code 0 |
| `python3 -c "import yaml; yaml.safe_load(open('registry.yaml', encoding='utf-8'))"` | exit code 0 |
| `python3 -m json.tool settings.json` | exit code 0 |
| `python3 -m router.inventory` | generó `reports/local/inventory.yaml` |
| `git check-ignore -v reports/local/inventory.yaml` | confirmó la regla `reports/local/` de `.gitignore` |

La suite del router cubre intención frente a acción, cláusulas mixtas, gates críticos, SQLite frente a PostgreSQL, salida de skills, catálogo portable, carga de `SKILL.md`, symlinks, conflictos, fallo cerrado, inventario, perfiles acotados y activación segura. La suite de scripts cubre rechazo antes del backup, round-trip Antigravity de los `SKILL.md` allowlisted, instalación global del perfil `core` y permisos privados de backups y credenciales; no afirma simetría de árboles completos.

## No afirmado

- GitHub Actions no se ejecutó desde esta corrección; no se declara un resultado de CI remoto.
- El inventario local no valida seguridad, funcionamiento ni versiones no observadas.
- No se midió reducción de contexto, tokens o coste.
- No se realizó una aprobación final ni se afirma preparación para producción.

## Evaluación de perfiles y explicabilidad

**Fecha:** 2026-08-03

| Comprobación | Resultado local observado |
|---|---|
| `python3 evals/run.py` | 9/9 casos representativos del router OK |
| Perfil `core` | 10 skills globales; `all` cubre exactamente las 28 skills del repositorio |
| Activación `agentit enable|disable` | plan por defecto, manifiesto con hashes y rechazo de archivos modificados/no gestionados verificados |
| Descripciones de descubrimiento | 28 descripciones revisadas; longitud máxima observada: 152 caracteres |

Estos resultados prueban regresiones locales del clasificador y del gestor de
perfiles. No prueban que un agente produzca mejor código, ni reducción de tokens,
latencia o coste frente a un baseline.
