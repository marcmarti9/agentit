"""Provider-neutral task router with intelligent delegation.

The router only classifies and plans. It never executes a command, rewrites
stdout, loads a skill body, or lowers an inferred risk level.

Single-agent is the default only when multi-agent adds no clear benefit.
There are no hard subagent min/max caps. Craft depth (standard/polished/studio)
applies to design/visual work only. No powerwords beyond natural Agentit
activation ("use/usa/... agentit" in the user's language).
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised by the CI dependency check
    yaml = None


try:
    from router.preferences import load_preferences
except ImportError:
    from preferences import load_preferences

RISK_ORDER = {f"RISK_{level}": level for level in range(5)}
SKILL_PROFILE_MAP = {
    "supabase-postgres-best-practices": "supabase",
    "browser-testing-with-devtools": "frontend",
    "anti-ai-slop-design": "design",
    "design-taste-frontend": "design",
    "using-agentit": "core",
    "test-driven-development": "core",
    "verification-before-completion": "core",
    "verification-gauntlet": "core",
    "api-and-interface-design": "backend",
    "observability-and-instrumentation": "backend",
    "marketing-and-growth": "product",
    "anti-ai-slop-writing": "writing",
    "shipping-and-launch": "release",
    "ci-cd-and-automation": "release",
    "deprecation-and-migration": "release",
    "doubt-driven-development": "research",
    "context-engineering": "research",
    "idea-refine": "product",
    "interview-me": "product",
    "spec-driven-development": "product",
}
CRITICAL_CONTENT = {
    "commands",
    "diff",
    "errors",
    "pipelines",
    "secrets",
    "sql",
}
DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parents[1] / "registry.yaml"
KNOWN_REGISTRY_STATES = {
    "ACTIVE_GLOBAL",
    "DUPLICATED",
    "AVAILABLE_ON_DEMAND",
    "NOT_INSTALLED",
    "DISABLED",
    "ARCHIVED",
    "BROKEN",
    "SECURITY_REVIEW_REQUIRED",
    "UNKNOWN",
}
AVAILABLE_REGISTRY_STATES = {"ACTIVE_GLOBAL", "DUPLICATED"}
TOPOLOGIES = ("direct", "probe", "fan_out", "pipeline", "writer_reviewer", "audit")
ALWAYS_CORE_SKILLS = (
    "using-agentit",
    "architect-orchestrator",
    "using-agent-skills",
    "task-router",
    "long-horizon-recovery",
    "mcp-tooling-fit",
    "verification-before-completion",
    "verification-gauntlet",
)
DOMAIN_PACK_BY_CATEGORY = {
    "marketing": "product",
    "design": "design",
    "testing": "engineering",
    "bug": "engineering",
    "security": "backend",
    "database": "data",
    "frontend": "frontend",
    "documentation": "writing",
    "explanation": "research",
    "engineering": "engineering",
}
CATEGORY_SKILL_FAMILIES = {
    "marketing": ["marketing-and-growth", "design-taste-frontend"],
    "design": ["frontend-ui-engineering", "design-taste-frontend", "impeccable-design"],
    "testing": ["test-driven-development", "debugging-and-error-recovery"],
    "bug": ["debugging-and-error-recovery", "test-driven-development"],
    "security": ["security-hardening", "architect-orchestrator"],
    "database": ["supabase-postgres-best-practices"],
    "frontend": ["frontend-ui-engineering"],
    "documentation": ["anti-ai-slop-writing", "documentation-and-adrs"],
    "explanation": [],
    "engineering": ["architect-orchestrator"],
}

PRESENTATION_PATTERNS = (
    r"\b(css|style|styles|color|colour|font|spacing|shadow|visual|visualmente)\b",
    r"\b(copy|label|text|texto|copia|etiqueta)\b",
)
FUNCTIONAL_BOUNDARY_PATTERNS = (
    r"\b(validation|validación|logic|lógica|endpoint|api|database|base de datos)\b",
    r"\b(transaction|transacción|checkout|charge|cobro|process|procesamiento)\b",
    r"\b(webhook|permission|permiso|credential|credencial|secret|secreto)\b",
    r"\b(session|sesión|migration|migración|deploy|desplieg|infrastructure|infraestructura)\b",
    r"\b(concurren|race condition|rollback)\b",
)
SENSITIVE_SIGNAL_PATTERNS = (
    ("authentication/session boundary", r"auth|login|logout|sesión|session|authorization|autorización"),
    ("payment/data boundary", r"payment|pago|billing|factur|pii|personal data|datos personales"),
    ("credentials/secrets boundary", r"secret|secreto|credential|credencial|api[_ -]?key|password|contraseña"),
    ("persistence/infrastructure boundary", r"migration|migración|deploy|desplieg|infrastructure|infraestructura|database|base de datos"),
    ("public API/concurrency boundary", r"public api|api pública|api contract|contrato de api|concurren|race condition|rollback"),
)
EXPLANATORY_PATTERNS = (
    r"^\s*[¿?]?\s*(explain|explícame|explica|qué es|what is|how to|cómo)\b",
    r"^\s*[¿?]?\s*how\s+(?:do|can|should|would)\s+(?:i|we|you)\b",
    r"^\s*[¿?]?\s*(what|why|when|where|which|qué|por qué|cuándo|dónde|cuál)\b",
    r"^\s*[¿?]?\s*(describe|review|revisa)\b.{0,80}\b(without changing|sin cambiar|conceptual|policy|política)\b",
)
HOW_TO_QUESTION_PATTERNS = (
    r"^\s*[¿?]?\s*how\s+(?:do|can|should|would)\s+(?:i|we|you)\b",
    r"^\s*[¿?]?\s*how\s+to\b",
    r"^\s*[¿?]?\s*¿?cómo\b",
)
IMPLEMENTATION_ACTION_PATTERNS = (
    r"\b(?:implement(?:ing|ed)?|build|add|create|change|modify|update|fix|refactor|migrate|integrate|optimi[sz]e|improve|write)\b",
    r"\b(?:implementa|implemento|implementar|construye|construir|añade|añadir|crea|crear|cambia|cambiar|modifica|modificar|actualiza|actualizar|arregla|arreglar|refactoriza|refactorizar|migra|migrar|integra|integrar|optimiza|optimizar|mejora|mejorar|escribe|escribir)\b",
)
PRESENTATION_OBJECT_PATTERNS = (
    r"\b(button|botón|label|etiqueta|text|texto|copy|copia|color|colour|font|spacing|shadow|visual|visualmente|style|styles|estilo|estilos|ui|interfaz|screen|pantalla|page|página|stylesheet|hoja de estilos)\b",
)
REVIEW_ACTION_PATTERNS = (
    r"^\s*[¿?]?\s*(review|revisa|revisar|audit|audita|auditar|inspect|inspecciona|inspeccionar)\b",
    r"\b(?:review|revisa|revisar|audit|audita|auditar)\b.{0,100}\b(?:only|solo|without changing|sin cambiar|read[- ]only|solo lectura)\b",
)
CLAUSE_BOUNDARY_PATTERNS = (
    r",",
    r";",
    r":",
    r"\n",
    r"\bthen\b",
    r"\binstead\b",
    r"\band\b",
    r"\bbut\b",
    r"\by luego\b",
    r"\bdespués\b",
    r"\by\b",
    r"\bpero\b",
)
QUESTION_CLAUSE_BOUNDARY_PATTERNS = (
    r",",
    r";",
    r":",
    r"\n",
    r"\bthen\b",
    r"\binstead\b",
)


class RegistryError(RuntimeError):
    """Raised when routing metadata is unavailable or unsafe to consume."""


def load_registry(registry_path: Path | None = None) -> dict[str, dict[str, Any]]:
    """Load and validate the portable registry, indexed by unique entry ID."""
    path = Path(registry_path) if registry_path is not None else DEFAULT_REGISTRY_PATH
    if yaml is None:
        raise RegistryError("PyYAML is required to load registry.yaml")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RegistryError(f"cannot read registry {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise RegistryError(f"invalid YAML in registry {path}: {exc}") from exc

    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise RegistryError("registry root must be a mapping with schema_version: 1")
    entries = raw.get("entries")
    if not isinstance(entries, list):
        raise RegistryError("registry entries must be a list")

    indexed: dict[str, dict[str, Any]] = {}
    for position, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise RegistryError(f"registry entry {position} must be a mapping")
        skill_id = entry.get("id")
        state = entry.get("state")
        paths = entry.get("paths")
        dependencies = entry.get("essential_dependencies", [])
        required_signals = entry.get("requires_signals_any", [])
        conflicts_with = entry.get("conflicts_with", [])
        if not isinstance(skill_id, str) or not skill_id.strip():
            raise RegistryError(f"registry entry {position} has an invalid id")
        if skill_id in indexed:
            raise RegistryError(f"duplicate registry id: {skill_id}")
        if state not in KNOWN_REGISTRY_STATES:
            raise RegistryError(f"unknown registry state for {skill_id}: {state!r}")
        if not isinstance(paths, list) or not all(isinstance(item, str) for item in paths):
            raise RegistryError(f"registry paths for {skill_id} must be a string list")
        for template in paths:
            if not (
                template == "${HOME}"
                or template.startswith("${HOME}/")
                or template == "${REPO_ROOT}"
                or template.startswith("${REPO_ROOT}/")
            ):
                raise RegistryError(
                    f"registry path for {skill_id} must use ${{HOME}} or ${{REPO_ROOT}}: {template}"
                )
            suffix = template.split("/", 1)[1] if "/" in template else ""
            if ".." in Path(suffix).parts:
                raise RegistryError(f"registry path for {skill_id} escapes its root: {template}")
        if not isinstance(dependencies, list) or not all(
            isinstance(item, str) and item for item in dependencies
        ):
            raise RegistryError(
                f"essential_dependencies for {skill_id} must be an ID list"
            )
        if not isinstance(required_signals, list) or not all(
            isinstance(item, str) and item for item in required_signals
        ):
            raise RegistryError(f"requires_signals_any for {skill_id} must be a string list")
        if not isinstance(conflicts_with, list) or not all(
            isinstance(item, str) and item for item in conflicts_with
        ):
            raise RegistryError(f"conflicts_with for {skill_id} must be an ID list")
        for field in ("priority", "context_cost", "execution_cost", "trigger", "avoid_when"):
            value = entry.get(field)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise RegistryError(f"{field} for {skill_id} must be a non-empty string")
        conflicts = entry.get("conflicts", [])
        if not isinstance(conflicts, list) or not all(isinstance(item, str) for item in conflicts):
            raise RegistryError(f"conflicts for {skill_id} must be a string list")
        normalized = dict(entry)
        normalized["essential_dependencies"] = list(dependencies)
        normalized["conflicts_with"] = list(conflicts_with)
        indexed[skill_id] = normalized
    for skill_id, entry in indexed.items():
        for reference in entry["essential_dependencies"] + entry["conflicts_with"]:
            if reference not in indexed:
                raise RegistryError(f"registry reference for {skill_id} is absent: {reference}")
    return indexed


def resolve_registry_path(template: str, *, registry_path: Path, home: Path) -> Path:
    """Resolve one validated portable template without general env expansion."""
    repo_root = registry_path.resolve().parent
    if template == "${HOME}":
        root, relative = home.resolve(), ""
    elif template.startswith("${HOME}/"):
        root, relative = home.resolve(), template.removeprefix("${HOME}/")
    elif template == "${REPO_ROOT}":
        root, relative = repo_root, ""
    elif template.startswith("${REPO_ROOT}/"):
        root, relative = repo_root, template.removeprefix("${REPO_ROOT}/")
    else:
        raise RegistryError(f"unsupported registry path template: {template}")
    candidate = root / relative
    if not candidate.resolve(strict=False).is_relative_to(root):
        raise RegistryError(f"registry path escapes its resolved root: {template}")
    return candidate


def _path_is_loadable(entry: dict[str, Any], path: Path) -> bool:
    if path.is_symlink():
        return False
    kind = entry.get("kind", "skill")
    if "skill" not in kind and kind not in {"plugin", "bundle"}:
        return path.is_file()
    skill_file = path if path.is_file() else path / "SKILL.md"
    return skill_file.is_file() and not skill_file.is_symlink()


def _matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def _explanatory_requested(text: str) -> bool:
    return _matches(text, EXPLANATORY_PATTERNS)


def _implementation_requested(text: str) -> bool:
    if not _matches(text, IMPLEMENTATION_ACTION_PATTERNS):
        return False
    if not _explanatory_requested(text):
        return True
    boundaries = (
        QUESTION_CLAUSE_BOUNDARY_PATTERNS
        if _matches(text, HOW_TO_QUESTION_PATTERNS)
        else CLAUSE_BOUNDARY_PATTERNS
    )
    return _matches(
        text,
        tuple(
            rf"{boundary}.{{0,120}}{action}"
            for boundary in boundaries
            for action in IMPLEMENTATION_ACTION_PATTERNS
        ),
    )


def _presentation_only(text: str) -> bool:
    """Return true when sensitive nouns are present only in visual/prose scope."""
    sensitive_patterns = tuple(pattern for _, pattern in SENSITIVE_SIGNAL_PATTERNS)
    if not _matches(text, PRESENTATION_PATTERNS):
        return False
    if not _matches(text, sensitive_patterns) or _matches(
        text, FUNCTIONAL_BOUNDARY_PATTERNS
    ):
        return False
    return not (
        _matches(text, IMPLEMENTATION_ACTION_PATTERNS)
        and not _matches(text, PRESENTATION_OBJECT_PATTERNS)
    )


def _agentit_mentioned(text: str) -> bool:
    return bool(re.search(r"\bagentit\b", text, re.IGNORECASE))


def _agentit_activation_requested(text: str) -> bool:
    """Recognize affirmative natural-language activation, not a bare mention."""
    if not _agentit_mentioned(text):
        return False
    if _matches(
        text,
        (
            r"\b(?:do not|don't|dont|never)\b.{0,40}\b(?:use|enable|activate)\b.{0,20}\bagentit\b",
            r"\b(?:no|nunca)\b.{0,40}\b(?:uses?|usar|actives?|activar|habilites?|habilitar)\b.{0,20}\bagentit\b",
            r"\b(?:without|sin)\b.{0,20}\b(?:using|enabling|activating|usar|habilitar|activar)\b.{0,20}\bagentit\b",
            r"\bagentit\b.{0,30}\b(?:without|sin)\b.{0,20}\b(?:enabling|activating|habilitar|activar)\b",
        ),
    ):
        return False
    return _matches(
        text,
        (
            r"\b(?:use|using|enable|activate)\b.{0,20}\bagentit\b",
            r"\b(?:usa|usar|usando|utiliza|utilizar|utilizando|activa|activar|habilita|habilitar)\b.{0,20}\bagentit\b",
            r"\b(?:utilise|utiliser|utilisant|active|activer)\b.{0,20}\bagentit\b",
            r"\b(?:modo\s+agentit|agentit\s+mode)\b",
        ),
    )


def _file_path_mentions(text: str) -> list[str]:
    return re.findall(
        r"\b[\w./-]+\.(?:ts|tsx|js|jsx|py|go|rs|java|rb|php|css|scss|html|vue|svelte|md|sql|yml|yaml|json)\b",
        text,
        flags=re.IGNORECASE,
    )


def _domain_pair_signals(text: str) -> list[str]:
    pairs = (
        ("frontend", r"\b(frontend|front-end|ui|interfaz|react|next\.?js|css)\b"),
        ("backend", r"\b(backend|back-end|api|server|servicio|endpoint)\b"),
        ("tests", r"\b(tests?|pruebas?|e2e|unit(?:arios?)?|pytest|jest|vitest)\b"),
        ("docs", r"\b(docs?|documentation|documentación|readme)\b"),
        ("design", r"\b(design|diseño|visual|landing|ui\s*ux)\b"),
        ("data", r"\b(database|base de datos|sql|schema|migración|migration)\b"),
        ("infra", r"\b(ci|cd|deploy|infra|docker|kubernetes|pipeline)\b"),
    )
    found = [name for name, pattern in pairs if re.search(pattern, text, re.IGNORECASE)]
    return found


def _structural_plan_requested(text: str) -> bool:
    return _matches(
        text,
        (
            r"\b(architect(?:ure)?|arquitect(?:ura)?|estructura|restructur|rediseño de (?:la )?arquitectura)\b",
            r"\b(system design|diseño del sistema|plantea(?:miento)?|propuesta de (?:estructura|arquitectura|diseño))\b",
            r"\b(migrate|migración|refactor (?:global|grande|completo)|large refactor)\b",
            r"\b(multi[- ]?(?:module|package|service)|varios (?:módulos|paquetes|servicios))\b",
        ),
    )


def _parallelism_signals(text: str) -> dict[str, Any]:
    """Detect real parallel opportunity from ordinary language — no powerwords."""
    signals: list[str] = []
    score = 0.0

    paths = _file_path_mentions(text)
    unique_paths = list(dict.fromkeys(p.lower() for p in paths))
    if len(unique_paths) >= 2:
        signals.append(f"multi_path:{len(unique_paths)}")
        score += 0.35

    domains = _domain_pair_signals(text)
    if len(domains) >= 2:
        signals.append("domain_pair:" + "+".join(domains[:4]))
        score += 0.30

    # Natural concurrency / independence language (ordinary prompts).
    if _matches(
        text,
        (
            r"\b(en paralelo|at the same time|al mismo tiempo|simult[aá]neamente|meanwhile|mientras)\b",
            r"\b(independen\w*|por separado|separately|each (?:one|file|module|package)|cada (?:uno|archivo|m[oó]dulo|paquete))\b",
            r"\b(two|three|2|3|dos|tres)\s+(?:different|distint\w*|separate|hip[oó]tesis|approaches|enfoques|opciones|concepts|conceptos)\b",
        ),
    ):
        signals.append("natural_concurrency")
        score += 0.40

    # User wants agents — natural phrasing, not jargon.
    multi_agent_ask = _matches(
        text,
        (
            r"\b(varios|m[uú]ltiples|multiple|several|more than one)\s+agentes?\b",
            r"\b(agentes?\s+(?:en\s+paralelo|especializad\w*|separad\w*))\b",
            r"\b(with|con)\s+(?:several|multiple|varios|m[uú]ltiples)\s+agents?\b",
            r"\b(multi[- ]?agent|multiagente|multi[- ]?agente)s?\b",
            r"\b(sub-?agents?|subagentes?)\b",
        ),
    )
    if multi_agent_ask:
        signals.append("user_multi_agent_request")
        score += 0.45

    research_then_impl = _matches(
        text,
        (
            r"\b(research|investiga|investigar|explora|scout|trends?|tendencias?)\b.{0,80}\b(then|luego|y (?:despu[eé]s|luego)|after that|implement|implementa|build|crea|diseña)\b",
            r"\b(first|primero)\b.{0,40}\b(research|investiga|explora)\b",
        ),
    )
    if research_then_impl:
        signals.append("research_then_implement")
        score += 0.25

    review_and_fix = _matches(
        text,
        (
            r"\b(review|revisa|revisar|audit|audita)\b.{0,80}\b(fix|arregla|arreglar|correct|corrige)\b",
            r"\b(fix|arregla|arreglar)\b.{0,80}\b(review|revisi[oó]n|feedback|issues?|problemas?)\b",
        ),
    )
    if review_and_fix:
        signals.append("review_and_fix")
        score += 0.25

    alternatives = _matches(
        text,
        (
            r"\b(two|2|dos|three|3|tres)\s+(?:architectures?|arquitecturas?|designs?|diseños?|approaches|enfoques|options|opciones)\b",
            r"\b(compare|compara|compara(?:r)?)\b.{0,40}\b(approaches|enfoques|options|opciones|architectures?)\b",
        ),
    )
    if alternatives:
        signals.append("alternative_exploration")
        score += 0.40

    # Soft coupling penalty: single shared contract language.
    if _matches(
        text,
        (
            r"\b(same (?:file|module|contract)|mismo (?:archivo|m[oó]dulo|contrato)|integrat(?:e|ion)|integrar)\b",
            r"\b(tightly coupled|fuertemente acoplad\w*)\b",
        ),
    ):
        signals.append("coupling_signal")
        score -= 0.25

    score = max(0.0, min(1.0, score))
    return {
        "score": round(score, 2),
        "signals": signals,
        "paths": unique_paths,
        "domains": domains,
        "multi_agent_ask": multi_agent_ask,
    }


def _delegation_requested(text: str) -> bool:
    """True when ordinary language already implies independent or multi-unit work."""
    info = _parallelism_signals(text)
    return info["score"] >= 0.35 or info["multi_agent_ask"]


def _infer_risk(text: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    action_boundary = r"(?:^|[.;:\n]|\bthen\b|\binstead\b|\band\b|\by luego\b|\bdespués\b|\by\b)\s*(?:please\s+|por favor\s+)?"
    presentation_only = _presentation_only(text)
    explanatory = _explanatory_requested(text)
    implementation_requested = _implementation_requested(text)
    documentation = _matches(
        text, (r"^\s*(document|documenta|documentar|añade documentación)\b",)
    )
    explicitly_not_requested = _matches(
        text,
        (
            r"^\s*(do not|don't|never)\b.{0,80}\b(restore|delete|drop|chmod|chown|deploy|rotate)\b",
            r"^\s*(no|nunca)\b.{0,80}\b(restaures?|restaurar|elimines?|eliminar|borres?|borrar|ejecutes?|ejecutar|despliegues?|desplegar|rotes?|rotar)\b",
        ),
    )
    destructive_action = _matches(
        text,
        (
            action_boundary + r"(?:drop|truncate|destroy|delete|wipe|purge)\b.{0,50}\b(?:databases?|tables?|schemas?|data|records?|files?|directories|accounts?|backups?|credentials?|secrets?)\b",
            action_boundary + r"(?:elimina|eliminar|borra|borrar|destruye|destruir|trunca|truncar)\b.{0,50}\b(?:bases? de datos|tablas?|esquemas?|datos|registros?|archivos?|directorios?|cuentas?|backups?|copias? de seguridad|credenciales?|secretos?)\b",
            action_boundary + r"rm\s+-[^\n;]*(?:r|f)[^\n;]*\s+/",
            action_boundary + r"[^.;]{0,80}\b(irreversible|sin posibilidad de recuperación)\b",
        ),
    )
    production_action = _matches(
        text,
        (
            action_boundary + r"(change|modify|deploy|release|run|execute|apply|restore|delete|drop)\b.{0,80}\b(prod|production(?![- ]?like\b)|live (?:environment|system|database|service|site))\b",
            action_boundary + r"(haz|hacer|cambia|cambiar|modifica|modificar|despliega|desplegar|ejecuta|ejecutar|aplica|aplicar|restaura|restaurar|elimina|eliminar)\b.{0,80}\bproducción\b",
        ),
    )
    backup_action = _matches(
        text,
        (
            action_boundary + r"(restore|restores|restoring|delete|remove|overwrite)\b.{0,50}\bbackups?\b",
            action_boundary + r"(restaura|restaurar|elimina|eliminar|sobrescribe|sobrescribir)\b.{0,50}\b(backups?|copia(?:s)? de seguridad)\b",
        ),
    )
    credential_action = _matches(
        text,
        (
            action_boundary + r"(rotate|revoke|delete|replace|expose|change)\b.{0,50}\b(credentials?|secrets?|api[_ -]?keys?|passwords?)\b",
            action_boundary + r"(rota|rotar|revoca|revocar|elimina|eliminar|reemplaza|reemplazar|expone|cambia|cambiar)\b.{0,50}\b(credenciales?|secretos?|claves? api|contraseñas?)\b",
        ),
    )
    permission_action = _matches(
        text,
        (
            action_boundary + r"(?:(?:run|execute|apply|change)\b.{0,30})?(chmod|chown)\b",
            action_boundary + r"(run|execute|apply|change)\b.{0,50}\b(iam|critical permissions?)\b",
            action_boundary + r"(?:(?:ejecuta|ejecutar|aplica|aplicar|cambia|cambiar)\b.{0,30})?(chmod|chown)\b",
            action_boundary + r"(ejecuta|ejecutar|aplica|aplicar|cambia|cambiar)\b.{0,50}\b(iam|permisos? críticos?)\b",
        ),
    )
    data_loss = _matches(
        text,
        (
            action_boundary + r"(?:cause|risk|accept|provoca|causa|acepta)\b.{0,40}\b(?:data\s*loss|pérdida\s+de\s+datos)\b",
        ),
    )
    if any(
        (
            destructive_action,
            production_action,
            backup_action,
            credential_action,
            permission_action,
            data_loss,
        )
    ):
        reasons.append("detecté una acción real irreversible, de producción o de control crítico")
        return "RISK_4", reasons

    if explanatory and not implementation_requested:
        return "RISK_0", ["parece una explicación sin una operación solicitada"]
    if documentation:
        return "RISK_1", ["parece documentación sin una operación solicitada"]
    if explicitly_not_requested:
        return "RISK_0", ["el texto rechaza explícitamente ejecutar la operación"]

    high_impact = _matches(
        text,
        (
            r"auth|login|logout|sesión|session|authorization|autorización|permission|permiso",
            r"payment|pago|billing|factur",
            r"pii|personal data|datos personales|secret|secreto|credential|credencial",
            r"migration|migración|deploy|desplieg|infrastructure|infraestructura",
            r"public api|api pública|api contract|contrato de api",
            r"concurren|race condition|rollback|base de datos|database",
        ),
    )
    if high_impact and not presentation_only:
        return "RISK_3", reasons + ["detecté impacto en seguridad, persistencia o infraestructura"]
    if explanatory or _matches(text, (r"brainstorm|question|pregunta",)):
        return "RISK_0", ["parece una explicación o conversación sin cambio real"]
    if _matches(text, (r"css|rename|renombr|format|formato|document|documentación|copy|texto|typo",)):
        return "RISK_1", ["parece un cambio localizado y reversible"]
    if _matches(text, (r"feature|funcionalidad|implement|arregla|fix|bug|refactor|test|prueba|integrat",)):
        return "RISK_2", ["parece desarrollo estándar con posible regresión"]
    return "RISK_2", ["tarea no reconocida; se conserva un nivel conservador por defecto"]


def _category(text: str, risk: str) -> str:
    if risk == "RISK_0" and _explanatory_requested(text):
        return "explanation"
    # Order matters: testing/marketing/design beat generic database keyword collisions
    # (e.g. "TDD for the backup service" is testing, not a restore operation).
    patterns = (
        ("marketing", r"marketing|cro|seo|copy|landing|conversion|analytics|analítica|growth"),
        ("design", r"design|diseño|visual|screenshot|captura|ui estética|redesign"),
        ("testing", r"\btdd\b|test-driven|tests?\s+first|red-green|coverage|cobertura|\btests?\b|\bpruebas?\b|eval|benchmark"),
        ("bug", r"bug|fix|error|falla|fallo|debug|depura"),
        ("security", r"auth|login|security|seguridad|secret|credential|permission|autorización"),
        (
            "database",
            r"database|base de datos|\bsql\b|schema|esquema|migration|migración|"
            r"\btablas?\b|\btables?\b|"
            r"\b(restore|restaura|restaurar|restoring)\b.{0,40}\b(backup|copia|backups?)|"
            r"\b(backup|backups?|copia de seguridad)\b.{0,40}\b(restore|restaura|restaurar|delete|elimina|eliminar|drop)|"
            r"\b(postgres|postgresql|psql|supabase|sqlite)\b",
        ),
        # Word boundaries required: bare "ui" must not match inside "arquitectura".
        ("frontend", r"\b(frontend|front-end|ui|css|react|component|web|browser)\b"),
        ("documentation", r"\b(document\w*|readme|docs|texto|copy|writing|escritura)\b"),
        ("explanation", r"\b(explain|explica|qué es|what is|how to|cómo|question|pregunta)\b"),
    )
    for name, pattern in patterns:
        if _matches(text, (pattern,)):
            return name
    return "security" if risk in {"RISK_3", "RISK_4"} else "engineering"


def _complexity(text: str, risk: str) -> str:
    if risk == "RISK_4":
        return "critical"
    if risk == "RISK_3":
        return "large" if _matches(text, (r"architect|arquitect|migration|migración|deploy|infra",)) else "medium"
    if risk == "RISK_0":
        return "trivial"
    if risk == "RISK_1":
        return "trivial"
    return "small" if _matches(text, (r"bug|fix|feature|funcionalidad|small|pequeñ",)) else "medium"


def _content_types(text: str) -> list[str]:
    found: list[str] = []
    checks = (
        ("secrets", r"secret|secreto|token|api[_ -]?key|password|contraseña|credential|credencial|\.env"),
        ("pipelines", r"\||\bpipe\b|pipeline|2>&1|&&|;|>\s*[^=]"),
        ("diff", r"git\s+diff|^@@\s+-?\d|diff --git|before.*after"),
        ("commands", r"\b(bash|shell|command|comando|run|ejecuta|drop|delete|truncate)\b"),
        ("errors", r"error|exception|stack\s*trace|traceback|stderr|failure|fallo"),
        ("sql", r"\b(select|insert|update|delete|drop|alter|create)\b.{0,80}\b(table|database|tabla|schema)\b"),
        ("json", r"\bjson\b|\{.*\}|\[.*\]"),
        ("logs", r"\blogs?\b|stdout|salida de tests|test output"),
        ("code", r"\b(code|código|source|fuente|css|typescript|javascript|python|script)\b|\.(ts|tsx|js|py|css)\b"),
        ("prose", r"text|texto|document|documentación|explain|explica|copy|writing"),
    )
    for name, pattern in checks:
        if _matches(text, (pattern,)):
            found.append(name)
    return found or ["unknown"]


def _recommended_skill_ids(text: str, category: str, risk: str) -> list[str]:
    selected: list[str] = []
    if risk in {"RISK_3", "RISK_4"}:
        selected.extend(["security-hardening", "architect-orchestrator"])
    if category == "marketing":
        # Curated in-repo skill first; external marketingskills remains optional.
        selected.extend(
            ["marketing-and-growth", "design-taste-frontend", "marketingskills"]
        )
    elif category == "design":
        selected.extend(["frontend-ui-engineering", "design-taste-frontend"])
    elif category == "documentation" and _matches(
        text, (r"public|público|copy|writing|texto",)
    ):
        selected.append("no-ai-slop")
        selected.append("anti-ai-slop-writing")
    else:
        if category == "bug":
            selected.append("debugging-and-error-recovery")
        if category == "testing":
            selected.append("test-driven-development")
        if category == "database":
            selected.append("supabase-postgres-best-practices")
        if category == "frontend":
            selected.append("frontend-ui-engineering")

    # Cross-cutting signals (stack; do not early-return away from these).
    if _matches(
        text,
        (
            r"\btdd\b",
            r"test-driven",
            r"tests?\s+first",
            r"red-green",
            r"pruebas?\s+primero",
            r"\b(unittest|pytest|jest|vitest)\b",
        ),
    ):
        selected.append("test-driven-development")
    if _matches(text, (r"landing|portfolio|hero section|rediseño visual|visual redesign",)):
        selected.append("design-taste-frontend")
    if _matches(text, (r"context|contexto|token|compresión|compression|memory|memoria",)):
        selected.append("context-engineering")
    if (
        risk != "RISK_0"
        and not _explanatory_requested(text)
        and (
            _implementation_requested(text)
            or category in {"bug", "testing", "frontend", "database", "security", "marketing", "design"}
            or _matches(text, (r"\b(implement|arregla|fix|añade|agrega|refactor|ship|deploy)\b",))
        )
    ):
        selected.append("verification-before-completion")
        selected.append("verification-gauntlet")
    if _agentit_activation_requested(text):
        selected.append("using-agentit")
    if _matches(
        text,
        (
            r"\bgauntlet\b",
            r"\bagentit verify\b",
            r"verification gauntlet",
            r"anti-greenwash",
            r"mutation test",
        ),
    ):
        selected.append("verification-gauntlet")
    return list(dict.fromkeys(selected))


def _entry_available(
    skill_id: str,
    entries: dict[str, dict[str, Any]],
    *,
    registry_path: Path,
    home: Path,
    resolving: set[str] | None = None,
) -> bool:
    entry = entries.get(skill_id)
    if entry is None:
        raise RegistryError(f"router candidate is absent from registry: {skill_id}")
    if entry["state"] not in AVAILABLE_REGISTRY_STATES:
        return False
    paths = entry["paths"]
    if not paths or not any(
        _path_is_loadable(
            entry,
            resolve_registry_path(template, registry_path=registry_path, home=home),
        )
        for template in paths
    ):
        return False

    chain = set() if resolving is None else set(resolving)
    if skill_id in chain:
        raise RegistryError(f"essential dependency cycle involving {skill_id}")
    chain.add(skill_id)
    for dependency_id in entry["essential_dependencies"]:
        if dependency_id not in entries:
            raise RegistryError(
                f"essential dependency for {skill_id} is absent: {dependency_id}"
            )
        if not _entry_available(
            dependency_id,
            entries,
            registry_path=registry_path,
            home=home,
            resolving=chain,
        ):
            return False
    return True


def _resolve_skill_recommendations(
    candidates: list[str],
    entries: dict[str, dict[str, Any]],
    *,
    registry_path: Path,
    home: Path,
    text: str,
) -> tuple[list[str], list[str], list[str], dict[str, dict[str, Any]]]:
    available: list[str] = []
    missing: list[str] = []
    suppressed_conflicts: list[str] = []
    metadata: dict[str, dict[str, Any]] = {}
    priority_order = {
        "core": 0,
        "on_demand": 1,
        "specialized": 2,
        "optional": 3,
        "experimental": 4,
        "reference": 5,
    }
    cost_order = {"low": 0, "medium": 1, "high": 2, "unknown": 3}

    def cost_rank(value: Any) -> int:
        if not isinstance(value, str):
            return 99
        return next((rank for prefix, rank in cost_order.items() if value.startswith(prefix)), 99)

    ordered_candidates = sorted(
        candidates,
        key=lambda skill_id: (
            priority_order.get(entries.get(skill_id, {}).get("priority"), 99),
            cost_rank(entries.get(skill_id, {}).get("context_cost")),
            candidates.index(skill_id),
        ),
    )
    for skill_id in ordered_candidates:
        entry = entries.get(skill_id)
        if entry is None:
            raise RegistryError(f"router candidate is absent from registry: {skill_id}")
        signals = entry.get("requires_signals_any", [])
        if signals and not any(
            re.search(rf"\b{re.escape(signal)}\b", text, re.IGNORECASE)
            for signal in signals
        ):
            continue
        metadata[skill_id] = {
            "priority": entry.get("priority"),
            "context_cost": entry.get("context_cost"),
            "execution_cost": entry.get("execution_cost"),
            "conflicts": entry.get("conflicts", []),
            "trigger": entry.get("trigger"),
            "avoid_when": entry.get("avoid_when"),
        }
        is_available = _entry_available(
            skill_id,
            entries,
            registry_path=registry_path,
            home=home,
        )
        conflicts_with_available = set(entry["conflicts_with"]).intersection(available)
        available_conflicts_with_current = any(
            skill_id in entries[selected_id]["conflicts_with"]
            for selected_id in available
        )
        if is_available and (
            conflicts_with_available or available_conflicts_with_current
        ):
            suppressed_conflicts.append(skill_id)
            continue
        target = available if is_available else missing
        target.append(skill_id)
    return available, missing, suppressed_conflicts, metadata


def _topology(text: str, risk: str, parallelism: dict[str, Any] | None = None) -> str:
    """Choose an execution shape from structure and risk, not jargon powerwords."""
    info = parallelism if parallelism is not None else _parallelism_signals(text)
    investigation = _matches(
        text,
        (
            r"\b(probe|investiga|reproduce|localiza|root cause|causa raíz)\b",
            r"\b(trace the|trace this|trazar|rastrear|diagnos[ea])\b",
        ),
    )
    # Parallel investigation of independent hypotheses → fan_out of probes.
    if investigation and (
        "natural_concurrency" in info["signals"]
        or "alternative_exploration" in info["signals"]
        or info["score"] >= 0.45
    ):
        return "fan_out"
    if investigation and not _implementation_requested(text):
        return "probe"
    if _matches(
        text,
        (
            r"\b(pipeline|etapas secuenciales|sequential stages)\b",
            r"\b(then|luego|despu[eé]s)\b.{0,40}\b(then|luego|despu[eé]s)\b",
        ),
    ) or "research_then_implement" in info["signals"]:
        if "research_then_implement" in info["signals"]:
            return "pipeline"
        if _matches(text, (r"pipeline|sequential stages|etapas secuenciales",)):
            return "pipeline"
    if info["score"] >= 0.35 or info["multi_agent_ask"]:
        # Independent units win over collapsing into a single writer, even at RISK_3,
        # unless the work is one coupled sensitive implementation without multi-unit signals.
        multi_unit = any(
            s.startswith("multi_path")
            or s.startswith("domain_pair")
            or s in {"natural_concurrency", "alternative_exploration", "user_multi_agent_request"}
            for s in info["signals"]
        )
        if multi_unit:
            return "fan_out"
    if risk == "RISK_4":
        return "audit"
    if risk == "RISK_3":
        if _implementation_requested(text):
            return "writer_reviewer"
        return "audit"
    if "review_and_fix" in info["signals"]:
        return "writer_reviewer"
    return "direct"


def _subagent_budget(
    text: str,
    risk: str,
    topology: str,
    parallelism: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Soft advisory budget — no hard min/max caps. recommended is guidance only."""
    info = parallelism if parallelism is not None else _parallelism_signals(text)
    score = float(info.get("score") or 0.0)

    if risk in {"RISK_0"} and topology == "direct":
        return {
            "recommended": 0,
            "soft_max_hint": None,
            "max": None,
            "requires_justification": False,
            "hard_cap": False,
            "rationale": "explanation/conversation; no delegation needed",
        }

    if topology == "audit":
        return {
            "recommended": 1,
            "soft_max_hint": None,
            "max": None,
            "requires_justification": True,
            "hard_cap": False,
            "rationale": "independent safety review",
        }

    if topology == "writer_reviewer":
        recommended = 1
        if "review_and_fix" in info["signals"]:
            recommended = 1
        return {
            "recommended": recommended,
            "soft_max_hint": None,
            "max": None,
            "requires_justification": True,
            "hard_cap": False,
            "rationale": "one writer plus independent review",
        }

    if topology == "fan_out":
        units = 2
        if any(s.startswith("multi_path:") for s in info["signals"]):
            for s in info["signals"]:
                if s.startswith("multi_path:"):
                    try:
                        units = max(units, int(s.split(":")[1]))
                    except ValueError:
                        pass
        if any(s.startswith("domain_pair:") for s in info["signals"]):
            domains = info.get("domains") or []
            units = max(units, len(domains))
        if "alternative_exploration" in info["signals"]:
            units = max(units, 2)
        recommended = max(2, min(units, 5))
        return {
            "recommended": recommended,
            "soft_max_hint": None,
            "max": None,
            "requires_justification": True,
            "hard_cap": False,
            "rationale": f"independent units suggested (~{recommended}); spawn only with clear ownership",
        }

    if topology == "pipeline":
        return {
            "recommended": 1,
            "soft_max_hint": None,
            "max": None,
            "requires_justification": True,
            "hard_cap": False,
            "rationale": "staged work; optional probe/research stage before implement",
        }

    if topology == "probe":
        recommended = 1 if score >= 0.35 else 0
        return {
            "recommended": recommended,
            "soft_max_hint": None,
            "max": None,
            "requires_justification": recommended > 0,
            "hard_cap": False,
            "rationale": "read-only investigation; isolate when context would pollute implementation",
        }

    # direct: still allow advisory spawn when score is high but topology stayed direct
    if score >= 0.55 and risk not in {"RISK_0", "RISK_1"}:
        return {
            "recommended": 1,
            "soft_max_hint": None,
            "max": None,
            "requires_justification": True,
            "hard_cap": False,
            "rationale": "possible specialist isolation; agent decides",
        }
    return {
        "recommended": 0,
        "soft_max_hint": None,
        "max": None,
        "requires_justification": False,
        "hard_cap": False,
        "rationale": "no clear multi-unit benefit; stay single-agent unless new evidence appears",
    }


def _domain_pack(category: str, text: str) -> str:
    if _matches(text, (r"\b(landing|portfolio|hero|rediseño visual|visual redesign|brand experience)\b",)):
        return "design"
    if _matches(text, (r"\b(postgres|postgresql|supabase|sql|schema|migración)\b",)):
        return "data"
    if _matches(text, (r"\b(ci|cd|deploy|release|docker|kubernetes)\b",)):
        return "release"
    return DOMAIN_PACK_BY_CATEGORY.get(category, "engineering")


def _craft_depth_applies(domain_pack: str, category: str, text: str) -> bool:
    if domain_pack == "design" or category == "design":
        return True
    return _matches(
        text,
        (
            r"\b(landing|portfolio|hero|rediseño|redesign|visual|ui\s*ux|diseño visual|art direction)\b",
        ),
    )


def _recommend_craft_depth(text: str, risk: str) -> str | None:
    if _matches(text, (r"\b(studio|flagship|premium|ambitious|competition|conceptos? m[uú]ltiples)\b",)):
        return "studio"
    if _matches(text, (r"\b(polished|pulido|portfolio|public[- ]facing|landing|hero)\b",)):
        return "polished"
    if risk in {"RISK_0", "RISK_1"}:
        return "standard"
    return "polished"


def _recommend_spend(risk: str, complexity: str, parallelism: dict[str, Any]) -> str:
    if risk in {"RISK_3", "RISK_4"} or complexity in {"large", "critical"}:
        return "thorough"
    if parallelism.get("score", 0) >= 0.45 or complexity == "medium":
        return "normal"
    return "lean"


def _critic_required(text: str, risk: str, topology: str, parallelism: dict[str, Any]) -> bool:
    if _structural_plan_requested(text):
        return True
    if risk in {"RISK_3", "RISK_4"} and _implementation_requested(text):
        return True
    if topology in {"fan_out", "pipeline", "writer_reviewer"} and parallelism.get("score", 0) >= 0.45:
        return True
    if _matches(
        text,
        (
            r"\b(plan|propuesta|architecture|arquitectura|estructura|migrate|migración|refactor)\b",
        ),
    ) and _matches(
        text,
        (
            r"\b(grande|large|completo|global|sistema|multi|varios|entire|whole)\b",
        ),
    ):
        return True
    return False


def _skill_budget(
    category: str,
    risk: str,
    domain_pack: str,
    recommended_skills: list[str],
) -> dict[str, Any]:
    """Only task-relevant skills plus a tiny always-core set."""
    family = list(CATEGORY_SKILL_FAMILIES.get(category, []))
    task_skills = [s for s in recommended_skills if s not in ALWAYS_CORE_SKILLS]
    # Prefer family order then remaining recommendations.
    ordered: list[str] = []
    for skill in family + task_skills:
        if skill not in ordered and skill in recommended_skills:
            ordered.append(skill)
    for skill in recommended_skills:
        if skill not in ordered and skill not in ALWAYS_CORE_SKILLS:
            ordered.append(skill)
    # Cap bodies aggressively: agent loads these, not the whole catalog.
    max_task_bodies = 4 if risk in {"RISK_3", "RISK_4"} else 3
    load_now = ordered[:max_task_bodies]
    core = [s for s in ALWAYS_CORE_SKILLS if risk != "RISK_0" or s in {"using-agentit", "task-router", "using-agent-skills"}]
    if risk == "RISK_0":
        core = ["using-agentit", "task-router", "using-agent-skills"]
    return {
        "domain_pack": domain_pack,
        "always_core": core,
        "load_now": load_now,
        "do_not_load": "full_catalog",
        "max_task_skill_bodies": max_task_bodies,
        "notes": "Load only always_core + load_now skill bodies. Discover more via using-agent-skills/find-skills if gaps appear.",
    }


def _token_estimate(
    *,
    risk: str,
    complexity: str,
    domain_pack: str,
    topology: str,
    subagents: dict[str, Any],
    craft_depth: str | None,
    spend: str,
    project_signals: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Project-aware rough envelope — not a fixed Standard/Polished/Studio bill."""
    base = {"RISK_0": 3, "RISK_1": 8, "RISK_2": 25, "RISK_3": 45, "RISK_4": 60}.get(risk, 25)
    complexity_bonus = {"trivial": 0, "small": 5, "medium": 15, "large": 35, "critical": 50}.get(
        complexity, 15
    )
    domain_bonus = {
        "design": 20,
        "frontend": 12,
        "product": 10,
        "data": 10,
        "backend": 8,
        "release": 12,
        "research": 15,
        "writing": 5,
        "engineering": 8,
    }.get(domain_pack, 8)
    topo_bonus = {
        "direct": 0,
        "probe": 8,
        "pipeline": 15,
        "writer_reviewer": 18,
        "fan_out": 25,
        "audit": 12,
    }.get(topology, 0)
    recommended = int(subagents.get("recommended") or 0)
    specialist_bonus = recommended * 12
    craft_bonus = {"standard": 0, "polished": 15, "studio": 40}.get(craft_depth or "", 0)
    spend_bonus = {"lean": 0, "normal": 8, "thorough": 20}.get(spend, 8)
    project = project_signals or {}
    size_bonus = int(project.get("size_bonus") or 0)
    low = max(5, int((base + complexity_bonus + domain_bonus + topo_bonus + specialist_bonus + craft_bonus + spend_bonus + size_bonus) * 0.6))
    high = max(low + 10, int((base + complexity_bonus + domain_bonus + topo_bonus + specialist_bonus + craft_bonus + spend_bonus + size_bonus) * 2.2))
    basis = [
        f"risk={risk}",
        f"complexity={complexity}",
        f"domain_pack={domain_pack}",
        f"topology={topology}",
        f"specialists_recommended={recommended}",
        f"spend={spend}",
    ]
    if craft_depth:
        basis.append(f"craft_depth={craft_depth}")
    if project.get("basis"):
        basis.extend(project["basis"])
    return {
        "low_k": low,
        "high_k": high,
        "unit": "approximate_total_model_tokens_thousands",
        "display": f"~{low}k-{high}k total model tokens (rough, project-aware)",
        "basis": basis,
        "not_a_bill": True,
    }


def _pushback_on_multi_agent(parallelism: dict[str, Any], topology: str) -> dict[str, Any] | None:
    if not parallelism.get("multi_agent_ask"):
        return None
    if parallelism.get("score", 0) < 0.35 and topology == "direct":
        return {
            "advise": True,
            "message": (
                "You asked for multiple agents, but this task looks tightly coupled or too small "
                "for coordination overhead. Recommend staying single-agent unless you have "
                "independent packages or want an independent critic."
            ),
        }
    return {
        "advise": False,
        "message": "Multi-agent request aligns with independent units or review needs.",
    }


def _rejected_topologies(selected: str) -> dict[str, str]:
    reasons: dict[str, str] = {}
    for topology in TOPOLOGIES:
        if topology == selected:
            continue
        if selected == "direct":
            reasons = {
                "probe": "no read-only investigation or reproduction request",
                "fan_out": "no independent work units identified",
                "pipeline": "no sequential artifact stages identified",
                "writer_reviewer": "risk does not require independent verification",
                "audit": "no critical review or operational boundary detected",
            }
            break
        if selected == "probe":
            reasons = {
                "direct": "investigation evidence should be isolated before implementation",
                "fan_out": "probe keeps the investigation read-only and bounded",
                "pipeline": "no validated implementation artifacts exist yet",
                "writer_reviewer": "implementation was not requested",
                "audit": "the request is investigation, not a final critical-operation review",
            }
            break
        if selected == "fan_out":
            reasons = {
                "direct": "independent work units were explicitly requested",
                "probe": "the task requests work beyond read-only investigation",
                "pipeline": "the work units do not declare sequential artifact dependencies",
                "writer_reviewer": "parallel ownership is more useful than one writer plus review",
                "audit": "the task does not request a critical-operation audit",
            }
            break
        if selected == "pipeline":
            reasons = {
                "direct": "the task declares ordered stages with dependent artifacts",
                "probe": "the task includes execution stages beyond investigation",
                "fan_out": "stages depend on validated outputs rather than being independent",
                "writer_reviewer": "stage dependencies are primary; review is not the main shape",
                "audit": "no critical-operation review is the primary request",
            }
            break
        if selected == "writer_reviewer":
            reasons = {
                "direct": "independent verification is required for this sensitive implementation",
                "probe": "implementation was requested; investigation alone is insufficient",
                "fan_out": "affected behavior is coupled; no independent ownership boundaries were declared",
                "pipeline": "no sequential artifact stages were declared",
                "audit": "an audit alone would not implement the requested change",
            }
            break
        if selected == "audit":
            reasons = {
                "direct": "the risk or review request requires an independent safety check",
                "probe": "the request is not limited to read-only investigation",
                "fan_out": "the safety decision needs one bounded review owner",
                "pipeline": "no validated sequential artifacts are required for the review",
                "writer_reviewer": "no implementation writer was requested; review-only control is sufficient",
            }
            break
    return reasons


def _signals(
    text: str,
    *,
    risk: str,
    topology: str,
    content_types: list[str],
    routing_advice: list[str],
) -> list[str]:
    signals: list[str] = []
    presentation_only = _presentation_only(text)
    if presentation_only:
        signals.append("presentation-only scope")
    for label, pattern in SENSITIVE_SIGNAL_PATTERNS:
        if risk not in {"RISK_0", "RISK_1"} and _matches(text, (pattern,)) and not presentation_only:
            signals.append(label)
    if risk == "RISK_0":
        signals.append("explanation or conversation without a requested mutation")
    elif risk == "RISK_1" and not signals:
        signals.append("localized reversible change")
    elif risk == "RISK_2" and not signals:
        signals.append("standard development scope with possible regression")
    if _delegation_requested(text):
        signals.append("independent or multi-unit work indicated by ordinary language")
    if topology == "probe":
        signals.append("read-only investigation or reproduction requested")
    if topology == "writer_reviewer":
        signals.append("independent verification useful after implementation")
    if topology == "audit":
        signals.append("independent safety review required before action")
    for content_type in sorted(set(content_types).intersection(CRITICAL_CONTENT)):
        signals.append(f"critical content: {content_type}")
    signals.extend(f"routing advice: {advice}" for advice in routing_advice)
    return list(dict.fromkeys(signals))


def _heuristic_confidence(risk: str, signals: list[str]) -> float:
    """Return an uncalibrated strength score, never a probability claim."""
    if risk == "RISK_4":
        return 0.96
    if risk == "RISK_3":
        return 0.82 if any("boundary" in signal for signal in signals) else 0.70
    if risk == "RISK_1":
        return 0.90 if "presentation-only scope" in signals else 0.76
    if risk == "RISK_0":
        return 0.94
    return 0.62 if len(signals) <= 1 else 0.70


def _model_plan(
    *,
    topology: str,
    critic_required: bool,
    risk: str,
    local_prefs: dict[str, Any] | None,
) -> dict[str, Any]:
    """Capability-tier plan; local models are first-class when configured."""
    local_prefs = local_prefs or {}
    local_enabled = bool(local_prefs.get("enabled", False))
    endpoints = local_prefs.get("endpoints") or []
    if not isinstance(endpoints, list):
        endpoints = []

    def pick(tier: str) -> dict[str, Any]:
        for endpoint in endpoints:
            if not isinstance(endpoint, dict):
                continue
            if str(endpoint.get("tier")) == tier:
                return {
                    "tier": tier,
                    "endpoint_id": endpoint.get("id"),
                    "model": endpoint.get("model"),
                    "base_url": endpoint.get("base_url"),
                    "local": True,
                    "tools": bool(endpoint.get("tools", True)),
                    "context_tokens": endpoint.get("context_tokens"),
                }
        return {
            "tier": tier,
            "endpoint_id": None,
            "model": None,
            "local": False,
            "notes": "no matching local endpoint; use provider default for tier",
        }

    parent_tier = "judgment" if risk in {"RISK_3", "RISK_4"} or critic_required else "coding"
    worker_tier = "fast" if topology in {"probe", "fan_out"} else "coding"
    critic_tier = "critic"
    plan = {
        "catalog": "models/capabilities.yaml",
        "local_enabled": local_enabled,
        "parent": pick(parent_tier) if local_enabled else {"tier": parent_tier, "local": False},
        "worker": pick(worker_tier) if local_enabled else {"tier": worker_tier, "local": False},
        "critic": pick(critic_tier) if local_enabled else {"tier": critic_tier, "local": False},
        "rules": [
            "Local endpoints may be used when they meet the role tier and tool needs.",
            "Do not silently assign RISK_3/4 critic work to an unproven weak local model.",
            "Disclose when falling back from local to cloud or parent execution.",
        ],
    }
    if risk in {"RISK_3", "RISK_4"} and local_enabled:
        critic = plan["critic"]
        if critic.get("local") and not critic.get("tools", True):
            plan["critic"] = {
                "tier": "critic",
                "local": False,
                "notes": "local critic lacks tools; prefer stronger/cloud critic for RISK_3/4",
            }
    return plan


def route_task(
    prompt: str,
    explicit_risk: str | None = None,
    *,
    registry_path: Path | None = None,
    home: Path | None = None,
    project_root: Path | None = None,
    craft_depth_override: str | None = None,
    spend_override: str | None = None,
    parallelism_override: str | None = None,
    topology_override: str | None = None,
) -> dict[str, Any]:
    resolved_registry_path = (
        Path(registry_path) if registry_path is not None else DEFAULT_REGISTRY_PATH
    )
    resolved_home = Path(home) if home is not None else Path.home()
    registry_entries = load_registry(resolved_registry_path)
    text = prompt.strip()
    inferred, reasons = _infer_risk(text.lower())
    risk = inferred
    if explicit_risk in RISK_ORDER:
        if RISK_ORDER[explicit_risk] < RISK_ORDER[inferred]:
            reasons.append("el riesgo explícito no puede reducir el riesgo inferido")
        else:
            risk = explicit_risk
            reasons.append("usé el riesgo explícito porque no rebaja el suelo detectado")

    category = _category(text.lower(), risk)
    complexity = _complexity(text.lower(), risk)
    content_types = _content_types(text.lower())
    routing_advice: list[str] = []

    try:
        from router.project_signals import collect_project_signals
    except ImportError:
        from project_signals import collect_project_signals  # type: ignore
    project_signals = collect_project_signals(project_root)
    if category == "database" and not _matches(
        text,
        (
            r"\b(postgres(?:ql)?|psql|supabase|sqlite|mysql|mariadb|mongodb|mongo|oracle|sql server|mssql|cockroachdb|dynamodb|redis)\b",
        ),
    ):
        routing_advice.append("inspect_database_stack")
    critical = risk in {"RISK_3", "RISK_4"} or bool(CRITICAL_CONTENT.intersection(content_types))
    prefs = load_preferences(resolved_home / ".agentit" / "preferences.yaml")
    user_style_prefs = prefs.get("user_style_preferences", {})
    response_style = user_style_prefs.get("response_style", "terse")

    if risk in {"RISK_0", "RISK_1"}:
        output_profile = "TERSE_SAFE"
    elif risk == "RISK_2":
        output_profile = "TERSE_SAFE" if response_style == "terse" else "STANDARD"
    else:
        output_profile = "VERBOSE_ALLOWED"

    if risk == "RISK_4":
        compression = {
            "enabled": False,
            "mode": "FULL_FIDELITY",
            "allowed": [],
            "semantic": False,
            "deny_reasons": sorted(CRITICAL_CONTENT),
        }
    elif critical:
        compression = {
            "enabled": False,
            "mode": "PRESERVE_CRITICAL_CONTENT",
            "allowed": ["exact_dedup"],
            "semantic": False,
            "deny_reasons": sorted(CRITICAL_CONTENT.intersection(content_types)),
        }
    elif risk == "RISK_2":
        compression = {
            "enabled": True,
            "mode": "SELECTIVE_REVERSIBLE",
            "allowed": ["exact_dedup", "tool_filtering", "artifact_references", "output_terse"],
            "semantic": False,
            "deny_reasons": [],
            "engines": {
                "exact_dedup": "router.dedup.ContextDeduplicator",
                "tool_filtering": "router.tool_filter.filter_tool_output",
                "artifact_references": "router.artifact_ref.create_artifact_reference",
            },
        }
    else:
        compression = {
            "enabled": True,
            "mode": "SAFE_STRUCTURAL",
            "allowed": ["exact_dedup", "tool_filtering", "artifact_references", "output_terse"],
            "semantic": False,
            "deny_reasons": [],
            "engines": {
                "exact_dedup": "router.dedup.ContextDeduplicator",
                "tool_filtering": "router.tool_filter.filter_tool_output",
                "artifact_references": "router.artifact_ref.create_artifact_reference",
            },
        }

    verification = {
        "tests_required": risk != "RISK_0",
        "targeted": risk in {"RISK_1", "RISK_2"},
        "full_suite": risk in {"RISK_3", "RISK_4"},
        "independent_review": risk in {"RISK_3", "RISK_4"},
        "backup_required": risk == "RISK_4",
        "dry_run_required": risk == "RISK_4",
        "post_check_required": risk in {"RISK_3", "RISK_4"},
    }
    lowered = text.lower()
    parallelism = _parallelism_signals(lowered)
    (
        skills_available,
        skills_recommended_missing,
        skills_suppressed_conflicts,
        skill_recommendation_metadata,
    ) = _resolve_skill_recommendations(
        _recommended_skill_ids(lowered, category, risk),
        registry_entries,
        registry_path=resolved_registry_path,
        home=resolved_home,
        text=lowered,
    )
    topology = _topology(lowered, risk, parallelism)
    if topology_override in TOPOLOGIES:
        topology = topology_override
        reasons.append(f"topology override applied: {topology_override}")
    subagents = _subagent_budget(lowered, risk, topology, parallelism)
    domain_pack = _domain_pack(category, lowered)
    # Prefer stack markers from the real project when present.
    markers = set(project_signals.get("stack_markers") or [])
    if "supabase" in markers and domain_pack == "engineering":
        domain_pack = "data"
    elif "typescript" in markers or "node" in markers:
        if category == "frontend":
            domain_pack = "frontend"
    craft_applies = _craft_depth_applies(domain_pack, category, lowered)
    craft_depth = _recommend_craft_depth(lowered, risk) if craft_applies else None
    if craft_depth_override in {"standard", "polished", "studio"}:
        if craft_applies or craft_depth_override:
            craft_depth = craft_depth_override
            craft_applies = True
            reasons.append(f"craft_depth override: {craft_depth_override}")
    spend = _recommend_spend(risk, complexity, parallelism)
    if spend_override in {"lean", "normal", "thorough"}:
        spend = spend_override
        reasons.append(f"spend override: {spend_override}")
    critic_required = _critic_required(lowered, risk, topology, parallelism)
    # Large structural plans always get an independent critic slot in the advisory budget.
    if critic_required and int(subagents.get("recommended") or 0) < 1:
        subagents = dict(subagents)
        subagents["recommended"] = 1
        subagents["requires_justification"] = True
        subagents["rationale"] = (
            (subagents.get("rationale") or "") + "; independent critic required before committing large plan"
        ).strip("; ").strip()
    all_skill_ids = list(
        dict.fromkeys(skills_available + skills_recommended_missing)
    )
    skill_budget = _skill_budget(category, risk, domain_pack, all_skill_ids)
    token_estimate = _token_estimate(
        risk=risk,
        complexity=complexity,
        domain_pack=domain_pack,
        topology=topology,
        subagents=subagents,
        craft_depth=craft_depth,
        spend=spend,
        project_signals=project_signals,
    )
    multi_agent_pushback = _pushback_on_multi_agent(parallelism, topology)
    signals = _signals(
        lowered,
        risk=risk,
        topology=topology,
        content_types=content_types,
        routing_advice=routing_advice,
    )
    for item in parallelism.get("signals") or []:
        signals.append(f"parallelism: {item}")
    if critic_required:
        signals.append("critic required for structural/high-impact plan")
    if craft_depth:
        signals.append(f"craft depth applies: {craft_depth}")
    signals = list(dict.fromkeys(signals))

    prefs = load_preferences(resolved_home / ".agentit" / "preferences.yaml")
    auto_jit_enabled = bool(prefs.get("auto_jit_profiles", True))
    auto_plan_enabled = bool(prefs.get("auto_plan_mode", True))
    parallelism_preference = parallelism_override or prefs.get(
        "parallelism_preference", "medium"
    )
    if parallelism_override:
        reasons.append(f"parallelism preference override: {parallelism_override}")
    # Soft threshold shift by preference (still no hard caps).
    pref_shift = {"low": 0.15, "medium": 0.0, "high": -0.10, "max": -0.20}.get(
        str(parallelism_preference), 0.0
    )
    if pref_shift and topology == "direct" and float(parallelism.get("score") or 0) >= (
        0.35 + pref_shift
    ):
        topology = "fan_out"
        subagents = _subagent_budget(lowered, risk, topology, parallelism)
        if critic_required and int(subagents.get("recommended") or 0) < 1:
            subagents = dict(subagents)
            subagents["recommended"] = 1
            subagents["requires_justification"] = True
        token_estimate = _token_estimate(
            risk=risk,
            complexity=complexity,
            domain_pack=domain_pack,
            topology=topology,
            subagents=subagents,
            craft_depth=craft_depth,
            spend=spend,
            project_signals=project_signals,
        )
        multi_agent_pushback = _pushback_on_multi_agent(parallelism, topology)
        reasons.append("parallelism preference raised topology to fan_out")
    local_models = prefs.get("local_models") if isinstance(prefs.get("local_models"), dict) else {}
    models = _model_plan(
        topology=topology,
        critic_required=critic_required,
        risk=risk,
        local_prefs=local_models,
    )
    # Evidence-based verification contract attached to the route.
    verification = {
        **verification,
        "evidence_required": risk != "RISK_0",
        "fresh_command_output": risk != "RISK_0",
        "critic_before_large_plan": critic_required,
        "receipt_path_hint": ".agentit/verify/",
        "anti_greenwash": True,
        "claims_without_evidence": "forbidden",
    }

    jit_profiles: list[str] = []
    unmapped_skills: list[str] = []
    if auto_jit_enabled:
        mapped_set = set()
        postgres_stack = _matches(
            lowered,
            (r"\b(postgres(?:ql)?|psql|supabase|cockroachdb)\b",),
        ) or "supabase" in markers
        pack_profile = {
            "design": "design",
            "frontend": "frontend",
            "backend": "backend",
            "data": "supabase" if postgres_stack else "backend",
            "product": "product",
            "writing": "writing",
            "release": "release",
            "research": "research",
            "engineering": "core",
        }.get(domain_pack)
        if pack_profile and pack_profile != "core":
            mapped_set.add(pack_profile)
        for skill in skills_recommended_missing:
            if skill in SKILL_PROFILE_MAP:
                mapped_set.add(SKILL_PROFILE_MAP[skill])
            else:
                unmapped_skills.append(skill)
        jit_profiles = sorted(mapped_set)

    auto_plan_recommended = (
        (risk in {"RISK_2", "RISK_3", "RISK_4"} or topology != "direct" or critic_required)
        if auto_plan_enabled
        else (risk in {"RISK_3", "RISK_4"})
    )

    applied_prefs = {
        "preferred_language": prefs.get("user_style_preferences", {}).get("preferred_language", "es"),
        "testing_framework": prefs.get("user_style_preferences", {}).get("testing_framework", "pytest"),
        "ui_styling": prefs.get("user_style_preferences", {}).get("ui_styling", "vanilla_css_oklch"),
        "response_style": response_style,
        "parallelism_preference": parallelism_preference,
    }

    return {
        "risk": risk,
        "category": category,
        "complexity": complexity,
        "content_types": content_types,
        "domain_pack": domain_pack,
        "craft_depth": craft_depth,
        "craft_depth_applies": craft_applies,
        "spend": spend,
        "skill_budget": skill_budget,
        "token_estimate": token_estimate,
        "parallelism": {
            "score": parallelism.get("score"),
            "signals": parallelism.get("signals"),
            "paths": parallelism.get("paths"),
            "domains": parallelism.get("domains"),
            "preference": parallelism_preference,
        },
        "critic_required": critic_required,
        "multi_agent_pushback": multi_agent_pushback,
        "project_signals": project_signals,
        "models": models,
        "continuity": {
            "state_path": "docs/agentit/STATE.md",
            "checkpoint_dir": ".agentit/checkpoints",
            "resume_required_before_reinterview": True,
            "mid_task_reroute": True,
        },
        "skills": skills_available,
        "skills_available": skills_available,
        "skills_recommended_missing": skills_recommended_missing,
        "skills_suppressed_conflicts": skills_suppressed_conflicts,
        "skill_recommendation_metadata": skill_recommendation_metadata,
        "routing_advice": routing_advice,
        "signals": signals,
        "confidence": _heuristic_confidence(risk, signals),
        "confidence_calibrated": False,
        "rejected_topologies": _rejected_topologies(topology),
        "output_profile": output_profile,
        "compression": compression,
        "topology": topology,
        "subagents": subagents,
        "verification": verification,
        "auto_plan_mode_recommended": auto_plan_recommended,
        "jit_profile_recommendations": jit_profiles,
        "unmapped_skills": unmapped_skills,
        "applied_preferences": applied_prefs,
        "activation": {
            "requested": _agentit_activation_requested(lowered),
            "agentit_mentioned": _agentit_mentioned(lowered),
            "powerwords_required": False,
            "notes": "Only affirmative natural Agentit activation is special-cased; bare or negated mentions do not activate it.",
        },
        "reversible": True if risk in {"RISK_0", "RISK_1", "RISK_2"} else None,
        "recovery": (
            "not proven; retrieve originals before RISK_3/RISK_4 actions"
            if risk in {"RISK_3", "RISK_4"}
            else "not needed"
        ),
        "reasons": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify an agent task (intelligent orchestration; no powerwords)."
    )
    parser.add_argument("prompt", nargs="*", help="task text")
    parser.add_argument("--risk", choices=sorted(RISK_ORDER), dest="explicit_risk")
    parser.add_argument("--file", type=Path, help="read the task text from a UTF-8 file")
    parser.add_argument("--registry", type=Path, help="portable registry path")
    parser.add_argument("--home", type=Path, help="HOME used for bounded path discovery")
    parser.add_argument("--project", type=Path, help="project root for size/stack signals")
    parser.add_argument(
        "--craft-depth",
        choices=("standard", "polished", "studio"),
        help="design craft depth override",
    )
    parser.add_argument(
        "--spend",
        choices=("lean", "normal", "thorough"),
        help="soft main-agent thoroughness override",
    )
    parser.add_argument(
        "--parallelism",
        choices=("low", "medium", "high", "max"),
        help="soft parallelism preference override",
    )
    parser.add_argument(
        "--topology",
        choices=TOPOLOGIES,
        help="topology override (never lowers risk floor)",
    )
    args = parser.parse_args()
    prompt = args.file.read_text(encoding="utf-8") if args.file else " ".join(args.prompt)
    if not prompt.strip():
        parser.error("provide a prompt or --file")
    try:
        result = route_task(
            prompt,
            args.explicit_risk,
            registry_path=args.registry,
            home=args.home,
            project_root=args.project,
            craft_depth_override=args.craft_depth,
            spend_override=args.spend,
            parallelism_override=args.parallelism,
            topology_override=args.topology,
        )
    except RegistryError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
