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


RISK_ORDER = {f"RISK_{level}": level for level in range(5)}
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


def _infer_risk(text: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    action_boundary = r"(?:^|[.;]|\bthen\b|\binstead\b|\by luego\b|\bdespués\b)\s*(?:please\s+|por favor\s+)?"
    explanatory = _matches(
        text,
        (
            r"^\s*(explain|explícame|explica|qué es|what is)\b",
            r"^\s*(describe|review|revisa)\b.{0,80}\b(without changing|sin cambiar|conceptual|policy|política)\b",
        ),
    )
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

    if explanatory:
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
    if high_impact:
        return "RISK_3", reasons + ["detecté impacto en seguridad, persistencia o infraestructura"]
    if _matches(text, (r"explain|explíca|explica|qué es|what is|question|pregunta|brainstorm",)):
        return "RISK_0", ["parece una explicación o conversación sin cambio real"]
    if _matches(text, (r"css|rename|renombr|format|formato|document|documentación|copy|texto|typo",)):
        return "RISK_1", ["parece un cambio localizado y reversible"]
    if _matches(text, (r"feature|funcionalidad|implement|arregla|fix|bug|refactor|test|prueba|integrat",)):
        return "RISK_2", ["parece desarrollo estándar con posible regresión"]
    return "RISK_2", ["tarea no reconocida; se conserva un nivel conservador por defecto"]


def _category(text: str, risk: str) -> str:
    if risk == "RISK_0" and _matches(
        text, (r"\b(explain|explícame|explica|qué es|what is|question|pregunta)\b",)
    ):
        return "explanation"
    patterns = (
        ("marketing", r"marketing|cro|seo|copy|landing|conversion|analytics|analítica|growth"),
        ("design", r"design|diseño|visual|screenshot|captura|ui estética|redesign"),
        ("database", r"database|base de datos|sql|schema|esquema|migration|migración|backup|restore"),
        ("security", r"auth|login|security|seguridad|secret|credential|permission|autorización"),
        ("bug", r"bug|fix|error|falla|fallo|debug|depura"),
        ("testing", r"test|prueba|coverage|cobertura|eval|benchmark"),
        ("frontend", r"frontend|ui|css|react|component|web|browser"),
        ("documentation", r"document|readme|docs|texto|copy|writing|escritura"),
        ("explanation", r"explain|explica|qué es|what is|question|pregunta"),
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
        selected.append("marketingskills")
        return list(dict.fromkeys(selected))
    if category == "design":
        selected.extend(["frontend-ui-engineering", "hallmark"])
        return list(dict.fromkeys(selected))
    if category == "documentation" and _matches(text, (r"public|público|copy|writing|texto",)):
        selected.append("no-ai-slop")
        return list(dict.fromkeys(selected))

    if category == "bug":
        selected.append("debugging-and-error-recovery")
    if category == "testing":
        selected.append("test-driven-development")
    if category == "database":
        selected.append("supabase-postgres-best-practices")
    if category == "frontend":
        selected.append("frontend-ui-engineering")
    if _matches(text, (r"context|contexto|token|compresión|compression|memory|memoria",)):
        selected.append("context-engineering")
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
        if is_available and set(entry["conflicts_with"]).intersection(available):
            suppressed_conflicts.append(skill_id)
            continue
        target = available if is_available else missing
        target.append(skill_id)
    return available, missing, suppressed_conflicts, metadata


def _topology(text: str, risk: str) -> str:
    """Choose a minimal execution shape; risk alone never creates agents."""
    if _matches(
        text,
        (r"probe|investiga|reproduce|localiza|trace|root cause|causa raíz",),
    ):
        return "probe"
    if _matches(
        text,
        (
            r"parallel|paralel|independent|independiente|fan[- ]out|dag|subagent|subagente",
            r"multidomain|multidominio|separate packages|paquetes separados",
        ),
    ):
        return "fan_out"
    if risk in {"RISK_3", "RISK_4"}:
        return "audit"
    return "direct"


def _subagent_budget(text: str, risk: str) -> dict[str, Any]:
    """Return a budget, not a command to spawn agents."""
    explicit_delegation = _matches(
        text,
        (
            r"parallel|paralel|independent|independiente|fan[- ]out|dag|subagent|subagente",
            r"multidomain|multidominio|separate packages|paquetes separados",
        ),
    )
    if not explicit_delegation or risk in {"RISK_0", "RISK_1"}:
        maximum = 0
    elif risk == "RISK_2":
        maximum = 3
    else:
        maximum = 5
    return {"recommended": 0, "max": maximum, "requires_justification": maximum > 0}


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
    critical = risk in {"RISK_3", "RISK_4"} or bool(CRITICAL_CONTENT.intersection(content_types))

    if risk in {"RISK_0", "RISK_1"}:
        output_profile = "TERSE_SAFE"
    elif risk == "RISK_2":
        output_profile = "STANDARD"
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
            "allowed": ["exact_dedup", "reversible_ccr"],
            "semantic": False,
            "deny_reasons": [],
        }
    else:
        compression = {
            "enabled": True,
            "mode": "SAFE_STRUCTURAL",
            "allowed": ["exact_dedup", "output_terse"],
            "semantic": False,
            "deny_reasons": [],
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
        "output_profile": output_profile,
        "compression": compression,
        "topology": _topology(text.lower(), risk),
        "subagents": _subagent_budget(text.lower(), risk),
        "verification": verification,
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
