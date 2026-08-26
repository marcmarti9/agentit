"""Bounded Worker Context Contract for delegated Agentit work.

The active AI decides semantics (skills, packs, references, topology, risk). This
module projects that explicit decision into a least-privilege worker payload and
validates mechanical invariants before spawn. It never classifies natural-language
intent or expands a task into a global catalog.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    from router.capabilities import (
        CapabilityCatalogError,
        load_capability_catalog,
        resolve_capabilities,
        specialist_capability_requirements,
        validate_capability_envelope,
    )
except ImportError:
    from capabilities import (  # type: ignore
        CapabilityCatalogError,
        load_capability_catalog,
        resolve_capabilities,
        specialist_capability_requirements,
        validate_capability_envelope,
    )


INSTRUCTION_BASENAMES: tuple[str, ...] = (
    "AGENTS.md",
    "CLAUDE.md",
    "CODEX.md",
    "GEMINI.md",
)

PRECEDENCE: tuple[str, ...] = (
    "safety",
    "explicit_user_instruction",
    "project_instruction",
    "preferences",
    "defaults",
)

DEFAULT_CONSTRAINTS: tuple[str, ...] = (
    "no commits",
    "no pushes",
    "no external changes",
    "no dependency changes",
)

ROLES: frozenset[str] = frozenset({"implementer", "reviewer", "probe"})
VALID_RISKS: frozenset[str] = frozenset({"RISK_1", "RISK_2", "RISK_3", "RISK_4"})

PROJECTABLE_PREFERENCE_KEYS: tuple[str, ...] = (
    "preferred_language",
    "code_style",
    "testing_framework",
    "ui_styling",
    "response_style",
)

_SECRET_KEY_RE = re.compile(
    r"(secret|password|passwd|token|api[_-]?key|private[_-]?key|credential|auth)",
    re.IGNORECASE,
)
_SECRET_VALUE_RE = re.compile(
    r"(?i)(sk-[a-z0-9]{16,}|ghp_[a-z0-9]{20,}|xox[baprs]-[a-z0-9-]{10,}"
    r"|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
)


class WorkerContextError(ValueError):
    """Raised when a worker context cannot be built or validated safely."""


@dataclass(frozen=True)
class InstructionFile:
    path: str
    basename: str
    scope: str
    content: str
    sha256_prefix: str


@dataclass
class WorkerTaskSpec:
    """Explicit AI-owned task metadata to project into a delegated worker."""

    objective: str
    scope: str = ""
    role: str = "implementer"
    risk: str = "RISK_2"
    skills: Sequence[str] = field(default_factory=tuple)
    relevant_packs: Sequence[str] = field(default_factory=tuple)
    references: Sequence[str] = field(default_factory=tuple)
    allowed_files: Sequence[str] = field(default_factory=tuple)
    write_paths: Sequence[str] = field(default_factory=tuple)
    artifact_uris: Sequence[str] = field(default_factory=tuple)
    expected_output: str = ""
    verification: str = ""
    stop_condition: str = ""
    explicit_user_instructions: Sequence[str] = field(default_factory=tuple)
    safety_constraints: Sequence[str] = field(default_factory=tuple)
    extra_constraints: Sequence[str] = field(default_factory=tuple)
    authorize_commits: bool = False
    authorize_push: bool = False
    authorize_external: bool = False
    work_subdir: str | None = None
    include_manifest_skills: bool = False
    parent_topology: str = ""
    independent_review_required: bool = False
    specialist_ids: Sequence[str] = field(default_factory=tuple)
    required_capabilities: Sequence[str] = field(default_factory=tuple)
    preferred_capabilities: Sequence[str] = field(default_factory=tuple)
    available_providers: Sequence[str] | None = None
    provider_host: str = "local"


def _sha256_prefix(text: str, n: int = 12) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def _is_safe_regular_file(path: Path) -> bool:
    try:
        return path.is_file() and not path.is_symlink()
    except OSError:
        return False


def discover_project_instructions(
    project_root: Path,
    *,
    work_subdir: str | None = None,
) -> list[InstructionFile]:
    """Discover root and optional subdirectory instruction files safely."""
    root = Path(project_root)
    if not root.is_dir() or root.is_symlink():
        raise WorkerContextError(f"project root must be a regular directory: {root}")
    root_resolved = root.resolve()
    found: list[InstructionFile] = []

    def collect(directory: Path, scope: str) -> None:
        if not directory.is_dir() or directory.is_symlink():
            return
        try:
            directory.resolve().relative_to(root_resolved)
        except ValueError as exc:
            raise WorkerContextError(
                f"instruction directory escapes project root: {directory}"
            ) from exc
        for basename in INSTRUCTION_BASENAMES:
            path = directory / basename
            if not _is_safe_regular_file(path):
                continue
            content = path.read_text(encoding="utf-8")
            found.append(
                InstructionFile(
                    path=str(path.relative_to(root)),
                    basename=basename,
                    scope=scope,
                    content=content,
                    sha256_prefix=_sha256_prefix(content),
                )
            )

    collect(root, "root")
    if work_subdir:
        sub = (root / work_subdir).resolve()
        try:
            sub.relative_to(root_resolved)
        except ValueError as exc:
            raise WorkerContextError(f"work_subdir escapes project root: {work_subdir}") from exc
        if sub != root_resolved:
            collect(sub, "subdir")
    return found


def load_manifest_skill_ids(project_root: Path) -> list[str]:
    manifest_path = Path(project_root) / ".agentit" / "skills-manifest.json"
    if not _is_safe_regular_file(manifest_path):
        return []
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkerContextError(f"invalid skills manifest: {exc}") from exc
    skills = payload.get("skills")
    if isinstance(skills, dict):
        return sorted(str(key) for key in skills)
    if isinstance(skills, list):
        return [str(item) for item in skills if isinstance(item, str) and item.strip()]
    return []


def project_preferences(preferences: Mapping[str, Any] | None) -> dict[str, Any]:
    """Project only safe style/tooling preferences, never secret-shaped data."""
    if not preferences:
        return {}
    style = preferences.get("user_style_preferences")
    if not isinstance(style, dict):
        style = {key: preferences[key] for key in PROJECTABLE_PREFERENCE_KEYS if key in preferences}
    projected: dict[str, Any] = {}
    for key in PROJECTABLE_PREFERENCE_KEYS:
        if key not in style or _SECRET_KEY_RE.search(key):
            continue
        value = style[key]
        if isinstance(value, str) and _SECRET_VALUE_RE.search(value):
            continue
        if isinstance(value, str) and len(value) > 40 and _SECRET_KEY_RE.search(value):
            continue
        projected[key] = value
    return projected


def resolve_skills_projected(
    *,
    task_skills: Sequence[str],
    manifest_skills: Sequence[str],
    include_manifest_skills: bool,
    known_repository_skills: Iterable[str] | None = None,
) -> list[str]:
    """Project only explicitly selected task skills; never auto-load all skills."""
    known = set(known_repository_skills) if known_repository_skills is not None else None
    ordered: list[str] = []

    def add_many(values: Sequence[str]) -> None:
        for value in values:
            skill_id = str(value).strip()
            if not skill_id:
                continue
            if known is not None and skill_id not in known:
                raise WorkerContextError(f"unknown skill id for projection: {skill_id}")
            if skill_id not in ordered:
                ordered.append(skill_id)

    if task_skills:
        add_many(task_skills)
    elif include_manifest_skills and manifest_skills:
        add_many(manifest_skills)
    return ordered


def _dedup_text(values: Sequence[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        text = str(value).strip()
        if text and text not in result:
            result.append(text)
    return result


def build_constraints(spec: WorkerTaskSpec) -> list[str]:
    constraints: list[str] = []

    def add(value: str) -> None:
        value = value.strip()
        if value and value not in constraints:
            constraints.append(value)

    for item in spec.safety_constraints:
        add(item)
    if not spec.authorize_commits:
        add("no commits")
    if not spec.authorize_push:
        add("no pushes")
    if not spec.authorize_external:
        add("no external changes")
    add("no dependency changes")
    for item in spec.extra_constraints:
        add(item)
    if spec.role == "reviewer":
        add("read-only: do not modify source files")
        add("do not implement features; review only")
    if spec.role == "probe":
        add("read-only investigation")
        add("do not modify source files")
    if spec.independent_review_required and spec.role in {"reviewer", "probe"}:
        add("independent review: challenge assumptions; do not rubber-stamp the parent plan")
    return constraints


def detect_instruction_conflicts(instructions: Sequence[InstructionFile]) -> list[dict[str, str]]:
    """Return advisory root/subdir conflict signals; semantics remain AI-owned."""
    by_base: dict[str, list[InstructionFile]] = {}
    for instruction in instructions:
        by_base.setdefault(instruction.basename, []).append(instruction)
    conflicts: list[dict[str, str]] = []
    negation_pairs = (
        (r"\bnever use react\b", r"\balways use react\b"),
        (r"\bno react\b", r"\bmust use react\b"),
        (r"\bparameteri[sz]ed quer(?:y|ies) only\b", r"\bstring concatenat"),
        (r"\bdo not commit\b", r"\balways commit\b"),
    )
    for basename, items in by_base.items():
        roots = [item for item in items if item.scope == "root"]
        subs = [item for item in items if item.scope == "subdir"]
        for root_item in roots:
            for sub_item in subs:
                root_text = root_item.content.lower()
                sub_text = sub_item.content.lower()
                if any(
                    (re.search(a, root_text) and re.search(b, sub_text))
                    or (re.search(b, root_text) and re.search(a, sub_text))
                    for a, b in negation_pairs
                ):
                    conflicts.append(
                        {
                            "basename": basename,
                            "root_path": root_item.path,
                            "subdir_path": sub_item.path,
                            "note": "possible contradiction between root and subdir instructions",
                        }
                    )
    return conflicts


def resolve_effective_directives(
    *,
    safety: Sequence[str],
    explicit_user: Sequence[str],
    project_excerpts: Sequence[str],
    preferences: Mapping[str, Any],
    defaults: Sequence[str],
) -> dict[str, Any]:
    return {
        "precedence": list(PRECEDENCE),
        "layers": {
            "safety": list(safety),
            "explicit_user_instruction": list(explicit_user),
            "project_instruction": list(project_excerpts),
            "preferences": dict(preferences),
            "defaults": list(defaults),
        },
        "rule": (
            "When directives conflict, obey the highest precedence layer. Safety "
            "constraints cannot be overridden. Explicit user instructions override "
            "project files; project files override preferences; preferences override defaults."
        ),
    }


def build_worker_context(
    spec: WorkerTaskSpec,
    *,
    project_root: Path,
    preferences: Mapping[str, Any] | None = None,
    known_repository_skills: Iterable[str] | None = None,
    project_instructions: Sequence[InstructionFile] | None = None,
    skip_project_instructions: bool = False,
) -> dict[str, Any]:
    if not spec.objective or not str(spec.objective).strip():
        raise WorkerContextError("objective is required")
    if spec.role not in ROLES:
        raise WorkerContextError(f"invalid role: {spec.role}")
    if spec.risk not in VALID_RISKS:
        raise WorkerContextError(f"invalid risk: {spec.risk}")

    root = Path(project_root)
    if project_instructions is not None:
        instructions = list(project_instructions)
    elif skip_project_instructions:
        instructions = []
    else:
        instructions = discover_project_instructions(root, work_subdir=spec.work_subdir)

    manifest_skills = load_manifest_skill_ids(root)
    skills_projected = resolve_skills_projected(
        task_skills=spec.skills,
        manifest_skills=manifest_skills,
        include_manifest_skills=spec.include_manifest_skills,
        known_repository_skills=known_repository_skills,
    )

    try:
        capability_catalog = load_capability_catalog()
        specialist_requirements = specialist_capability_requirements(
            spec.specialist_ids,
            capability_catalog=capability_catalog,
        )
        required_capabilities = list(
            dict.fromkeys([*specialist_requirements["required"], *spec.required_capabilities])
        )
        preferred_capabilities = [
            capability
            for capability in dict.fromkeys(
                [*specialist_requirements["preferred"], *spec.preferred_capabilities]
            )
            if capability not in required_capabilities
        ]
        capability_envelope = resolve_capabilities(
            required=required_capabilities,
            preferred=preferred_capabilities,
            available_providers=spec.available_providers,
            host=spec.provider_host,
            catalog=capability_catalog,
        )
    except CapabilityCatalogError as exc:
        raise WorkerContextError(str(exc)) from exc

    prefs = project_preferences(preferences)
    constraints = build_constraints(spec)
    safety = _dedup_text(
        [
            *spec.safety_constraints,
            *[
                item
                for item in constraints
                if item.startswith("no ") or item.startswith("read-only")
            ],
        ]
    )
    project_excerpts = [
        f"[{item.path}] {item.content.strip()[:500]}"
        for item in instructions
        if item.content.strip()
    ]
    effective = resolve_effective_directives(
        safety=safety,
        explicit_user=list(spec.explicit_user_instructions),
        project_excerpts=project_excerpts,
        preferences=prefs,
        defaults=list(DEFAULT_CONSTRAINTS),
    )

    artifact_refs = _dedup_text(spec.artifact_uris)
    reference_refs = _dedup_text(spec.references)
    for value in [*artifact_refs, *reference_refs]:
        if _SECRET_VALUE_RE.search(value):
            raise WorkerContextError("refusing to project secret-shaped reference/artifact")

    context: dict[str, Any] = {
        "schema_version": 2,
        "role": spec.role,
        "objective": spec.objective.strip(),
        "scope": spec.scope.strip(),
        "project_instructions": [
            {
                "path": item.path,
                "basename": item.basename,
                "scope": item.scope,
                "sha256_prefix": item.sha256_prefix,
                "content": item.content,
            }
            for item in instructions
        ],
        "project_instruction_paths": [item.path for item in instructions],
        "relevant_packs": _dedup_text(spec.relevant_packs),
        "skills_projected": skills_projected,
        "references_projected": reference_refs,
        "specialist_ids": _dedup_text(spec.specialist_ids),
        "capability_envelope": capability_envelope,
        "preferences_projected": prefs,
        "risk": spec.risk,
        "constraints": constraints,
        "allowed_files": list(spec.allowed_files),
        "write_paths": list(spec.write_paths),
        "artifact_uris": artifact_refs,
        "expected_output": spec.expected_output.strip(),
        "verification": spec.verification.strip(),
        "stop_condition": spec.stop_condition.strip(),
        "explicit_user_instructions": list(spec.explicit_user_instructions),
        "instruction_conflicts": detect_instruction_conflicts(instructions),
        "effective_directives": effective,
        "projection": {
            "project_instructions_projected": bool(instructions),
            "skip_project_instructions": bool(skip_project_instructions),
            "skills_count": len(skills_projected),
            "references_count": len(reference_refs),
            "manifest_skills_available": list(manifest_skills),
            "full_catalog_forbidden": True,
        },
        "orchestration": {
            "parent_topology": spec.parent_topology.strip(),
            "independent_review_required": bool(spec.independent_review_required),
        },
    }
    return {"worker_context": context}


def assert_projection_complete(payload: Mapping[str, Any]) -> None:
    if "worker_context" not in payload or not isinstance(payload["worker_context"], dict):
        raise WorkerContextError("missing or invalid worker_context root key")
    context = payload["worker_context"]
    for key in ("schema_version", "objective", "risk", "role", "constraints"):
        if key not in context:
            raise WorkerContextError(f"worker_context missing required field: {key}")
    if not str(context["objective"]).strip():
        raise WorkerContextError("objective must be non-empty")
    if context["risk"] not in VALID_RISKS:
        raise WorkerContextError(f"invalid risk in payload: {context['risk']}")
    if context["role"] not in ROLES:
        raise WorkerContextError(f"invalid role in payload: {context['role']}")
    if not isinstance(context["constraints"], list) or not context["constraints"]:
        raise WorkerContextError("constraints must be a non-empty list")

    projection = context.get("projection") or {}
    if projection.get("skip_project_instructions"):
        raise WorkerContextError(
            "projection incomplete: project instructions were deliberately skipped "
            "(fresh negligence / GSD #671 class failure)"
        )
    for key in ("project_instructions", "skills_projected", "relevant_packs", "references_projected"):
        if key not in context:
            raise WorkerContextError(f"{key} field missing")

    envelope = context.get("capability_envelope")
    if not isinstance(envelope, dict):
        raise WorkerContextError("capability_envelope field missing")
    if envelope.get("least_privilege") is not True:
        raise WorkerContextError("capability envelope must enforce least privilege")
    try:
        validate_capability_envelope(envelope)
    except CapabilityCatalogError as exc:
        raise WorkerContextError(str(exc)) from exc

    prefs = context.get("preferences_projected")
    if not isinstance(prefs, dict):
        raise WorkerContextError("preferences_projected field missing")
    for key, value in prefs.items():
        if _SECRET_KEY_RE.search(str(key)):
            raise WorkerContextError(f"secret-shaped preference key projected: {key}")
        if isinstance(value, str) and _SECRET_VALUE_RE.search(value):
            raise WorkerContextError("secret-shaped preference value projected")

    if _SECRET_VALUE_RE.search(json.dumps(context, ensure_ascii=False)):
        raise WorkerContextError("secret-shaped material detected in worker_context")


def validate_for_spawn(
    payload: Mapping[str, Any],
    *,
    require_project_instructions: bool = False,
    max_skills: int | None = None,
    repository_skill_count: int | None = None,
) -> None:
    assert_projection_complete(payload)
    context = payload["worker_context"]
    instructions = context.get("project_instructions") or []
    if require_project_instructions and not instructions:
        raise WorkerContextError("spawn rejected: project instructions required but none projected")
    skills = context.get("skills_projected") or []
    if max_skills is not None and len(skills) > max_skills:
        raise WorkerContextError(
            f"spawn rejected: {len(skills)} skills projected exceeds max_skills={max_skills}"
        )
    if repository_skill_count and repository_skill_count > 5 and len(skills) >= repository_skill_count:
        raise WorkerContextError("spawn rejected: skills_projected looks like a full-catalog dump")
    envelope = context.get("capability_envelope") or {}
    unresolved = envelope.get("unresolved_required") or []
    if unresolved:
        raise WorkerContextError(
            f"spawn rejected: unresolved required capabilities: {', '.join(unresolved)}"
        )
    pending = envelope.get("pending_inventory") or []
    if pending:
        raise WorkerContextError(
            "spawn rejected: provider inventory required for capabilities: " + ", ".join(pending)
        )


def render_worker_prompt(payload: Mapping[str, Any]) -> str:
    assert_projection_complete(payload)
    context = payload["worker_context"]
    lines = [
        "# Worker Context Contract",
        "",
        "You are a delegated worker. You do not speak to the user.",
        "Obey the precedence rule: safety > explicit user instruction > project instruction > preferences > defaults.",
        "",
        f"## Role\n{context['role']}",
        f"## Risk\n{context['risk']}",
        f"## Objective\n{context['objective']}",
    ]
    if context.get("scope"):
        lines.append(f"## Scope\n{context['scope']}")

    packs = context.get("relevant_packs") or []
    orchestration = context.get("orchestration") or {}
    if packs or orchestration.get("parent_topology") or orchestration.get("independent_review_required"):
        lines.append("## Orchestration context")
        if packs:
            lines.append("- relevant_packs: " + ", ".join(packs))
        if orchestration.get("parent_topology"):
            lines.append(f"- parent_topology: {orchestration['parent_topology']}")
        if orchestration.get("independent_review_required"):
            lines.append("- independent_review_required: true")

    lines.append("## Constraints (mandatory)")
    lines.extend(f"- {item}" for item in context["constraints"])

    if context.get("explicit_user_instructions"):
        lines.append("## Explicit user instructions (override project files)")
        lines.extend(f"- {item}" for item in context["explicit_user_instructions"])

    instructions = context.get("project_instructions") or []
    if instructions:
        lines.append("## Project instructions (must follow)")
        for item in instructions:
            lines.extend([f"### {item['path']} ({item['scope']})", item["content"].rstrip(), ""])
    else:
        lines.append("## Project instructions\n(none found at project root or work_subdir)")

    lines.append("## Active skills for this task (only these; not the full catalog)")
    skills = context.get("skills_projected") or []
    lines.extend(f"- {item}" for item in skills) if skills else lines.append("- (none projected for this task)")

    references = context.get("references_projected") or []
    if references:
        lines.append("## Selected references")
        lines.extend(f"- {item}" for item in references)

    envelope = context.get("capability_envelope") or {}
    lines.append("## Capability envelope (least privilege)")
    if envelope.get("inventory_provided"):
        grants = envelope.get("grants") or []
        if grants:
            for grant in grants:
                permissions = ", ".join(grant.get("permissions") or [])
                lines.append(f"- {grant['capability']} via {grant['provider']}: {permissions}")
        else:
            lines.append("- (no provider grants)")
    else:
        pending = ", ".join(envelope.get("pending_inventory") or []) or "none"
        lines.append(f"- provider inventory required before execution: {pending}")

    prefs = context.get("preferences_projected") or {}
    if prefs:
        lines.append("## Applied user preferences")
        lines.extend(f"- {key}: {value}" for key, value in prefs.items())

    for heading, key in (("Allowed read paths", "allowed_files"), ("Allowed write paths", "write_paths"), ("Artifact references", "artifact_uris")):
        values = context.get(key) or []
        if values:
            lines.append(f"## {heading}")
            lines.extend(f"- {value}" for value in values)

    if context.get("expected_output"):
        lines.append(f"## Expected output\n{context['expected_output']}")
    if context.get("verification"):
        lines.append(f"## Verification\n{context['verification']}")
    if context.get("stop_condition"):
        lines.append(f"## Stop condition\n{context['stop_condition']}")

    conflicts = context.get("instruction_conflicts") or []
    if conflicts:
        lines.append("## Instruction conflict warnings")
        lines.append("Resolve ambiguity using directive precedence; escalate when still material.")
        for conflict in conflicts:
            lines.append(
                f"- {conflict.get('basename')}: {conflict.get('root_path')} vs {conflict.get('subdir_path')}"
            )

    lines.extend(
        [
            "",
            "## Forbidden",
            "- Silently dropping project instructions",
            "- Loading every global skill or whole pack by default",
            "- Forwarding secrets unrelated to the task",
            "- Commits, pushes, or external changes unless explicitly authorized",
            "",
            "## Return receipt",
            "result; files/artifacts; verification evidence; risks; stop reason.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_and_validate(
    spec: WorkerTaskSpec,
    *,
    project_root: Path,
    preferences: Mapping[str, Any] | None = None,
    known_repository_skills: Iterable[str] | None = None,
    require_project_instructions: bool = False,
    max_skills: int | None = 12,
    repository_skill_count: int | None = None,
    skip_project_instructions: bool = False,
) -> dict[str, Any]:
    payload = build_worker_context(
        spec,
        project_root=project_root,
        preferences=preferences,
        known_repository_skills=known_repository_skills,
        skip_project_instructions=skip_project_instructions,
    )
    validate_for_spawn(
        payload,
        require_project_instructions=require_project_instructions,
        max_skills=max_skills,
        repository_skill_count=repository_skill_count,
    )
    return payload


def _spec_from_mapping(data: Mapping[str, Any]) -> WorkerTaskSpec:
    return WorkerTaskSpec(
        objective=str(data.get("objective", "")),
        scope=str(data.get("scope", "")),
        role=str(data.get("role", "implementer")),
        risk=str(data.get("risk", "RISK_2")),
        skills=tuple(data.get("skills") or ()),
        relevant_packs=tuple(data.get("relevant_packs") or ()),
        references=tuple(data.get("references") or ()),
        allowed_files=tuple(data.get("allowed_files") or ()),
        write_paths=tuple(data.get("write_paths") or ()),
        artifact_uris=tuple(data.get("artifact_uris") or ()),
        expected_output=str(data.get("expected_output", "")),
        verification=str(data.get("verification", "")),
        stop_condition=str(data.get("stop_condition", "")),
        explicit_user_instructions=tuple(data.get("explicit_user_instructions") or ()),
        safety_constraints=tuple(data.get("safety_constraints") or ()),
        extra_constraints=tuple(data.get("extra_constraints") or ()),
        authorize_commits=bool(data.get("authorize_commits", False)),
        authorize_push=bool(data.get("authorize_push", False)),
        authorize_external=bool(data.get("authorize_external", False)),
        work_subdir=data.get("work_subdir"),
        include_manifest_skills=bool(data.get("include_manifest_skills", False)),
        parent_topology=str(data.get("parent_topology", "")),
        independent_review_required=bool(data.get("independent_review_required", False)),
        specialist_ids=tuple(data.get("specialist_ids") or ()),
        required_capabilities=tuple(data.get("required_capabilities") or ()),
        preferred_capabilities=tuple(data.get("preferred_capabilities") or ()),
        available_providers=(
            tuple(data.get("available_providers") or ())
            if data.get("available_providers") is not None
            else None
        ),
        provider_host=str(data.get("provider_host", "local")),
    )


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Build an auditable bounded Worker Context Contract.")
    parser.add_argument("command", nargs="?", default="build", choices=("build", "render", "validate"))
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--objective", default="")
    parser.add_argument("--scope", default="")
    parser.add_argument("--role", default="implementer", choices=sorted(ROLES))
    parser.add_argument("--risk", default="RISK_2", choices=sorted(VALID_RISKS))
    parser.add_argument("--skill", action="append", default=[], dest="skills")
    parser.add_argument("--pack", action="append", default=[], dest="packs")
    parser.add_argument("--reference", action="append", default=[], dest="references")
    parser.add_argument("--verification", default="")
    parser.add_argument("--expected-output", default="")
    parser.add_argument("--work-subdir", default=None)
    parser.add_argument("--user-instruction", action="append", default=[])
    parser.add_argument("--artifact", action="append", default=[], dest="artifacts")
    parser.add_argument("--include-manifest-skills", action="store_true")
    parser.add_argument("--require-project-instructions", action="store_true")
    parser.add_argument("--skip-project-instructions", action="store_true")
    parser.add_argument("--spec-json", type=Path)
    parser.add_argument("--preferences-json", type=Path)
    parser.add_argument("--format", choices=("json", "prompt"), default="json")
    args = parser.parse_args(argv)

    try:
        data: dict[str, Any] = {}
        if args.spec_json:
            data = json.loads(args.spec_json.read_text(encoding="utf-8"))
        if args.objective:
            data["objective"] = args.objective
        if args.scope:
            data["scope"] = args.scope
        data.setdefault("role", args.role)
        data.setdefault("risk", args.risk)
        if args.skills:
            data["skills"] = args.skills
        if args.packs:
            data["relevant_packs"] = args.packs
        if args.references:
            data["references"] = args.references
        if args.verification:
            data["verification"] = args.verification
        if args.expected_output:
            data["expected_output"] = args.expected_output
        if args.work_subdir:
            data["work_subdir"] = args.work_subdir
        if args.user_instruction:
            data["explicit_user_instructions"] = args.user_instruction
        if args.artifacts:
            data["artifact_uris"] = args.artifacts
        if args.include_manifest_skills:
            data["include_manifest_skills"] = True

        prefs = None
        if args.preferences_json:
            prefs = json.loads(args.preferences_json.read_text(encoding="utf-8"))

        payload = build_worker_context(
            _spec_from_mapping(data),
            project_root=args.project.resolve(),
            preferences=prefs,
            skip_project_instructions=args.skip_project_instructions,
        )
        validate_for_spawn(payload, require_project_instructions=args.require_project_instructions)
        if args.command == "render" or args.format == "prompt":
            sys.stdout.write(render_worker_prompt(payload))
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except (WorkerContextError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
