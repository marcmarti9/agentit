# Recomendaciones integradas

**Alcance:** decisiones de diseño para el repositorio. No constituyen aprobación de seguridad, despliegue ni publicación.

## Conservar como núcleo

- resolución directa y cero subagentes por defecto; delegación solo con independencia, ownership y verificador claros;
- `router/route.py` como clasificador heurístico y planificador, nunca como ejecutor o fuente de autorización;
- revisión humana para RISK_3/RISK_4 y todas las operaciones críticas;
- `registry.yaml` como política operativa portable, separada del inventario observado;
- progressive disclosure, deduplicación exacta y preservación íntegra de comandos, SQL, errores, diffs, rutas, hashes y números;
- instalador y actualizador en modo plan por defecto, con copias por archivo, manifiesto y rollback manual verificable.

## Selección de skills

El router debe informar por separado:

- `skills_available`: recomendaciones que superaron estado, ruta y dependencias esenciales;
- `skills_recommended_missing`: recomendaciones pertinentes que no superaron esas comprobaciones;
- `skills`: alias heredado que contiene únicamente `skills_available`.

No se debe cargar ni anunciar como utilizable una recomendación ausente. `supabase-postgres-best-practices` requiere una señal explícita de Postgres, PostgreSQL, `psql` o Supabase; SQLite no cumple esa condición.

## Inventario y plataforma

Generar la observación de cada máquina con `python3 -m router.inventory`. `reports/local/inventory.yaml` está ignorado por Git y puede omitir versiones que no se hayan observado. No trasladar sus rutas o estados al catálogo portable.

Los scripts shell requieren Linux, Bash 4+ y utilidades GNU. En otros sistemas deben ejecutarse únicamente en un entorno compatible o adaptarse y probarse antes de usar `--apply`.

## Componentes externos

Mantener hooks de compresión, proxies, MCP, wrappers y repositorios externos fuera del baseline hasta revisar procedencia, permisos, red, fidelidad y rollback. Los estados del catálogo son decisiones de política, no afirmaciones sobre lo instalado en una máquina.

## Evidencia y cambios locales

Los resultados locales reproducibles se registran en `evals/results.md`; el estado de GitHub Actions se informa por separado y solo después de una ejecución real. Esta corrección no ejecutó `--apply` ni modificó el HOME real: solo cambió el repositorio y generó el inventario ignorado.
