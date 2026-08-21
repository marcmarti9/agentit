"""LLM-native Agentit decision contract.

Natural-language understanding belongs to the host model. This module contains
only the stable decision schema and deterministic invariants that can be checked
without pretending Python understands the user's intent.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

try:
    from router.capabilities import (
        CapabilityCatalogError,
        load_capability_catalog,
        resolve_capabilities,
        specialist_capability_requirements,
    )
    from router.preferences import load_preferences
    from router.project_signals import collect_project_signals
    from router.registry import (
        DEFAULT_REGISTRY_PATH,
        RegistryError,
        load_registry,
        resolve_requested_skills,
    )
except ImportError:  # pragma: no cover - direct script execution
    from capabilities import (  # type: ignore
        CapabilityCatalogError,
        load_capability_catalog,
        resolve_capabilities,
        specialist_capability_requirements,
    )
    from preferences import load_preferences  # type: ignore
    from project_signals import collect_project_signals  # type: ignore
    from registry import (  # type: ignore
        DEFAULT_REGISTRY_PATH,
        RegistryError,
        load_registry,
        resolve_requested_skills,
    )


RISK_ORDER = {f"RISK_{level}": level for level in range(5)}
INTENTS = {
    "explain",
    "investigate",
    "review",
    "implement",
    "design",
    "document",
    "operate",
}
CATEGORIES = {
    "explanation",
    "research",
    "bug",
    "testing",
    "engineering",
    "frontend",
    "design",
    "backend",
    "database",
    "security",
    "marketing",
    "documentation",
    "release",
}
COMPLEXITIES = {"trivial", "bounded", "substantial", "structural"}
TOPOLOGIES = {"direct", "probe", "fan_out", "pipeline", "writer_reviewer", "audit"}
DOMAIN_PACKS = {
    "engineering",
    "frontend",
    "design",
    "backend",
    "data",
    "product",
    "writing",
    "release",
    "research",
}
CRAFT_DEPTHS = {"Standard", "Polished", "Studio"}
VERIFICATION_FIELDS = {
    "tests_required",
    "browser_required",
    "independent_review",
    "dry_run_required",
    "backup_required",
    "rollback_plan_required",
    "post_check_required",
}


class DecisionContractError(RuntimeError):
    """Raised when a model decision violates the Agentit decision contract."""


def decision_protocol() -> dict[str, Any]:
    """Return the stable rubric the host model must apply before execution."""
    return {
        "rule": "The host LLM must classify every task before execution. Python never infers intent from prompt keywords.",
        "context_rule": (
            "Use the full conversation, repository state, current files, available tools, user/project instructions, "
            "and the requested action. Do not classify from the last prompt string in isolation when context exists."
        ),
        "required_output_fields": [
            "schema_version",
            "intent",
            "category",
            "complexity",
            "risk",
            "reversible",
            "topology",
            "domain_pack",
            "public_visual",
            "greenfield_or_total_redesign",
            "craft_depth",
            "craft_depth_overridden",
            "destructive_data_operation",
            "skills",
            "specialists",
            "capabilities",
            "delegation",
            "verification",
            "critic_required",
            "evidence_signals",
            "reasons",
        ],
        "risk_rubric": {
            "RISK_0": "Read-only explanation or analysis with no meaningful external or repository mutation.",
            "RISK_1": "Local, trivial, easily reversible change with low blast radius.",
            "RISK_2": "Meaningful but bounded change with ordinary engineering/product consequences.",
            "RISK_3": "Sensitive boundary: auth, security, payments, PII, significant migration/infrastructure, or comparable impact.",
            "RISK_4": "Destructive, production, data-loss, irreversible, or otherwise high-blast-radius operation.",
        },
        "topology_rubric": {
            "direct": "One coherent execution owner; delegation adds no clear benefit.",
            "probe": "Read-only investigation should precede implementation or judgment.",
            "fan_out": "Two or more genuinely independent branches benefit from parallel isolated work.",
            "pipeline": "Distinct dependent stages with explicit handoffs.",
            "writer_reviewer": "One implementation owner plus independent review is justified by error cost.",
            "audit": "Primary job is independent inspection/critique rather than implementation.",
        },
        "selection_rules": [
            "Apply the same rubric every time; the answer may differ when context differs.",
            "Select the smallest useful skill set, but do not omit a skill that materially changes correctness or quality.",
            "Multi-agent is chosen only for a concrete benefit: independence, specialization, context isolation, breadth, or fresh review.",
            "A listed skill is not loaded until its SKILL.md body is actually available to the executing model.",
            "Public visual surfaces are design-primary and require rendered/browser verification.",
            "Large structural or high-impact plans require an independent critic.",
            "Explicit user/project risk constraints can raise the floor; the model may never lower them.",
        ],
        "hard_policy": [
            "RISK_3 and RISK_4 require independent review.",
            "RISK_4 requires dry-run/preview where technically meaningful, a rollback plan, and a post-check.",
            "Destructive data operations require RISK_4 and a verified backup.",
            "Fan-out requires at least two independent branches and a concrete delegation reason.",
            "Structural work requires critic_required=true.",
        ],
    }


def _safe_preferences(home: Path | None) -> dict[str, Any]:
    path = Path(home) / ".agentit" / "preferences.yaml" if home is not None else None
    prefs = load_preferences(path)
    style = prefs.get("user_style_preferences")
    style = style if isinstance(style, dict) else {}
    return {
        "preferred_language": style.get("preferred_language"),
        "testing_framework": style.get("testing_framework"),
        "ui_styling": style.get("ui_styling"),
        "response_style": style.get("response_style"),
        "auto_jit_profiles": bool(prefs.get("auto_jit_profiles", True)),
        "auto_plan_mode": bool(prefs.get("auto_plan_mode", True)),
        "parallelism_preference": prefs.get("parallelism_preference", "medium"),
    }


def build_decision_request(
    task: str,
    *,
    explicit_risk: str | None = None,
    registry_path: Path | None = None,
    home: Path | None = None,
    project_root: Path | None = None,
    provider_host: str = "local",
    available_providers: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Build context for the host LLM without semantically classifying the task."""
    if not isinstance(task, str) or not task.strip():
        raise DecisionContractError("task must be a non-empty string")
    if explicit_risk is not None and explicit_risk not in RISK_ORDER:
        raise DecisionContractError(f"unknown explicit risk: {explicit_risk}")

    path = Path(registry_path) if registry_path is not None else DEFAULT_REGISTRY_PATH
    entries = load_registry(path)
    project_signals = collect_project_signals(project_root)
    return {
        "schema_version": 1,
        "status": "decision_required",
        "classification_owner": "host_llm",
        "task": task,
        "explicit_risk_floor": explicit_risk,
        "protocol": decision_protocol(),
        "applied_preferences": _safe_preferences(home),
        "project_signals": project_signals,
        "token_estimate": {
            "status": "pending_host_decision",
            "not_a_bill": True,
            "basis": project_signals.get("basis", ["classification_pending"]),
        },
        "registry": {
            "path": str(path),
            "entry_count": len(entries),
            "selection_owner": "host_llm",
        },
        "provider_context": {
            "host": provider_host,
            "available_providers": list(available_providers) if available_providers is not None else None,
        },
    }


def _require_mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DecisionContractError(f"{field} must be a mapping")
    return value


def _require_string_list(value: Any, field: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise DecisionContractError(f"{field} must be a list of non-empty strings")
    result = list(dict.fromkeys(item.strip() for item in value))
    if nonempty and not result:
        raise DecisionContractError(f"{field} must not be empty")
    return result


def _require_bool(mapping: dict[str, Any], field: str) -> bool:
    value = mapping.get(field)
    if not isinstance(value, bool):
        raise DecisionContractError(f"{field} must be boolean")
    return value


def _validate_shape(decision: dict[str, Any]) -> dict[str, Any]:
    if decision.get("schema_version") != 1:
        raise DecisionContractError("decision must use schema_version: 1")

    intent = decision.get("intent")
    category = decision.get("category")
    complexity = decision.get("complexity")
    risk = decision.get("risk")
    topology = decision.get("topology")
    domain_pack = decision.get("domain_pack")
    if intent not in INTENTS:
        raise DecisionContractError(f"unknown intent: {intent!r}")
    if category not in CATEGORIES:
        raise DecisionContractError(f"unknown category: {category!r}")
    if complexity not in COMPLEXITIES:
        raise DecisionContractError(f"unknown complexity: {complexity!r}")
    if risk not in RISK_ORDER:
        raise DecisionContractError(f"unknown risk: {risk!r}")
    if topology not in TOPOLOGIES:
        raise DecisionContractError(f"unknown topology: {topology!r}")
    if domain_pack not in DOMAIN_PACKS:
        raise DecisionContractError(f"unknown domain_pack: {domain_pack!r}")

    reversible = decision.get("reversible")
    if reversible is not None and not isinstance(reversible, bool):
        raise DecisionContractError("reversible must be true, false, or null")

    for field in (
        "public_visual",
        "greenfield_or_total_redesign",
        "craft_depth_overridden",
        "destructive_data_operation",
        "critic_required",
    ):
        _require_bool(decision, field)

    craft_depth = decision.get("craft_depth")
    if craft_depth is not None and craft_depth not in CRAFT_DEPTHS:
        raise DecisionContractError(f"unknown craft_depth: {craft_depth!r}")

    decision["skills"] = _require_string_list(decision.get("skills"), "skills")
    decision["specialists"] = _require_string_list(decision.get("specialists"), "specialists")
    decision["evidence_signals"] = _require_string_list(
        decision.get("evidence_signals"), "evidence_signals"
    )
    decision["reasons"] = _require_string_list(decision.get("reasons"), "reasons", nonempty=True)

    capabilities = _require_mapping(decision.get("capabilities"), "capabilities")
    capabilities["required"] = _require_string_list(capabilities.get("required"), "capabilities.required")
    capabilities["preferred"] = _require_string_list(capabilities.get("preferred"), "capabilities.preferred")
    decision["capabilities"] = capabilities

    delegation = _require_mapping(decision.get("delegation"), "delegation")
    parallelism = delegation.get("parallelism")
    reason = delegation.get("reason")
    if not isinstance(parallelism, int) or isinstance(parallelism, bool) or parallelism < 1:
        raise DecisionContractError("delegation.parallelism must be an integer >= 1")
    if not isinstance(reason, str):
        raise DecisionContractError("delegation.reason must be a string")
    delegation["reason"] = reason.strip()
    decision["delegation"] = delegation

    verification = _require_mapping(decision.get("verification"), "verification")
    missing_verification = VERIFICATION_FIELDS - set(verification)
    if missing_verification:
        raise DecisionContractError(
            "verification is missing fields: " + ", ".join(sorted(missing_verification))
        )
    for field in VERIFICATION_FIELDS:
        if not isinstance(verification.get(field), bool):
            raise DecisionContractError(f"verification.{field} must be boolean")
    decision["verification"] = verification
    return decision


def _policy_violations(decision: dict[str, Any], explicit_risk: str | None) -> list[str]:
    violations: list[str] = []
    risk = decision["risk"]
    verification = decision["verification"]

    if explicit_risk is not None:
        if explicit_risk not in RISK_ORDER:
            raise DecisionContractError(f"unknown explicit risk: {explicit_risk}")
        if RISK_ORDER[risk] < RISK_ORDER[explicit_risk]:
            violations.append(f"risk {risk} is below explicit floor {explicit_risk}")

    if RISK_ORDER[risk] >= RISK_ORDER["RISK_3"] and not verification["independent_review"]:
        violations.append("RISK_3/RISK_4 requires verification.independent_review=true")
    if risk == "RISK_4":
        for field in ("dry_run_required", "rollback_plan_required", "post_check_required"):
            if not verification[field]:
                violations.append(f"RISK_4 requires verification.{field}=true")

    if decision["destructive_data_operation"]:
        if risk != "RISK_4":
            violations.append("destructive_data_operation requires RISK_4")
        if not verification["backup_required"]:
            violations.append("destructive_data_operation requires verification.backup_required=true")
        if decision["reversible"] is True:
            violations.append("destructive_data_operation cannot claim reversible=true")

    if decision["public_visual"]:
        if decision["domain_pack"] != "design":
            violations.append("public_visual work must use domain_pack=design")
        if decision["craft_depth"] is None:
            violations.append("public_visual work requires a craft_depth")
        if not verification["browser_required"]:
            violations.append("public_visual work requires browser verification")
    elif decision["craft_depth"] is not None:
        violations.append("craft_depth only applies when public_visual=true")

    if decision["greenfield_or_total_redesign"]:
        if not decision["public_visual"]:
            violations.append("greenfield_or_total_redesign implies public_visual=true")
        if decision["craft_depth"] != "Studio" and not decision["craft_depth_overridden"]:
            violations.append("greenfield/total public redesign defaults to Studio unless explicitly overridden")

    if decision["complexity"] == "structural" and not decision["critic_required"]:
        violations.append("structural work requires critic_required=true")

    parallelism = decision["delegation"]["parallelism"]
    reason = decision["delegation"]["reason"]
    if decision["topology"] == "fan_out":
        if parallelism < 2:
            violations.append("fan_out requires delegation.parallelism >= 2")
        if not reason:
            violations.append("fan_out requires a concrete delegation.reason")
    if decision["topology"] == "direct" and parallelism != 1:
        violations.append("direct topology requires delegation.parallelism=1")
    if decision["topology"] == "writer_reviewer" and not verification["independent_review"]:
        violations.append("writer_reviewer requires independent review")

    return violations


def validate_decision(
    decision: dict[str, Any],
    *,
    explicit_risk: str | None = None,
    registry_path: Path | None = None,
    home: Path | None = None,
    provider_host: str = "local",
    available_providers: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Validate a host-model decision and attach deterministic inventory evidence."""
    if not isinstance(decision, dict):
        raise DecisionContractError("decision must be a mapping")
    normalized = _validate_shape(dict(decision))
    violations = _policy_violations(normalized, explicit_risk)
    if violations:
        raise DecisionContractError("; ".join(violations))

    path = Path(registry_path) if registry_path is not None else DEFAULT_REGISTRY_PATH
    skill_inventory = resolve_requested_skills(
        normalized["skills"],
        registry_path=path,
        home=home,
        signals=normalized["evidence_signals"],
    )

    try:
        capability_catalog = load_capability_catalog()
        specialist_requirements = specialist_capability_requirements(
            normalized["specialists"],
            capability_catalog=capability_catalog,
        )
        required = list(
            dict.fromkeys(
                [*specialist_requirements["required"], *normalized["capabilities"]["required"]]
            )
        )
        preferred = [
            item
            for item in dict.fromkeys(
                [*specialist_requirements["preferred"], *normalized["capabilities"]["preferred"]]
            )
            if item not in required
        ]
        capability_envelope = resolve_capabilities(
            required=required,
            preferred=preferred,
            available_providers=(list(available_providers) if available_providers is not None else None),
            host=provider_host,
            catalog=capability_catalog,
        )
    except CapabilityCatalogError as exc:
        raise DecisionContractError(str(exc)) from exc

    execution_ready = not skill_inventory["missing"]
    if capability_envelope.get("status") == "degraded":
        execution_ready = False
    if capability_envelope.get("status") == "inventory_required" and required:
        execution_ready = False

    return {
        "schema_version": 1,
        "status": "valid",
        "classification_owner": "host_llm",
        "decision": normalized,
        "policy_violations": [],
        "skill_inventory": skill_inventory,
        "capability_envelope": capability_envelope,
        "execution_ready": execution_ready,
    }


def validate_decision_file(path: Path, **kwargs: Any) -> dict[str, Any]:
    import json

    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DecisionContractError(f"cannot read decision JSON {path}: {exc}") from exc
    return validate_decision(payload, **kwargs)
