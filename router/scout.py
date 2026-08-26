"""Private project-local Scout state for ecosystem candidates.

Scout is useful runtime functionality, but its mutable candidate/rejection queue is
working state, not public repository documentation. By default it lives under
`.agentit/scout/` in the target project and is written with private permissions.
"""

from __future__ import annotations

import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


class ScoutError(RuntimeError):
    """Raised when Scout state cannot be read or written safely."""


def _resolve_project_root(project_root: Path | str | None = None) -> Path:
    if project_root is not None:
        root = Path(project_root).expanduser().resolve()
    else:
        root_arg: str | None = None
        for index, arg in enumerate(sys.argv):
            if arg == "--project" and index + 1 < len(sys.argv):
                root_arg = sys.argv[index + 1]
                break
            if arg.startswith("--project="):
                root_arg = arg.split("=", 1)[1]
                break
        root = Path(root_arg).expanduser().resolve() if root_arg else Path.cwd().resolve()
    if not root.is_dir() or root.is_symlink():
        raise ScoutError(f"project root must be a regular directory: {root}")
    return root


def _state_paths(project_root: Path | str | None = None) -> tuple[Path, Path, Path]:
    root = _resolve_project_root(project_root)
    directory = root / ".agentit" / "scout"
    return directory, directory / "candidates.yaml", directory / "rejected.yaml"


def _slugify(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "-", slug)[:50]


def _load(path: Path, key: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        return {"version": 1, key: []}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ScoutError(f"invalid Scout state {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get(key, []), list):
        raise ScoutError(f"invalid Scout state shape in {path}")
    data.setdefault("version", 1)
    data.setdefault(key, [])
    return data


def _ensure_private_directory(directory: Path) -> None:
    agentit_dir = directory.parent
    agentit_dir.mkdir(parents=True, exist_ok=True)
    if agentit_dir.is_symlink() or not agentit_dir.is_dir():
        raise ScoutError(f"Scout state parent must be a regular directory: {agentit_dir}")
    os.chmod(agentit_dir, stat.S_IRWXU)
    directory.mkdir(parents=True, exist_ok=True)
    if directory.is_symlink() or not directory.is_dir():
        raise ScoutError(f"Scout state directory must be a regular directory: {directory}")
    os.chmod(directory, stat.S_IRWXU)


def _save(path: Path, data: dict[str, Any]) -> None:
    directory = path.parent
    _ensure_private_directory(directory)
    content = yaml.safe_dump(data, default_flow_style=False, sort_keys=False)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=directory, text=True)
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    finally:
        temporary_path.unlink(missing_ok=True)


def load_candidates(project_root: Path | str | None = None) -> dict[str, Any]:
    _, candidates_file, _ = _state_paths(project_root)
    return _load(candidates_file, "candidates")


def save_candidates(data: dict[str, Any], project_root: Path | str | None = None) -> None:
    _, candidates_file, _ = _state_paths(project_root)
    _save(candidates_file, data)


def load_rejected(project_root: Path | str | None = None) -> dict[str, Any]:
    _, _, rejected_file = _state_paths(project_root)
    return _load(rejected_file, "rejected")


def save_rejected(data: dict[str, Any], project_root: Path | str | None = None) -> None:
    _, _, rejected_file = _state_paths(project_root)
    _save(rejected_file, data)


def add_candidate(
    url_or_claim: str,
    cand_type: str = "evaluated_idea",
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    data = load_candidates(project_root)
    cand_id = _slugify(url_or_claim.split("/")[-1] if "/" in url_or_claim else url_or_claim)
    if not cand_id:
        cand_id = f"candidate-{len(data['candidates']) + 1}"
    candidate = {
        "id": cand_id,
        "source": url_or_claim,
        "claim": "Scouted ecosystem idea/tool",
        "type": cand_type,
        "status": "incubating",
        "decision": "pending_evaluation",
    }
    for existing in data["candidates"]:
        if existing.get("id") == cand_id or existing.get("source") == url_or_claim:
            return existing
    data["candidates"].append(candidate)
    save_candidates(data, project_root)
    return candidate


def reject_candidate(
    cand_id: str,
    reason: str,
    project_root: Path | str | None = None,
) -> bool:
    candidates_data = load_candidates(project_root)
    rejected_data = load_rejected(project_root)
    found = None
    remaining = []
    for item in candidates_data.get("candidates", []):
        if item.get("id") == cand_id:
            found = item
        else:
            remaining.append(item)
    if not found:
        return False
    candidates_data["candidates"] = remaining
    found["reason"] = reason
    found["decision"] = "rejected"
    rejected_data.setdefault("rejected", []).append(found)
    save_candidates(candidates_data, project_root)
    save_rejected(rejected_data, project_root)
    return True


def inspect_candidate(
    cand_id: str,
    project_root: Path | str | None = None,
) -> dict[str, Any] | None:
    for item in load_candidates(project_root).get("candidates", []):
        if item.get("id") == cand_id:
            return item
    for item in load_rejected(project_root).get("rejected", []):
        if item.get("id") == cand_id:
            return item
    return None
