"""Worker Context Contract — mandatory projection before delegated spawn.

Fresh context without project instructions is fresh negligence (GSD #671 lesson).
Every subagent spawn must pass through build_worker_context() so project
instructions, task-scoped skills, preferences, risk and constraints are
projected into an auditable payload.

This module is runtime topology infrastructure, not a skill.
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

# Discovery names (highest local path wins within project_instruction tier;
# explicit user instructions and safety always outrank these).
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

VALID_RISKS: frozenset[str] = frozenset(
    {"RISK_1", "RISK_2", "RISK_3", "RISK_4"}
)

# Preference keys safe to project into a worker (style/tooling only).
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
    scope: str  # "root" | "subdir"
    content: str
    sha256_prefix: str


@dataclass
class WorkerTaskSpec:
    """Declarative task input for worker projection."""

    objective: str
    scope: str = ""
    role: str = "implementer"
    risk: str = "RISK_2"
    skills: Sequence[str] = field(default_factory=tuple)
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
    # When True, merge project-manifest active skills then intersect with
    # task skills if task skills are non-empty; never the full catalog.
    include_manifest_skills: bool = False
    domain_pack: str = ""
    craft_depth: str | None = None
    spend: str = ""
    critic_required: bool = False
    specialist_id: str = ""
    model_tier: str = ""
    parent_topology: str = ""
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


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def discover_project_instructions(
    project_root: Path,
    *,
    work_subdir: str | None = None,
) -> list[InstructionFile]:
    """Discover instruction files at project root and optional work subdir.

    Root files are always considered. If work_subdir is set, matching files
    under that subdirectory are also loaded (subdir scope). Symlinks rejected.
    Missing files are silent (not an error).
    """
    root = Path(project_root)
    if not root.is_dir() or root.is_symlink():
        raise WorkerContextError(f"project root must be a regular directory: {root}")

    found: list[InstructionFile] = []

    def collect(directory: Path, scope: str) -> None:
        if not directory.is_dir() or directory.is_symlink():
            return
        try:
            directory.resolve().relative_to(root.resolve())
        except ValueError as exc:
            raise WorkerContextError(
                f"instruction directory escapes project root: {directory}"
            ) from exc
        for basename in INSTRUCTION_BASENAMES:
            path = directory / basename
            if not _is_safe_regular_file(path):
                continue
            content = _read_text(path)
            rel = str(path.relative_to(root))
            found.append(
                InstructionFile(
                    path=rel,
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
            sub.relative_to(root.resolve())
        except ValueError as exc:
            raise WorkerContextError(
                f"work_subdir escapes project root: {work_subdir}"
            ) from exc
        if sub != root.resolve():
            collect(sub, "subdir")

    return found


def load_manifest_skill_ids(project_root: Path) -> list[str]:
    """Return skill ids from .agentit/skills-manifest.json if present."""
    manifest_path = Path(project_root) / ".agentit" / "skills-manifest.json"
    if not _is_safe_regular_file(manifest_path):
        return []
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkerContextError(f"invalid skills manifest: {exc}") from exc
    skills = payload.get("skills")
    if isinstance(skills, dict):
        return sorted(str(k) for k in skills.keys())
    if isinstance(skills, list):
        return [str(s) for s in skills if isinstance(s, str) and s.strip()]
    return []


def project_preferences(
    preferences: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Project only safe style preferences; drop secret-shaped keys/values."""
    if not preferences:
        return {}
    style = preferences.get("user_style_preferences")
    if not isinstance(style, dict):
        style = {
            k: preferences[k]
            for k in PROJECTABLE_PREFERENCE_KEYS
            if k in preferences
        }
    projected: dict[str, Any] = {}
    for key in PROJECTABLE_PREFERENCE_KEYS:
        if key not in style:
            continue
        if _SECRET_KEY_RE.search(key):
            continue
        value = style[key]
        if isinstance(value, str) and _SECRET_VALUE_RE.search(value):
            continue
        if isinstance(value, str) and _SECRET_KEY_RE.search(value):
            # value itself looks like a secret label dump
            if len(value) > 40:
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
    """Project only task-necessary skills — never the full catalog.

    Rules:
    - If task_skills is non-empty: use those (deduped, order preserved).
    - Elif include_manifest_skills: use manifest active skills only.
    - Else: empty list (allowed for pure mechanical tasks).
    - If known_repository_skills is provided, unknown ids fail closed.
    - Never auto-expands to all repository skills.
    """
    known = set(known_repository_skills) if known_repository_skills is not None else None
    ordered: list[str] = []

    def add_many(ids: Sequence[str]) -> None:
        for skill_id in ids:
            sid = skill_id.strip()
            if not sid:
                continue
            if known is not None and sid not in known:
                raise WorkerContextError(f"unknown skill id for projection: {sid}")
            if sid not in ordered:
                ordered.append(sid)

    if task_skills:
        add_many(task_skills)
        return ordered
    if include_manifest_skills and manifest_skills:
        add_many(manifest_skills)
        return ordered
    return []


def build_constraints(
    spec: WorkerTaskSpec,
) -> list[str]:
    """Assemble constraints with safety first; honors explicit authorizations."""
    constraints: list[str] = []

    def add(item: str) -> None:
        text = item.strip()
        if text and text not in constraints:
            constraints.append(text)

    for item in spec.safety_constraints:
        add(item)

    if not spec.authorize_commits:
        add("no commits")
    if not spec.authorize_push:
        add("no pushes")
    if not spec.authorize_external:
        add("no external changes")
    add("no dependency changes")

    for item in DEFAULT_CONSTRAINTS:
        add(item)
    for item in spec.extra_constraints:
        add(item)

    if spec.role == "reviewer":
        add("read-only: do not modify source files")
        add("do not implement features; review only")
    if spec.role == "probe":
        add("read-only investigation")
        add("do not modify source files")
    if spec.critic_required and spec.role in {"reviewer", "probe"}:
        add("independent critic: challenge assumptions; do not rubber-stamp the parent plan")

    return constraints


def detect_instruction_conflicts(
    instructions: Sequence[InstructionFile],
) -> list[dict[str, str]]:
    """Heuristic conflict signals between root and subdir instruction files.

    Detects simple contradictory pairs on the same basename (root vs subdir)
    when both contain opposing absolute language. This is advisory metadata;
    safety + explicit user instructions still win at resolution time.
    """
    by_base: dict[str, list[InstructionFile]] = {}
    for inst in instructions:
        by_base.setdefault(inst.basename, []).append(inst)

    conflicts: list[dict[str, str]] = []
    negation_pairs = (
        (r"\bnever use react\b", r"\balways use react\b"),
        (r"\bno react\b", r"\bmust use react\b"),
        (r"\bparameteri[sz]ed quer(?:y|ies) only\b", r"\bstring concatenat"),
        (r"\bdo not commit\b", r"\balways commit\b"),
    )
    for basename, items in by_base.items():
        if len(items) < 2:
            continue
        roots = [i for i in items if i.scope == "root"]
        subs = [i for i in items if i.scope == "subdir"]
        for root_i in roots:
            for sub_i in subs:
                root_l = root_i.content.lower()
                sub_l = sub_i.content.lower()
                for a, b in negation_pairs:
                    if (re.search(a, root_l) and re.search(b, sub_l)) or (
                        re.search(b, root_l) and re.search(a, sub_l)
                    ):
                        conflicts.append(
                            {
                                "basename": basename,
                                "root_path": root_i.path,
                                "subdir_path": sub_i.path,
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
    """Apply precedence: safety > user > project > preferences > defaults.

    Returns a structured resolution map for audit, not a free-form merge that
    would let lower tiers override higher ones.
    """
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
            "When directives conflict, obey the highest precedence layer. "
            "Safety constraints cannot be overridden by user, project, "
            "preferences, or defaults. Explicit user instructions override "
            "project files. Project files override preferences. Preferences "
            "override built-in defaults."
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
    """Build the auditable worker_context payload.

    Parameters
    ----------
    skip_project_instructions:
        Test/debug only. When True, omits project instruction projection so
        assert_projection_complete() fails — used to prove the #671 regression.
    """
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
        instructions = discover_project_instructions(
            root, work_subdir=spec.work_subdir
        )

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
            dict.fromkeys(
                [*specialist_requirements["required"], *spec.required_capabilities]
            )
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
    safety = list(spec.safety_constraints) + [
        c for c in constraints if c.startswith("no ") or c.startswith("read-only")
    ]
    # Dedup safety while preserving order
    seen_s: set[str] = set()
    safety_unique: list[str] = []
    for item in safety:
        if item not in seen_s:
            seen_s.add(item)
            safety_unique.append(item)

    conflicts = detect_instruction_conflicts(instructions)
    project_excerpts = [
        f"[{inst.path}] {inst.content.strip()[:500]}"
        for inst in instructions
        if inst.content.strip()
    ]

    effective = resolve_effective_directives(
        safety=safety_unique,
        explicit_user=list(spec.explicit_user_instructions),
        project_excerpts=project_excerpts,
        preferences=prefs,
        defaults=list(DEFAULT_CONSTRAINTS),
    )

    # Artifact URIs must look like agentit:// or relative paths — no secret dumps.
    artifact_refs: list[str] = []
    for uri in spec.artifact_uris:
        text = str(uri).strip()
        if not text:
            continue
        if _SECRET_VALUE_RE.search(text):
            raise WorkerContextError("refusing to project secret-shaped artifact URI")
        artifact_refs.append(text)

    worker_context: dict[str, Any] = {
        "schema_version": 1,
        "role": spec.role,
        "objective": spec.objective.strip(),
        "scope": (spec.scope or "").strip(),
        "project_instructions": [
            {
                "path": inst.path,
                "basename": inst.basename,
                "scope": inst.scope,
                "sha256_prefix": inst.sha256_prefix,
                "content": inst.content,
            }
            for inst in instructions
        ],
        "project_instruction_paths": [inst.path for inst in instructions],
        "skills_projected": skills_projected,
        "specialist_ids": list(spec.specialist_ids),
        "capability_envelope": capability_envelope,
        "preferences_projected": prefs,
        "risk": spec.risk,
        "constraints": constraints,
        "allowed_files": list(spec.allowed_files),
        "write_paths": list(spec.write_paths),
        "artifact_uris": artifact_refs,
        "expected_output": (spec.expected_output or "").strip(),
        "verification": (spec.verification or "").strip(),
        "stop_condition": (spec.stop_condition or "").strip(),
        "explicit_user_instructions": list(spec.explicit_user_instructions),
        "instruction_conflicts": conflicts,
        "effective_directives": effective,
        "projection": {
            "project_instructions_projected": bool(instructions),
            "skip_project_instructions": bool(skip_project_instructions),
            "skills_count": len(skills_projected),
            "manifest_skills_available": list(manifest_skills),
            "full_catalog_forbidden": True,
        },
        "orchestration": {
            "domain_pack": (spec.domain_pack or "").strip(),
            "craft_depth": spec.craft_depth,
            "spend": (spec.spend or "").strip(),
            "critic_required": bool(spec.critic_required),
            "specialist_id": (spec.specialist_id or "").strip(),
            "model_tier": (spec.model_tier or "").strip(),
            "parent_topology": (spec.parent_topology or "").strip(),
        },
    }
    return {"worker_context": worker_context}


def assert_projection_complete(payload: Mapping[str, Any]) -> None:
    """Fail closed if mandatory projection fields are missing or empty when required.

    Rules:
    - worker_context object must exist with schema_version, objective, risk, role
    - project instructions must be projected unless the project truly has none
      AND skip was not used; if skip_project_instructions is True → always fail
    - constraints must be non-empty
    - skills_projected must not equal a full dump when a bound is provided
      (checked separately via assert_skills_bounded)
    - secrets must not appear in projected preferences or instruction paths
    """
    if "worker_context" not in payload:
        raise WorkerContextError("missing worker_context root key")
    ctx = payload["worker_context"]
    if not isinstance(ctx, dict):
        raise WorkerContextError("worker_context must be an object")

    for key in ("schema_version", "objective", "risk", "role", "constraints"):
        if key not in ctx:
            raise WorkerContextError(f"worker_context missing required field: {key}")

    if not str(ctx["objective"]).strip():
        raise WorkerContextError("objective must be non-empty")
    if ctx["risk"] not in VALID_RISKS:
        raise WorkerContextError(f"invalid risk in payload: {ctx['risk']}")
    if ctx["role"] not in ROLES:
        raise WorkerContextError(f"invalid role in payload: {ctx['role']}")
    if not isinstance(ctx["constraints"], list) or not ctx["constraints"]:
        raise WorkerContextError("constraints must be a non-empty list")

    projection = ctx.get("projection") or {}
    if projection.get("skip_project_instructions"):
        raise WorkerContextError(
            "projection incomplete: project instructions were deliberately skipped "
            "(fresh negligence / GSD #671 class failure)"
        )

    # Instructions may be legitimately empty if the project has none; that is
    # recorded in projection flags. Callers that require files should use
    # require_project_instructions=True via validate_for_spawn.
    if "project_instructions" not in ctx:
        raise WorkerContextError("project_instructions field missing")
    if "skills_projected" not in ctx:
        raise WorkerContextError("skills_projected field missing")
    envelope = ctx.get("capability_envelope")
    if not isinstance(envelope, dict):
        raise WorkerContextError("capability_envelope field missing")
    if envelope.get("least_privilege") is not True:
        raise WorkerContextError("capability envelope must enforce least privilege")
    try:
        validate_capability_envelope(envelope)
    except CapabilityCatalogError as exc:
        raise WorkerContextError(str(exc)) from exc
    if "preferences_projected" not in ctx:
        raise WorkerContextError("preferences_projected field missing")

    prefs = ctx.get("preferences_projected") or {}
    if isinstance(prefs, dict):
        for key, value in prefs.items():
            if _SECRET_KEY_RE.search(str(key)):
                raise WorkerContextError(f"secret-shaped preference key projected: {key}")
            if isinstance(value, str) and _SECRET_VALUE_RE.search(value):
                raise WorkerContextError("secret-shaped preference value projected")

    blob = json.dumps(ctx, ensure_ascii=False)
    if _SECRET_VALUE_RE.search(blob):
        raise WorkerContextError("secret-shaped material detected in worker_context")


def validate_for_spawn(
    payload: Mapping[str, Any],
    *,
    require_project_instructions: bool = False,
    max_skills: int | None = None,
    repository_skill_count: int | None = None,
) -> None:
    """Full pre-spawn gate used by the delegation runtime."""
    assert_projection_complete(payload)
    ctx = payload["worker_context"]
    instructions = ctx.get("project_instructions") or []
    if require_project_instructions and not instructions:
        raise WorkerContextError(
            "spawn rejected: project instructions required but none projected"
        )
    skills = ctx.get("skills_projected") or []
    if max_skills is not None and len(skills) > max_skills:
        raise WorkerContextError(
            f"spawn rejected: {len(skills)} skills projected exceeds max_skills={max_skills}"
        )
    if repository_skill_count is not None and repository_skill_count > 0:
        if len(skills) >= repository_skill_count and repository_skill_count > 5:
            raise WorkerContextError(
                "spawn rejected: skills_projected looks like a full-catalog dump"
            )
    unresolved = (ctx.get("capability_envelope") or {}).get("unresolved_required") or []
    if unresolved:
        raise WorkerContextError(
            f"spawn rejected: unresolved required capabilities: {', '.join(unresolved)}"
        )
    pending = (ctx.get("capability_envelope") or {}).get("pending_inventory") or []
    if pending:
        raise WorkerContextError(
            "spawn rejected: provider inventory required for capabilities: "
            + ", ".join(pending)
        )


def render_worker_prompt(payload: Mapping[str, Any]) -> str:
    """Render a worker prompt that embeds the projected contract.

    The prompt is the operational surface; the JSON payload is the audit surface.
    """
    assert_projection_complete(payload)
    ctx = payload["worker_context"]
    lines: list[str] = [
        "# Worker Context Contract",
        "",
        "You are a delegated worker. You do not speak to the user.",
        "Obey the precedence rule: safety > explicit user instruction > "
        "project instruction > preferences > defaults.",
        "",
        f"## Role\n{ctx['role']}",
        f"## Risk\n{ctx['risk']}",
        f"## Objective\n{ctx['objective']}",
    ]
    if ctx.get("scope"):
        lines.append(f"## Scope\n{ctx['scope']}")

    orch = ctx.get("orchestration") or {}
    if any(orch.get(k) for k in ("domain_pack", "specialist_id", "model_tier", "parent_topology")) or orch.get(
        "critic_required"
    ):
        lines.append("## Orchestration context")
        if orch.get("domain_pack"):
            lines.append(f"- domain_pack: {orch['domain_pack']}")
        if orch.get("craft_depth"):
            lines.append(f"- craft_depth: {orch['craft_depth']}")
        if orch.get("spend"):
            lines.append(f"- spend: {orch['spend']}")
        if orch.get("specialist_id"):
            lines.append(f"- specialist_id: {orch['specialist_id']}")
        if orch.get("model_tier"):
            lines.append(f"- model_tier: {orch['model_tier']}")
        if orch.get("parent_topology"):
            lines.append(f"- parent_topology: {orch['parent_topology']}")
        if orch.get("critic_required"):
            lines.append("- critic_required: true (challenge the plan; do not rubber-stamp)")

    lines.append("## Constraints (mandatory)")
    for item in ctx["constraints"]:
        lines.append(f"- {item}")

    if ctx.get("explicit_user_instructions"):
        lines.append("## Explicit user instructions (override project files)")
        for item in ctx["explicit_user_instructions"]:
            lines.append(f"- {item}")

    instructions = ctx.get("project_instructions") or []
    if instructions:
        lines.append("## Project instructions (must follow)")
        for inst in instructions:
            lines.append(f"### {inst['path']} ({inst['scope']})")
            lines.append(inst["content"].rstrip())
            lines.append("")
    else:
        lines.append(
            "## Project instructions\n(none found at project root or work_subdir)"
        )

    skills = ctx.get("skills_projected") or []
    lines.append("## Active skills for this task (only these; not the full catalog)")
    if skills:
        for sid in skills:
            lines.append(f"- {sid}")
    else:
        lines.append("- (none projected for this task)")

    envelope = ctx.get("capability_envelope") or {}
    lines.append("## Capability envelope (least privilege)")
    if envelope.get("inventory_provided"):
        grants = envelope.get("grants") or []
        if grants:
            for grant in grants:
                permissions = ", ".join(grant.get("permissions") or [])
                lines.append(
                    f"- {grant['capability']} via {grant['provider']}: {permissions}"
                )
        else:
            lines.append("- (no provider grants)")
    else:
        pending = ", ".join(envelope.get("pending_inventory") or []) or "none"
        lines.append(f"- provider inventory required before execution: {pending}")

    prefs = ctx.get("preferences_projected") or {}
    if prefs:
        lines.append("## Applied user preferences")
        for key, value in prefs.items():
            lines.append(f"- {key}: {value}")

    if ctx.get("allowed_files"):
        lines.append("## Allowed read paths")
        for path in ctx["allowed_files"]:
            lines.append(f"- {path}")
    if ctx.get("write_paths"):
        lines.append("## Allowed write paths")
        for path in ctx["write_paths"]:
            lines.append(f"- {path}")
    if ctx.get("artifact_uris"):
        lines.append("## Artifact references")
        for uri in ctx["artifact_uris"]:
            lines.append(f"- {uri}")

    if ctx.get("expected_output"):
        lines.append(f"## Expected output\n{ctx['expected_output']}")
    if ctx.get("verification"):
        lines.append(f"## Verification\n{ctx['verification']}")
    if ctx.get("stop_condition"):
        lines.append(f"## Stop condition\n{ctx['stop_condition']}")

    conflicts = ctx.get("instruction_conflicts") or []
    if conflicts:
        lines.append("## Instruction conflict warnings")
        lines.append(
            "Resolve using precedence (safety > user > project root vs subdir "
            "is still under project_instruction; escalate if ambiguous)."
        )
        for conflict in conflicts:
            lines.append(
                f"- {conflict.get('basename')}: {conflict.get('root_path')} vs "
                f"{conflict.get('subdir_path')}"
            )

    lines.extend(
        [
            "",
            "## Forbidden",
            "- Silently dropping project instructions",
            "- Loading every global skill",
            "- Forwarding secrets unrelated to the task",
            "- Commits, pushes, or external changes unless constraints allow them",
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
    """Convenience: build, validate for spawn, return payload."""
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


# --- CLI helpers -----------------------------------------------------------------


def _spec_from_mapping(data: Mapping[str, Any]) -> WorkerTaskSpec:
    return WorkerTaskSpec(
        objective=str(data.get("objective", "")),
        scope=str(data.get("scope", "")),
        role=str(data.get("role", "implementer")),
        risk=str(data.get("risk", "RISK_2")),
        skills=tuple(data.get("skills") or ()),
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
    )


def main(argv: list[str] | None = None) -> int:
    """CLI: python3 -m router.worker_context build --project DIR --objective ..."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Build an auditable Worker Context Contract payload."
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="build",
        choices=("build", "render", "validate"),
    )
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--objective", default="")
    parser.add_argument("--scope", default="")
    parser.add_argument("--role", default="implementer", choices=sorted(ROLES))
    parser.add_argument("--risk", default="RISK_2", choices=sorted(VALID_RISKS))
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        dest="skills",
        help="Task-scoped skill id (repeatable). Never dumps the full catalog.",
    )
    parser.add_argument("--verification", default="")
    parser.add_argument("--expected-output", default="")
    parser.add_argument("--work-subdir", default=None)
    parser.add_argument("--user-instruction", action="append", default=[])
    parser.add_argument("--artifact", action="append", default=[], dest="artifacts")
    parser.add_argument("--include-manifest-skills", action="store_true")
    parser.add_argument("--require-project-instructions", action="store_true")
    parser.add_argument("--skip-project-instructions", action="store_true")
    parser.add_argument("--spec-json", type=Path, help="Load WorkerTaskSpec fields from JSON")
    parser.add_argument("--preferences-json", type=Path)
    parser.add_argument(
        "--format",
        choices=("json", "prompt"),
        default="json",
    )
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

        spec = _spec_from_mapping(data)
        payload = build_worker_context(
            spec,
            project_root=args.project.resolve(),
            preferences=prefs,
            skip_project_instructions=args.skip_project_instructions,
        )

        if args.command in {"build", "validate", "render"}:
            validate_for_spawn(
                payload,
                require_project_instructions=args.require_project_instructions,
            )

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
