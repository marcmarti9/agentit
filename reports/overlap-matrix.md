# Matriz de solapamiento

La matriz distingue capacidades, no nombres comerciales. `A` significa capacidad principal, `S` secundaria, `—` no es el objetivo.

| Capacidad | ECC | Superpowers | Addy Agent Skills | Marketing Skills | Hallmark | No AI Slop | Decisión del harness |
|---|---:|---:|---:|---:|---:|---:|---|
| planificación / spec | A | A | A | — | — | — | una skill seleccionada, no tres |
| implementación | A | A | A | — | S | — | metodología bajo demanda |
| TDD / testing | A | A | A | — | S | — | TDD solo con lógica o regresión |
| debugging | A | S | A | — | — | — | debugging on-demand |
| code review | A | S | A | — | — | — | revisión proporcional |
| arquitectura / APIs | A | S | A | — | — | — | arquitectura solo con límites reales |
| seguridad | A | — | A | — | — | — | security-hardening en RISK_3/RISK_4 |
| memoria / contexto | A | S | A | — | — | — | política local; no cargar bundles completos |
| investigación / herramientas | A | S | A | S | — | — | investigación separada de ejecución |
| documentación técnica | A | S | A | — | — | S | documentación vinculada al cambio |
| frontend funcional | S | S | A | — | S | — | frontend-ui-engineering cuando aplique |
| diseño visual | — | — | S | — | A | — | Hallmark solo visual |
| marketing / CRO / SEO | S | — | — | A | — | — | bundle de marketing especializado |
| copywriting público | — | — | S | A | — | A | marketing primero; No AI Slop opcional al final |
| coordinación de subagentes | A | S | S | — | — | — | Architect decide; Orchestrator solo multidominio |

## Integración de la hipótesis inicial

La hipótesis es útil con dos correcciones:

1. **Superpowers** puede ser la metodología principal para una feature compleja, pero no debe convertirse en instrucciones globales si Addy ya aporta el lifecycle seleccionado.
2. **Agent Skills** es la fuente local más amplia de producción, pero su copia global está duplicada y tiene drift. Debe existir una única fuente canónica y despliegues verificables.
3. **Marketing Skills** solicitado (`coreyhaines31/marketingskills`) no está instalado. El plugin observado es `phuryn/pm-skills`; se mantiene separado hasta una comparación de casos con el repo correcto.
4. **Hallmark** y **No AI Slop** son especializados y no deben entrar en el baseline de ingeniería.
5. **ECC** es un catálogo de componentes, no un motivo para instalar un framework monolítico; se deben extraer solo capacidades que no estén cubiertas.

## Variantes recomendadas

| Perfil | Skills máximas orientativas | Uso |
|---|---:|---|
| lite | 0–1 | explicación, cambio trivial, comprobación puntual |
| standard | 1–3 | bug/feature pequeña, con una skill de dominio y verificación |
| deep | 2–5 | feature mediana, arquitectura, revisión crítica |
| critical | justificadas individualmente | seguridad, migración, producción; incluye revisión independiente |

Los máximos son límites de coordinación, no objetivos de consumo.
