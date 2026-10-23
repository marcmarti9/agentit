"""Bounded, read-only artifact review and capacity gate before publication.

The operator declares task scopes and supplies remote observations. Agentit never
discovers remote hosts, executes ledger commands, deletes artifacts or installs
Git hooks. Receipts are private observations, not authenticated attestations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GIB = 1024 ** 3
RECEIPT = Path(".agentit/cleanup/review.json")
LEDGER = Path(".agentit/cleanup/ledger.json")
MAX_REVIEW_AGE = 24 * 3600
MAX_REMOTE_AGE = 3600
RETENTIONS = {"active", "private", "unique", "unsynced", "required", "other_owner"}


class CleanupError(ValueError):
    """Invalid, incomplete or unsafe review input."""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fresh(stamp: Any, max_age: int) -> bool:
    try:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(stamp)).total_seconds()
        return 0 <= age <= max_age
    except (TypeError, ValueError):
        return False


def _integer(value: Any) -> int:
    if type(value) is not int or value < 0:
        raise CleanupError("capacity values must be nonnegative integers")
    return value


def capacity_result(*, available_bytes: int, total_bytes: int,
                    planned_peak_bytes: int, reserve_bytes: int,
                    shared_production: bool = False) -> dict[str, Any]:
    available, total, peak, reserve = map(_integer, (
        available_bytes, total_bytes, planned_peak_bytes, reserve_bytes))
    if type(shared_production) is not bool or available > total or total == 0:
        raise CleanupError("invalid filesystem capacity observation")
    if shared_production:
        reserve = max(reserve, 100 * GIB, (total + 9) // 10)
    return {"allowed": available >= peak + reserve, "available_bytes": available,
            "total_bytes": total, "planned_peak_bytes": peak, "reserve_bytes": reserve,
            "required_bytes": peak + reserve, "shared_production": shared_production}


def local_capacity(path: Path, *, planned_peak_bytes: int, reserve_bytes: int,
                   shared_production: bool = False) -> dict[str, Any]:
    if not hasattr(os, "statvfs"):
        raise CleanupError("this host lacks statvfs; obtain capacity on a supported host")
    fs = os.statvfs(path)
    return capacity_result(available_bytes=fs.f_bavail * fs.f_frsize,
                           total_bytes=fs.f_blocks * fs.f_frsize,
                           planned_peak_bytes=planned_peak_bytes, reserve_bytes=reserve_bytes,
                           shared_production=shared_production)


def _git(project: Path, *args: str) -> str:
    result = subprocess.run(["git", "-c", "core.fsmonitor=false", *args], cwd=project,
                            capture_output=True, check=False, timeout=30)
    if result.returncode:
        raise CleanupError("Git project inspection failed")
    return os.fsdecode(result.stdout).rstrip("\r\n")


def _source(project: Path, retained: Any) -> dict[str, Any]:
    if Path(_git(project, "rev-parse", "--show-toplevel")).resolve() != project:
        raise CleanupError("--project must be the Git worktree root")
    if not isinstance(retained, list):
        raise CleanupError("retained_source_paths must be a list")
    prefixes = []
    for item in retained:
        if not isinstance(item, dict) or any(not isinstance(item.get(key), str) or not item[key].strip()
                                             for key in ("path", "owner", "reason")):
            raise CleanupError("retained source requires path, owner and reason")
        path = Path(item["path"])
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise CleanupError("retained source must be a bounded project-relative path")
        prefixes.append(path)
    changed = set(filter(None, _git(project, "diff", "--no-ext-diff", "--no-renames",
                                    "--name-only", "-z", "HEAD").split("\0")))
    changed.update(filter(None, _git(project, "ls-files", "--others", "--exclude-standard",
                                     "--directory", "--no-empty-directory", "-z").split("\0")))
    explained = {name for name in changed if any(Path(name) == prefix or prefix in Path(name).parents
                                                for prefix in prefixes)}
    # Bind the committed publication, allowing explicitly owned concurrent WIP.
    # Neither uncommitted changes nor retained artifacts are published by a push.
    return {"commit": _git(project, "rev-parse", "HEAD"),
            "tree": _git(project, "rev-parse", "HEAD^{tree}"),
            "unreviewed_changes": sorted(changed - explained),
            "retained_changes": sorted(explained)}


def _regular_path(path: Path) -> Path:
    path = Path(os.path.abspath(path))
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise CleanupError("symlink path rejected")
    return path


def _private(project: Path, path: Path) -> Path:
    result = _regular_path(path if path.is_absolute() else project / path)
    try:
        relative = result.relative_to(project / ".agentit")
    except ValueError as exc:
        raise CleanupError("review inputs and receipts must be inside private .agentit") from exc
    if not relative.parts:
        raise CleanupError("private artifact must be below .agentit")
    if _git(project, "ls-files", "--", ".agentit"):
        raise CleanupError("tracked .agentit state is not private")
    if not _git(project, "check-ignore", "--", str(result.relative_to(project))):
        raise CleanupError(".agentit must be Git-ignored before cleanup review")
    return result


def _read(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.stat().st_size > 4 * 1024 * 1024:
        raise CleanupError("missing or oversized review JSON")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CleanupError("review JSON must be an object")
    return data


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(project: Path, payload: dict[str, Any], destination: Path = RECEIPT) -> None:
    path = _private(project, destination)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path.parent, 0o700)
    fd, name = tempfile.mkstemp(prefix=".cleanup-", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def ledger_template(task_id: str) -> dict[str, Any]:
    return {"schema_version": 1, "task_id": task_id,
            "inventory_complete": False, "local_scopes": [], "remote_scopes": [],
            "retained_source_paths": [],
            "no_local_resources_reason": "", "no_remote_resources_reason": "",
            "capacity": [{"path": ".", "planned_peak_bytes": 0,
                          "reserve_bytes": GIB, "shared_production": False}]}


def _stat_entry(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise CleanupError("local inventory symlink rejected")
    info = path.stat()
    return {"device": info.st_dev, "inode": info.st_ino, "mode": info.st_mode,
            "size": info.st_size, "mtime_ns": info.st_mtime_ns}


def _local_snapshot(project: Path, scope: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(scope.get("path"), str) or not scope["path"].strip():
        raise CleanupError("local scope requires a path")
    raw = Path(scope["path"])
    root = _regular_path(raw if raw.is_absolute() else project / raw)
    if not root.is_dir():
        raise CleanupError("local inventory root must exist")
    # Bounded scope: one directory level. Operators classify retained subtrees as
    # units, or declare narrower scopes to inspect their children. Never follow
    # symlinks, walk sibling trees or calculate expensive recursive du totals.
    # The review receipt cannot be part of the snapshot it stores: writing it
    # changes its own metadata and its parent directory mtime.
    receipt = (project / RECEIPT).resolve()
    entries = {}
    for path in sorted(root.iterdir()):
        if path.is_symlink():
            raise CleanupError("local inventory symlink rejected")
        if path.resolve() == receipt:
            continue
        record = _stat_entry(path)
        if path.resolve() == receipt.parent and path.is_dir():
            record["mtime_ns"] = None
            nested = {}
            for child in sorted(path.iterdir()):
                if child.is_symlink():
                    raise CleanupError("local inventory symlink rejected")
                if child.resolve() == receipt:
                    continue
                nested[child.name] = _stat_entry(child)
            record["children_excluding_receipt"] = nested
        entries[path.name] = record
    return {"path": str(root), "entries": entries}


def _resources(resources: Any, reasons: list[str], counts: dict[str, int],
               present: set[str] | None = None) -> None:
    if not isinstance(resources, list):
        raise CleanupError("resources must be a list")
    names = set()
    for resource in resources:
        if not isinstance(resource, dict):
            raise CleanupError("resource must be an object")
        name = resource.get("name")
        if not isinstance(name, str) or not name or name in {".", ".."} or "/" in name or "\\" in name or name in names:
            raise CleanupError("resource names must be unique immediate children")
        names.add(name)
        disposition = resource.get("disposition")
        ownership = resource.get("ownership")
        if ownership not in {"task", "other", "unknown"}:
            raise CleanupError("invalid resource ownership")
        if not isinstance(resource.get("reason"), str) or not resource["reason"].strip():
            reasons.append("resource_reason_missing")
        if disposition == "removed":
            counts["removed_resources"] += 1
            if ownership != "task":
                reasons.append("unowned_removal")
            if present is not None and name in present:
                reasons.append("removed_resource_still_present")
        elif disposition == "retained":
            counts["retained_resources"] += 1
            if resource.get("retention") not in RETENTIONS:
                counts["unresolved_resources"] += 1
                reasons.append("unresolved_resource")
            if present is not None and name not in present:
                reasons.append("retained_resource_missing")
        elif disposition in {"cleanup_required", "unresolved"}:
            counts["unresolved_resources"] += 1
            reasons.append("unresolved_resource")
        else:
            raise CleanupError("invalid resource disposition")
    if present is not None and present - names:
        reasons.append("unlisted_local_resource")


def _observe(project: Path, ledger: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    counts = {"removed_resources": 0, "retained_resources": 0, "unresolved_resources": 0}
    if ledger.get("schema_version") != 1 or not isinstance(ledger.get("task_id"), str) or not ledger["task_id"].strip():
        raise CleanupError("ledger requires schema_version 1 and task_id")
    if ledger.get("inventory_complete") is not True:
        reasons.append("inventory_incomplete")
    observations: dict[str, Any] = {"local": [], "remote": [], "capacity": []}
    for kind in ("local", "remote"):
        scopes = ledger.get(f"{kind}_scopes")
        if not isinstance(scopes, list):
            raise CleanupError("ledger scopes must be explicit lists")
        no_resources_reason = ledger.get(f"no_{kind}_resources_reason")
        if not scopes and (not isinstance(no_resources_reason, str) or not no_resources_reason.strip()):
            reasons.append(f"{kind}_scope_not_reviewed")
        for scope in scopes:
            if not isinstance(scope, dict):
                raise CleanupError("scope must be an object")
            if kind == "local":
                try:
                    snapshot = _local_snapshot(project, scope)
                    observations[kind].append(snapshot)
                    _resources(scope.get("resources"), reasons, counts, set(snapshot["entries"]))
                except (OSError, CleanupError):
                    reasons.append("unsafe_local_scope")
            else:
                try:
                    evidence_path = _private(project, Path(scope["evidence"]))
                    evidence = _read(evidence_path)
                    if not isinstance(scope.get("id"), str) or not scope["id"].strip() or evidence.get("scope_id") != scope["id"]:
                        raise CleanupError("remote evidence scope mismatch")
                    if not _fresh(evidence.get("observed_at"), MAX_REMOTE_AGE):
                        reasons.append("remote_inventory_expired")
                    if evidence.get("inventory_complete") is not True:
                        reasons.append("remote_inventory_incomplete")
                    _resources(evidence.get("resources"), reasons, counts)
                    capacity = capacity_result(**evidence["capacity"])
                    if not capacity["allowed"]:
                        reasons.append("insufficient_capacity")
                    observations[kind].append({"scope_id": scope["id"],
                                               "evidence": str(evidence_path),
                                               "sha256": _hash(evidence_path),
                                               "capacity": capacity,
                                               "observation_kind": "operator_supplied"})
                except (OSError, KeyError, TypeError, CleanupError, json.JSONDecodeError):
                    reasons.append("remote_evidence_invalid")
    plans = ledger.get("capacity")
    if not isinstance(plans, list) or not plans:
        raise CleanupError("at least one local capacity plan is required")
    capacity_devices = set()
    for plan in plans:
        if not isinstance(plan, dict):
            raise CleanupError("capacity plan must be an object")
        raw = Path(plan["path"])
        path = _regular_path(raw if raw.is_absolute() else project / raw)
        capacity = local_capacity(path, planned_peak_bytes=plan["planned_peak_bytes"],
                                  reserve_bytes=plan["reserve_bytes"],
                                  shared_production=plan["shared_production"])
        device = path.stat().st_dev
        if device in capacity_devices:
            raise CleanupError("declare one combined peak and reserve per filesystem")
        capacity_devices.add(device)
        observations["capacity"].append({"path": str(path), **capacity})
        if not capacity["allowed"]:
            reasons.append("insufficient_capacity")
    if project.stat().st_dev not in capacity_devices:
        reasons.append("local_capacity_missing")
    for scope in observations["local"]:
        if Path(scope["path"]).stat().st_dev not in capacity_devices:
            reasons.append("local_capacity_missing")
    return {"blocking_reasons": sorted(set(reasons)), "counts": counts,
            "observations": observations}


def _summary(receipt: dict[str, Any], extra: list[str] | None = None) -> dict[str, Any]:
    reasons = sorted(set(receipt.get("blocking_reasons", []) + (extra or [])))
    counts = receipt.get("counts", {"removed_resources": 0, "retained_resources": 0,
                                    "unresolved_resources": 0})
    allowed = not reasons
    retained_sources = len(receipt.get("review", {}).get("retained_source_paths", []))
    status = "BLOCKED" if not allowed else ("REVIEWED_WITH_RETAINED" if counts["retained_resources"] or retained_sources else "REVIEWED")
    return {"allowed": allowed, "status": status, "blocking_reasons": reasons,
            "source_commit": receipt.get("source", {}).get("commit"),
            "retained_source_scopes": retained_sources, **counts}


def review(project: Path, ledger_path: Path) -> dict[str, Any]:
    project = _regular_path(project).resolve()
    path = _private(project, ledger_path)
    # Invalidate a previous pass before interpreting a replacement review.
    _write(project, {"schema_version": 1, "blocking_reasons": ["review_incomplete"]})
    ledger = _read(path)
    source = _source(project, ledger.get("retained_source_paths", []))
    result = _observe(project, ledger)
    if source["unreviewed_changes"]:
        result["blocking_reasons"].append("source_dirty")
    receipt = {"schema_version": 1, "project": str(project), "reviewed_at": now_iso(),
               "source": source, "ledger": str(path), "ledger_sha256": _hash(path),
               "review": ledger, **result}
    _write(project, receipt)
    return _summary(receipt)


def check(project: Path) -> dict[str, Any]:
    project = _regular_path(project).resolve()
    path = _private(project, RECEIPT)
    if not path.exists():
        return _summary({}, ["review_missing"])
    try:
        receipt = _read(path)
        if receipt.get("schema_version") != 1 or receipt.get("project") != str(project):
            raise CleanupError("invalid receipt identity")
        reasons = []
        if not _fresh(receipt.get("reviewed_at"), MAX_REVIEW_AGE):
            reasons.append("review_expired")
        ledger_path = _private(project, Path(receipt["ledger"]))
        ledger = _read(ledger_path)
        source = _source(project, ledger.get("retained_source_paths", []))
        if source["unreviewed_changes"]:
            reasons.append("source_dirty")
        if any(source[key] != receipt["source"][key] for key in ("commit", "tree")):
            reasons.append("source_changed")
        if _hash(ledger_path) != receipt["ledger_sha256"]:
            reasons.append("ledger_changed")
        current = _observe(project, ledger)
        reasons.extend(current["blocking_reasons"])
        if current["observations"]["local"] != receipt["observations"]["local"]:
            reasons.append("local_inventory_changed")
        if current["observations"]["remote"] != receipt["observations"]["remote"]:
            reasons.append("remote_inventory_changed")
        return _summary(receipt, reasons)
    except (OSError, ValueError, KeyError, TypeError):
        return _summary({}, ["review_invalid"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agentit cleanup", description=__doc__)
    parser.add_argument("command", choices=("init", "review", "check", "capacity"))
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--task-id", default="")
    parser.add_argument("--path", type=Path, default=Path.cwd())
    parser.add_argument("--planned-peak-bytes", type=int, default=0)
    parser.add_argument("--reserve-bytes", type=int, default=GIB)
    parser.add_argument("--shared-production", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "capacity":
            payload = local_capacity(args.path, planned_peak_bytes=args.planned_peak_bytes,
                                     reserve_bytes=args.reserve_bytes,
                                     shared_production=args.shared_production)
        elif args.command == "init":
            project = _regular_path(args.project).resolve()
            if not args.task_id.strip():
                raise CleanupError("init requires --task-id")
            if _private(project, args.ledger).exists():
                raise CleanupError("ledger already exists; preserve and update it explicitly")
            _write(project, ledger_template(args.task_id), args.ledger)
            payload = {"allowed": False, "status": "INVENTORY_REQUIRED"}
        elif args.command == "review":
            payload = review(args.project, args.ledger)
        else:
            payload = check(args.project)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        # Private inventory paths, remote identifiers and retention notes never
        # enter stdout, verification output tails, PR bodies or CI summaries.
        payload = {"allowed": False, "status": "BLOCKED", "error": type(exc).__name__}
        if isinstance(exc, CleanupError):
            payload["message"] = str(exc)
        print(json.dumps(payload))
        return 2
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["allowed"] or args.command == "init" else 1


if __name__ == "__main__":
    raise SystemExit(main())
