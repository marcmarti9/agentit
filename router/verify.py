"""Signal-gated verification gauntlet for Agentit.

Plan-first by default: select probes from probes/catalog.yaml based on project
signals and optional task text. Execute only when apply=True. Persist a receipt
under .agentit/verify/ for session close-out.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = REPO_ROOT / "probes" / "catalog.yaml"


class VerifyError(RuntimeError):
    """Invalid catalog, project, or probe execution."""


def _load_catalog(path: Path | None = None) -> dict[str, Any]:
    catalog_path = path or DEFAULT_CATALOG
    if yaml is None:
        raise VerifyError("PyYAML is required to load probes/catalog.yaml")
    if not catalog_path.is_file() or catalog_path.is_symlink():
        raise VerifyError(f"probe catalog missing or symlink: {catalog_path}")
    data = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("probes"), list):
        raise VerifyError("probe catalog must define a probes list")
    return data


def detect_signals(project_root: Path, task_text: str = "") -> list[str]:
    """Detect cheap filesystem + task signals for probe selection."""
    root = Path(project_root)
    signals: set[str] = {"any"}
    text = task_text.lower()

    def has(*names: str) -> bool:
        return any((root / name).exists() for name in names)

    if (root / ".git").exists():
        signals.add("git")
    if has("pubspec.yaml"):
        signals.update({"dart", "flutter"})
    if has("package.json"):
        signals.add("node")
    if has("tsconfig.json"):
        signals.add("typescript")
    if has("pyproject.toml", "setup.cfg", "pytest.ini", "requirements.txt"):
        signals.add("python")
    if has("Cargo.toml"):
        signals.add("rust")
    if has("go.mod"):
        signals.add("go")
    if has("supabase", "supabase/config.toml") or _tree_mentions(
        root, ("supabase", "postgres", "postgresql")
    ):
        signals.update({"supabase", "postgres", "postgresql"})
    if _matches(
        text,
        (
            r"\b(postgres|postgresql|psql|supabase|rls)\b",
            r"\b(auth|login|session|jwt|oauth)\b",
            r"\b(api|http|endpoint|fastapi|express|flask|django)\b",
            r"\b(frontend|ui|css|react|browser|landing)\b",
        ),
    ):
        if re.search(r"\b(postgres|postgresql|psql|supabase|rls)\b", text):
            signals.update({"postgres", "postgresql", "supabase", "psql"})
        if re.search(r"\b(auth|login|session|jwt|oauth)\b", text):
            signals.update({"auth", "login", "session", "jwt", "oauth"})
        if re.search(r"\b(api|http|endpoint|fastapi|express|flask|django)\b", text):
            signals.update({"api", "http", "endpoint", "fastapi", "express", "flask", "django"})
        if re.search(r"\b(frontend|ui|css|react|browser|landing)\b", text):
            signals.update({"frontend", "ui", "css", "react", "browser", "landing"})
    return sorted(signals)


def _tree_mentions(root: Path, needles: tuple[str, ...], *, max_files: int = 80) -> bool:
    count = 0
    for path in root.rglob("*"):
        if count >= max_files:
            break
        if not path.is_file() or path.is_symlink():
            continue
        if any(part in {".git", "node_modules", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".ts", ".tsx", ".js", ".py", ".dart", ".sql", ".toml", ".yaml", ".yml", ".json"}:
            continue
        count += 1
        try:
            sample = path.read_text(encoding="utf-8", errors="ignore")[:4000].lower()
        except OSError:
            continue
        if any(needle in sample for needle in needles):
            return True
    return False


def _matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def select_probes(
    catalog: dict[str, Any],
    signals: list[str],
    *,
    include_advisory: bool = True,
) -> list[dict[str, Any]]:
    signal_set = set(signals)
    selected: list[dict[str, Any]] = []
    for probe in catalog.get("probes", []):
        if not isinstance(probe, dict) or not probe.get("id"):
            continue
        needed = probe.get("signals_any") or ["any"]
        if not any(signal in signal_set for signal in needed):
            continue
        severity = str(probe.get("severity", "blocking"))
        if severity == "advisory" and not include_advisory:
            continue
        selected.append(probe)
    return selected


def _detector_matches(project_root: Path, when: list[str]) -> bool:
    for name in when:
        path = project_root / name
        if path.exists():
            return True
        # directory name match
        if name in {"tests"} and (project_root / "tests").is_dir():
            return True
    return False


def resolve_detect_command(probe: dict[str, Any], project_root: Path) -> list[str] | None:
    for detector in probe.get("detectors") or []:
        if not isinstance(detector, dict):
            continue
        when = detector.get("when") or []
        if not isinstance(when, list) or not _detector_matches(project_root, [str(x) for x in when]):
            continue
        command = detector.get("command")
        if isinstance(command, list) and command:
            # Skip if primary binary missing
            binary = str(command[0])
            if binary in {"python3", "npm", "npx", "cargo", "go", "flutter", "dart"}:
                if shutil.which(binary) is None and binary != "python3":
                    # python3 might be sys.executable later
                    if binary != "python3":
                        continue
            return [str(part) for part in command]
    return None


def plan_verification(
    project_root: Path,
    *,
    task_text: str = "",
    catalog_path: Path | None = None,
    include_advisory: bool = True,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    if not root.is_dir() or root.is_symlink():
        raise VerifyError(f"project root must be a regular directory: {root}")
    catalog = _load_catalog(catalog_path)
    signals = detect_signals(root, task_text)
    probes = select_probes(catalog, signals, include_advisory=include_advisory)
    planned: list[dict[str, Any]] = []
    for probe in probes:
        entry: dict[str, Any] = {
            "id": probe.get("id"),
            "name": probe.get("name"),
            "severity": probe.get("severity", "blocking"),
            "kind": probe.get("kind"),
            "description": probe.get("description"),
            "evidence": probe.get("evidence"),
            "status": "planned",
        }
        kind = probe.get("kind")
        if kind == "script":
            script = REPO_ROOT / str(probe.get("script", ""))
            entry["command"] = ["python3", str(script), str(root)]
            entry["runnable"] = script.is_file()
        elif kind == "detect_command":
            command = resolve_detect_command(probe, root)
            entry["command"] = command
            entry["runnable"] = command is not None
            if command is None:
                entry["status"] = "skipped_no_detector"
        elif kind == "checklist":
            entry["checks"] = probe.get("checks") or []
            entry["runnable"] = False
            entry["status"] = "manual_checklist"
        else:
            entry["runnable"] = False
            entry["status"] = "unknown_kind"
        planned.append(entry)
    return {
        "schema_version": 1,
        "mode": "plan",
        "project_root": str(root),
        "task_text": task_text,
        "signals": signals,
        "anti_greenwash": catalog.get("anti_greenwash") or [],
        "probes": planned,
        "blocking_ids": [
            p["id"] for p in planned if p.get("severity") == "blocking" and p.get("status") != "skipped_no_detector"
        ],
        "runnable_ids": [p["id"] for p in planned if p.get("runnable")],
        "checklist_ids": [p["id"] for p in planned if p.get("kind") == "checklist"],
    }


def _run_command(command: list[str], *, cwd: Path, timeout: int = 300) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
        output = (completed.stdout or "") + (completed.stderr or "")
        return {
            "exit_code": completed.returncode,
            "output": output[-20000:],
            "ok": completed.returncode == 0,
        }
    except subprocess.TimeoutExpired as exc:
        return {"exit_code": 124, "output": f"timeout: {exc}", "ok": False}
    except OSError as exc:
        return {"exit_code": 127, "output": str(exc), "ok": False}


def apply_verification(
    project_root: Path,
    *,
    task_text: str = "",
    catalog_path: Path | None = None,
    include_advisory: bool = True,
    run_project_commands: bool = True,
) -> dict[str, Any]:
    plan = plan_verification(
        project_root,
        task_text=task_text,
        catalog_path=catalog_path,
        include_advisory=include_advisory,
    )
    root = Path(plan["project_root"])
    results: list[dict[str, Any]] = []
    blocking_failed = False

    for probe in plan["probes"]:
        item = dict(probe)
        severity = item.get("severity", "blocking")
        if item.get("kind") == "checklist":
            item["status"] = "pending_agent_evidence"
            item["ok"] = None
            results.append(item)
            continue
        if item.get("status") == "skipped_no_detector":
            item["ok"] = True
            results.append(item)
            continue
        if not item.get("runnable"):
            item["status"] = "not_runnable"
            item["ok"] = severity != "blocking"
            if severity == "blocking":
                blocking_failed = True
            results.append(item)
            continue
        command = item.get("command") or []
        if not run_project_commands and item.get("kind") == "detect_command":
            item["status"] = "skipped_project_command"
            item["ok"] = True
            results.append(item)
            continue
        run = _run_command([str(c) for c in command], cwd=root)
        item["status"] = "passed" if run["ok"] else "failed"
        item["ok"] = run["ok"]
        item["exit_code"] = run["exit_code"]
        item["output_tail"] = run["output"][-4000:]
        if not run["ok"] and severity == "blocking":
            blocking_failed = True
        results.append(item)

    receipt = {
        **plan,
        "mode": "apply",
        "probes": results,
        "blocking_failed": blocking_failed,
        "passed": not blocking_failed,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "pending_checklists": [
            p["id"] for p in results if p.get("status") == "pending_agent_evidence"
        ],
    }
    path = _write_receipt(root, receipt)
    receipt["receipt_path"] = str(path)
    return receipt


def _write_receipt(project_root: Path, receipt: dict[str, Any]) -> Path:
    verify_dir = project_root / ".agentit" / "verify"
    verify_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(verify_dir, stat.S_IRWXU)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = verify_dir / f"{stamp}-receipt.json"
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.tmp-", dir=verify_dir, text=True
    )
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(receipt, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary_path, destination)
        os.chmod(destination, stat.S_IRUSR | stat.S_IWUSR)
    finally:
        temporary_path.unlink(missing_ok=True)
    return destination


def format_plan(plan: dict[str, Any]) -> str:
    lines = [
        f"mode: {plan.get('mode')}",
        f"project: {plan.get('project_root')}",
        f"signals: {', '.join(plan.get('signals') or [])}",
        f"blocking: {', '.join(plan.get('blocking_ids') or []) or '(none)'}",
        f"runnable: {', '.join(plan.get('runnable_ids') or []) or '(none)'}",
        f"checklists: {', '.join(plan.get('checklist_ids') or []) or '(none)'}",
        "probes:",
    ]
    for probe in plan.get("probes") or []:
        cmd = " ".join(probe.get("command") or []) if probe.get("command") else probe.get("kind")
        lines.append(
            f"  - [{probe.get('severity')}] {probe.get('id')}: {probe.get('status')} :: {cmd}"
        )
    if plan.get("anti_greenwash"):
        lines.append("anti_greenwash:")
        for rule in plan["anti_greenwash"][:6]:
            lines.append(f"  - {rule}")
    if plan.get("receipt_path"):
        lines.append(f"receipt: {plan['receipt_path']}")
    if "passed" in plan:
        lines.append(f"passed: {plan.get('passed')} (blocking_failed={plan.get('blocking_failed')})")
        if plan.get("pending_checklists"):
            lines.append(
                "pending_checklists: " + ", ".join(plan["pending_checklists"])
            )
    return "\n".join(lines)
