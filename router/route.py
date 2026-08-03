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


RISK_ORDER = {f"RISK_{level}": level for level in range(5)}
CRITICAL_CONTENT = {
    "commands",
    "diff",
    "errors",
    "pipelines",
    "secrets",
    "sql",
}


def _matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def _infer_risk(text: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    destructive = _matches(
        text,
        (
            r"\b(drop|truncate|destroy|delete|wipe|purge)\b",
            r"\b(elimina|borrar|destruye|destruir|irreversible|restaura|restaurar)\b",
            r"data\s*loss|pérdida\s+de\s+datos",
        ),
    )
    production = _matches(text, (r"\bprod(?:uction)?\b", r"producción", r"live"))
    if destructive and production:
        return "RISK_4", ["detecté una operación destructiva dirigida a producción"]
    if _matches(text, (r"\b(drop|truncate)\s+database\b", r"base de datos de producción")):
        return "RISK_4", ["detecté una operación potencialmente irreversible sobre datos"]
    if destructive:
        reasons.append("detecté una operación destructiva; se eleva como mínimo a RISK_3")

    high_impact = _matches(
        text,
        (
            r"auth|login|logout|sesión|session|authorization|autorización|permission|permiso",
            r"payment|pago|billing|factur",
            r"pii|personal data|datos personales|secret|secreto|credential|credencial",
            r"migration|migración|deploy|desplieg|infrastructure|infraestructura",
            r"public api|api pública|api contract|contrato de api",
            r"concurren|race condition|rollback|backup|restore|base de datos|database",
        ),
    )
    if high_impact or destructive:
        return "RISK_3", reasons + ["detecté impacto en seguridad, persistencia o infraestructura"]
    if _matches(text, (r"explain|explíca|explica|qué es|what is|question|pregunta|brainstorm",)):
        return "RISK_0", ["parece una explicación o conversación sin cambio real"]
    if _matches(text, (r"css|rename|renombr|format|formato|document|documentación|copy|texto|typo",)):
        return "RISK_1", ["parece un cambio localizado y reversible"]
    if _matches(text, (r"feature|funcionalidad|implement|arregla|fix|bug|refactor|test|prueba|integrat",)):
        return "RISK_2", ["parece desarrollo estándar con posible regresión"]
    return "RISK_2", ["tarea no reconocida; se conserva un nivel conservador por defecto"]


def _category(text: str, risk: str) -> str:
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


def _skills(text: str, category: str, risk: str) -> list[str]:
    if category == "marketing":
        return ["marketing-skills"]
    if category == "design":
        return ["hallmark"]
    if category == "documentation" and _matches(text, (r"public|público|copy|writing|texto",)):
        return ["no-ai-slop"]

    selected: list[str] = []
    if risk in {"RISK_3", "RISK_4"}:
        selected.extend(["security-hardening", "architect-orchestrator"])
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
    if risk == "RISK_2" and not selected:
        selected.append("superpowers")
    return list(dict.fromkeys(selected))


def route_task(prompt: str, explicit_risk: str | None = None) -> dict[str, Any]:
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
    return {
        "risk": risk,
        "category": category,
        "complexity": complexity,
        "content_types": content_types,
        "skills": _skills(text, category, risk),
        "output_profile": output_profile,
        "compression": compression,
        "subagents": {"max": [0, 0, 2, 4, 5][RISK_ORDER[risk]]},
        "verification": verification,
        "reversible": True,
        "recovery": "retrieve originals before RISK_3/RISK_4 actions" if risk in {"RISK_3", "RISK_4"} else "not needed",
        "reasons": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify an agent task conservatively.")
    parser.add_argument("prompt", nargs="*", help="task text")
    parser.add_argument("--risk", choices=sorted(RISK_ORDER), dest="explicit_risk")
    parser.add_argument("--file", type=Path, help="read the task text from a UTF-8 file")
    args = parser.parse_args()
    prompt = args.file.read_text(encoding="utf-8") if args.file else " ".join(args.prompt)
    if not prompt.strip():
        parser.error("provide a prompt or --file")
    print(json.dumps(route_task(prompt, args.explicit_risk), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
