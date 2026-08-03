# Comparación de optimizadores de tokens y contexto

**Regla:** las cifras de ahorro publicadas por los proyectos son claims de sus autores, no mediciones de este harness. Aquí se separan superficie, fidelidad, reversibilidad y coste total.

## Decisión resumida

| Herramienta | Función observada | Riesgo principal | Compatibilidad práctica | Clasificación |
|---|---|---|---|---|
| Caveman | concisión/compresión de output y modos para agentes | puede quitar contexto explicativo o matices | integración por hook/plugin; no instalada | `ENABLE_BY_PROFILE` para `TERSE_SAFE` |
| RTK | wrappers/filtros de salida de terminal y auto-rewrite de Bash | altera stdout, semántica de pipes/pipelines o fuerza repeticiones | tiene instrucciones/hooks para Claude, Gemini, Codex y Antigravity; no instalado | `MANUAL_ONLY` / `EXPERIMENTAL` con allowlist |
| Headroom | routing por contenido, compresión de JSON/código/prosa y CCR recuperable | integración, latencia, recuperación incorrecta o proxy duplicado | MCP/wrapper/proxy, no instalado | `ENABLE_BY_TASK` en perfil aislado |
| context-compress | compresión/limpieza de archivos de instrucciones con modos regex/LLM | cambia negaciones o wording exacto; hooks automáticos | CLI/batch, no instalado | `MANUAL_ONLY` para prosa no crítica |
| tokless | pipeline unificado de herramientas y contexto | supply chain, solapamiento y “one tool” opaco | declara soporte multiagente; no instalado | `REJECT` para instalación automática; investigación opcional |
| LLMLingua-2 | compresión semántica task-agnostic | pérdida de números, negaciones, errores o sintaxis | componente Python/ML; dependencia local parcial en OmniRoute | `EXPERIMENTAL` offline |
| Agent Skills for Context Engineering | prácticas de selección, memoria, evaluación y progressive disclosure | no es un compresor ejecutable; riesgo de cargar demasiadas skills | plataforma-agnostic | `KEEP_AS_REFERENCE` |
| OmniRoute | catálogo local con session-dedup, CCR, RTK, Headroom, Caveman y LLMLingua | proxy/interceptación y asunción de disponibilidad | paquete instalado, gateway `20128` no responde | `MANUAL_ONLY` como fuente de ideas |

## Compatibilidad y fuentes

- [Caveman](https://github.com/JuliusBrussee/caveman) documenta modos de concisión e integraciones con agentes. Sus porcentajes deben medirse con output y calidad reales.
- [RTK](https://github.com/rtk-ai/rtk) documenta filtros de comandos, hooks/auto-rewrite y soporte para varios clientes. La cifra que importa aquí debe incluir repeticiones, exit codes, stderr, pipes y fallos.
- [Headroom](https://github.com/headroomlabs-ai/headroom) documenta ContentRouter, SmartCrusher, CCR y uso como MCP/wrapper/proxy. Su ventaja potencial es conservar originales, pero hay que probar la integración concreta.
- [context-compress](https://github.com/vidanov/context-compress) ofrece modos de reducción y estadísticas para instruction files. Se limita a batch manual hasta probar fidelidad.
- [tokless](https://github.com/HoangP8/tokless) propone una instalación unificada; el instalador y la superficie de hooks requieren revisión independiente antes de ejecutar.
- [LLMLingua](https://github.com/microsoft/LLMLingua) y [LLMLingua-2](https://aclanthology.org/2024.findings-acl.57/) aportan una base académica, pero no son una skill directa de Codex/Claude.
- [Agent Skills for Context Engineering](https://github.com/muratcankoylan/agent-skills-for-context-engineering) es una fuente de prácticas de contexto, no una autorización para instalar sus skills completas globalmente.

## Política por contenido

| Contenido | Acción por defecto |
|---|---|
| logs repetitivos no críticos, progreso decorativo | reducción estructural medible, manteniendo fallos |
| JSON/tablas grandes recuperables | exact dedup o CCR con ID y original local |
| texto histórico secundario | compresión semántica experimental con comparación |
| código, SQL, esquemas, diffs, comandos, errores | conservar completo |
| rutas, hashes, IDs, números, fechas y límites | conservar exacto |
| secretos, permisos, migraciones y operaciones persistentes | fidelidad completa; RISK_3/RISK_4 |
| pipes, redirecciones, pipelines y stdout que alimenta otro comando | no interceptar |

## Qué debe medir una prueba

No basta con `input_tokens_before - input_tokens_after`. El registro debe incluir input no cacheado, creación/lecturas de caché, output, subagentes, repeticiones, recuperaciones, llamadas, duración, éxito, tests, regresiones, archivos releídos y diferencias entre stdout original y adaptado. Una optimización que reduce una línea pero provoca una segunda ejecución no es ahorro neto.

## OmniRoute local

La inspección del paquete Node `/home/Marc/.nvm/versions/node/v22.23.0/lib/node_modules/omniroute` encontró catalogados CCR, deduplicación de sesión, RTK, Headroom, Caveman y LLMLingua. Eso es evidencia de código instalado, no evidencia de gateway activo: `curl http://127.0.0.1:20128/` falló y no se activó ninguna ruta.
