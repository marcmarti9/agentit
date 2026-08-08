"""Conservative, provider-neutral task router.

The router only classifies and plans. It never executes a command, rewrites
stdout, loads a skill body, or lowers an inferred risk level.
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


def _delegation_requested(text: str) -> bool:
    return _matches(
        text,
        (
            r"parallel|paralel|independent|independiente|fan[- ]out|dag|subagent|subagente",
            r"multidomain|multidominio|separate packages|paquetes separados",
        ),
    )


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
        ("frontend", r"frontend|ui|css|react|component|web|browser"),
        ("documentation", r"document|readme|docs|texto|copy|writing|escritura"),
        ("explanation", r"explain|explica|qué es|what is|how to|cómo|question|pregunta"),
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
    if _matches(text, (r"\busa agentit\b|\buse agentit\b|\bagentit mode\b|\bmodo agentit\b",)):
        selected.append("using-agentit")
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


def _topology(text: str, risk: str) -> str:
    """Choose a minimal execution shape; risk alone never creates agents."""
    # Avoid bare "trace" — matches product names like `agentit trace`.
    if _matches(
        text,
        (
            r"\b(probe|investiga|reproduce|localiza|root cause|causa raíz)\b",
            r"\b(trace the|trace this|trazar|rastrear|diagnos[ea])\b",
        ),
    ):
        return "probe"
    if _delegation_requested(text):
        return "fan_out"
    if _matches(text, (r"pipeline|sequential stages|etapas secuenciales|dag de etapas",)):
        return "pipeline"
    if risk in {"RISK_3", "RISK_4"}:
        if risk == "RISK_4":
            return "audit"
        if _implementation_requested(text):
            return "writer_reviewer"
        return "audit"
    return "direct"


def _subagent_budget(text: str, risk: str, topology: str) -> dict[str, Any]:
    """Return a budget, not a command to spawn agents."""
    if topology in {"writer_reviewer", "audit"}:
        return {"recommended": 1, "max": 1, "requires_justification": True}
    if not _delegation_requested(text) or risk in {"RISK_0", "RISK_1"}:
        maximum = 0
    elif risk == "RISK_2":
        maximum = 3
    else:
        maximum = 5
    return {"recommended": 0, "max": maximum, "requires_justification": maximum > 0}


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
        signals.append("independent work explicitly requested")
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


def route_task(
    prompt: str,
    explicit_risk: str | None = None,
    *,
    registry_path: Path | None = None,
    home: Path | None = None,
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
    (
        skills_available,
        skills_recommended_missing,
        skills_suppressed_conflicts,
        skill_recommendation_metadata,
    ) = _resolve_skill_recommendations(
        _recommended_skill_ids(text.lower(), category, risk),
        registry_entries,
        registry_path=resolved_registry_path,
        home=resolved_home,
        text=text.lower(),
    )
    topology = _topology(text.lower(), risk)
    signals = _signals(
        text.lower(),
        risk=risk,
        topology=topology,
        content_types=content_types,
        routing_advice=routing_advice,
    )
    prefs = load_preferences(resolved_home / ".agentit" / "preferences.yaml")
    auto_jit_enabled = bool(prefs.get("auto_jit_profiles", True))
    auto_plan_enabled = bool(prefs.get("auto_plan_mode", True))

    jit_profiles: list[str] = []
    unmapped_skills: list[str] = []
    if auto_jit_enabled and skills_recommended_missing:
        mapped_set = set()
        for skill in skills_recommended_missing:
            if skill in SKILL_PROFILE_MAP:
                mapped_set.add(SKILL_PROFILE_MAP[skill])
            else:
                unmapped_skills.append(skill)
        jit_profiles = sorted(mapped_set)

    auto_plan_recommended = (
        (risk in {"RISK_2", "RISK_3", "RISK_4"} or topology != "direct")
        if auto_plan_enabled
        else (risk in {"RISK_3", "RISK_4"})
    )

    applied_prefs = {
        "preferred_language": prefs.get("user_style_preferences", {}).get("preferred_language", "es"),
        "testing_framework": prefs.get("user_style_preferences", {}).get("testing_framework", "pytest"),
        "ui_styling": prefs.get("user_style_preferences", {}).get("ui_styling", "vanilla_css_oklch"),
        "response_style": response_style,
    }

    return {
        "risk": risk,
        "category": category,
        "complexity": complexity,
        "content_types": content_types,
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
        "subagents": _subagent_budget(text.lower(), risk, topology),
        "verification": verification,
        "auto_plan_mode_recommended": auto_plan_recommended,
        "jit_profile_recommendations": jit_profiles,
        "unmapped_skills": unmapped_skills,
        "applied_preferences": applied_prefs,
        "reversible": True if risk in {"RISK_0", "RISK_1", "RISK_2"} else None,
        "recovery": (
            "not proven; retrieve originals before RISK_3/RISK_4 actions"
            if risk in {"RISK_3", "RISK_4"}
            else "not needed"
        ),
        "reasons": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify an agent task conservatively.")
    parser.add_argument("prompt", nargs="*", help="task text")
    parser.add_argument("--risk", choices=sorted(RISK_ORDER), dest="explicit_risk")
    parser.add_argument("--file", type=Path, help="read the task text from a UTF-8 file")
    parser.add_argument("--registry", type=Path, help="portable registry path")
    parser.add_argument("--home", type=Path, help="HOME used for bounded path discovery")
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
        )
    except RegistryError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
