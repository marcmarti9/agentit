"""Opt-in, private Git transport for Agentit's per-project continuity state.

Only STATE.md travels. Never git-add it to the project being worked on.
The separately configured remote MUST be private and access-controlled.
"""

from __future__ import annotations

import hashlib
import fcntl
from contextlib import contextmanager
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

try:
    from .continuity import ContinuityError, _atomic_write_text, parse_state, state_path
except ImportError:  # Direct script invocation.
    from continuity import ContinuityError, _atomic_write_text, parse_state, state_path

CONFIG_RELATIVE = Path(".agentit/continuity-sync.json")
MAX_STATE_BYTES = 1024 * 1024
KEY_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


def _git(*argv: str, cwd: Path | None = None) -> str:
    try:
        result = subprocess.run(
            ["git", *argv], cwd=cwd, capture_output=True, text=True,
            timeout=60, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ContinuityError(f"Git transport failed: {type(exc).__name__}") from exc
    if result.returncode:
        # Git diagnostics sometimes echo credentials/remote URLs; do not expose them.
        raise ContinuityError(f"Git operation failed ({argv[0]}, exit {result.returncode}); check remote access and retry")
    return result.stdout.strip()


def _validate_remote(remote: str) -> str:
    remote = remote.strip()
    if not remote or remote.startswith("-") or "\n" in remote or "\r" in remote:
        raise ContinuityError("Invalid continuity remote")
    if remote.startswith("/"):
        return remote  # Local bare Git remote; useful for self-hosted sync/tests.
    if re.fullmatch(r"[A-Za-z0-9_.-]+@[A-Za-z0-9_.-]+:[A-Za-z0-9_./-]+", remote):
        return remote  # SCP-style SSH, no embedded password.
    parsed = urlsplit(remote)
    if parsed.scheme not in {"https", "ssh", "file"} or not parsed.netloc and parsed.scheme != "file":
        raise ContinuityError("Remote must be an SSH/HTTPS Git URL or an absolute local path")
    if parsed.password or (parsed.scheme == "https" and parsed.username) or parsed.query or parsed.fragment:
        raise ContinuityError("Do not embed credentials or query parameters in a continuity remote")
    if parsed.scheme == "file" and (parsed.netloc not in {"", "localhost"} or not parsed.path.startswith("/")):
        raise ContinuityError("File remotes must be local absolute paths")
    return remote


def _key_for_project(project_root: Path) -> str:
    try:
        origin = _git("-C", str(project_root), "config", "--get", "remote.origin.url")
    except ContinuityError as exc:
        raise ContinuityError("No Git origin found; supply a portable project key when linking") from exc
    if re.match(r"^[^@/\s]+@[^:/\s]+:.+", origin):
        host, path = origin.split("@", 1)[1].split(":", 1)
    else:
        parsed = urlsplit(origin)
        host, path = parsed.hostname, parsed.path
    if not host or not path:
        raise ContinuityError("Cannot derive a portable project key; supply one explicitly")
    canonical = f"{host.lower()}/{path.strip('/').removesuffix('.git').lower()}"
    return "repo-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20]


def _config_path(project_root: Path) -> Path:
    return project_root / CONFIG_RELATIVE


def _load_config(project_root: Path) -> dict | None:
    path = _config_path(project_root)
    if path.parent.is_symlink():
        raise ContinuityError("Unsafe continuity sync directory")
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise ContinuityError("Unsafe continuity sync configuration path")
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ContinuityError("Invalid continuity sync configuration") from exc
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise ContinuityError("Unsupported continuity sync configuration")
    if not isinstance(config.get("remote"), str):
        raise ContinuityError("Invalid continuity remote configuration")
    config["remote"] = _validate_remote(config["remote"])
    if not isinstance(config.get("project_key"), str) or not KEY_PATTERN.fullmatch(config["project_key"]):
        raise ContinuityError("Invalid continuity project key")
    base = config.get("last_sha256")
    if base is not None and (not isinstance(base, str) or not re.fullmatch(r"[a-f0-9]{64}", base)):
        raise ContinuityError("Invalid continuity sync baseline")
    return config


def _save_config(project_root: Path, config: dict) -> None:
    _atomic_write_text(_config_path(project_root), json.dumps(config, indent=2, sort_keys=True) + "\n", private=True)


def link_remote(project_root: Path, remote: str, *, project_key: str | None = None) -> dict:
    """Explicit opt-in only. Caller must confirm remote is private before invoking."""
    root = Path(project_root).resolve()
    remote = _validate_remote(remote)
    key = project_key or _key_for_project(root)
    if not KEY_PATTERN.fullmatch(key):
        raise ContinuityError("Project key must be 1-64 letters, digits, underscores or hyphens")
    if _config_path(root).exists():
        raise ContinuityError("Continuity remote already linked; unlink explicitly before changing it")
    _git("ls-remote", "--", remote)
    config = {"schema_version": 1, "remote": remote, "project_key": key, "last_sha256": None}
    _save_config(root, config)
    return {"status": "linked", "project_key": key, "sync": sync_state(root)}


def unlink_remote(project_root: Path) -> dict:
    path = _config_path(Path(project_root).resolve())
    if path.is_symlink():
        raise ContinuityError("Unsafe continuity sync configuration path")
    if not path.exists():
        return {"status": "disabled"}
    path.unlink()  # Does not touch either local STATE.md or remote data.
    return {"status": "unlinked", "local_state_preserved": True, "remote_data_preserved": True}


def _read_state(path: Path) -> bytes | None:
    if path.is_symlink():
        raise ContinuityError("Refusing symlinked continuity state")
    if not path.exists():
        return None
    if not path.is_file() or path.stat().st_size > MAX_STATE_BYTES:
        raise ContinuityError("Continuity state is not a regular file or exceeds 1 MiB")
    try:
        if not parse_state(path)["complete"]:
            raise ContinuityError("Continuity state is missing required sections")
        return path.read_bytes()
    except (OSError, UnicodeError) as exc:
        raise ContinuityError("Cannot read continuity state") from exc


def _digest(data: bytes | None) -> str | None:
    return hashlib.sha256(data).hexdigest() if data is not None else None


@contextmanager
def _project_lock(root: Path):
    directory = root / ".agentit"
    if directory.is_symlink():
        raise ContinuityError("Unsafe symlinked .agentit directory")
    directory.mkdir(mode=0o700, exist_ok=True)
    lock_path = directory / "continuity-sync.lock"
    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(lock_path, flags, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
    except OSError as exc:
        raise ContinuityError("Cannot lock continuity sync state") from exc


def _backup(root: Path, label: str, body: bytes) -> str:
    filename = f"{label}-{_digest(body)[:16]}.md"
    path = root / ".agentit" / "conflicts" / filename
    if path.exists() or path.is_symlink():
        if _read_state(path) != body:
            raise ContinuityError("Conflicting continuity backup path")
    else:
        _atomic_write_text(path, body.decode("utf-8"), private=True)
    return str(path)


def sync_state(project_root: Path, *, resolve: str | None = None) -> dict:
    """Reconcile one STATE.md with its authorized private Git remote.

    Normal sync never overwrites divergent state. Explicit conflict resolution
    creates a private backup and uses only a fast-forward Git push.
    """
    root = Path(project_root).resolve()
    if resolve not in {None, "local", "remote"}:
        raise ContinuityError("Conflict resolution must be local or remote")
    if _load_config(root) is None:
        return {"status": "disabled"}
    with _project_lock(root):
        return _sync_locked(root, resolve=resolve)


def _sync_locked(root: Path, *, resolve: str | None) -> dict:
    config = _load_config(root)
    if config is None:
        return {"status": "disabled"}
    local_path = state_path(root)
    local = _read_state(local_path)
    backup = None
    with tempfile.TemporaryDirectory(prefix="agentit-continuity-") as tmp:
        cloned = Path(tmp) / "remote"
        _git("clone", "--quiet", "--depth", "1", "--", config["remote"], str(cloned))
        target = cloned / "projects" / config["project_key"] / "STATE.md"
        if any(path.is_symlink() for path in (target.parent.parent, target.parent, target)):
            raise ContinuityError("Unsafe symlink in continuity remote")
        remote = _read_state(target)
        local_sha, remote_sha, base_sha = _digest(local), _digest(remote), config["last_sha256"]

        if local_sha == remote_sha:
            status = "up-to-date"
            final_sha = local_sha
        elif local is None or (base_sha is not None and local_sha == base_sha):
            if remote is None:
                raise ContinuityError("Remote continuity state was removed; refusing silent deletion")
            if _read_state(local_path) != local:
                raise ContinuityError("Local STATE.md changed during sync; retry")
            _atomic_write_text(local_path, remote.decode("utf-8"), private=True)
            status, final_sha = "pulled", remote_sha
        elif (remote is None and base_sha is None) or (base_sha is not None and remote_sha == base_sha) or (resolve == "local" and local is not None):
            if local is None:
                raise ContinuityError("Local continuity state was removed; refusing silent deletion")
            if resolve == "local" and remote is not None and remote_sha != base_sha:
                backup = _backup(root, "REMOTE", remote)
            if _read_state(local_path) != local:
                raise ContinuityError("Local STATE.md changed during sync; retry")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(local)
            _git("-C", str(cloned), "add", "--", f"projects/{config['project_key']}/STATE.md")
            _git("-C", str(cloned), "-c", "user.name=Agentit Continuity", "-c", "user.email=agentit@localhost", "commit", "--quiet", "-m", f"Update Agentit continuity for {config['project_key']}")
            branch = _git("-C", str(cloned), "symbolic-ref", "--short", "HEAD")
            _git("-C", str(cloned), "push", "--quiet", "origin", f"HEAD:refs/heads/{branch}")
            status, final_sha = ("resolved-pushed" if backup else "pushed"), local_sha
        elif resolve == "remote" and remote is not None:
            if local is not None:
                backup = _backup(root, "LOCAL", local)
            if _read_state(local_path) != local:
                raise ContinuityError("Local STATE.md changed during sync; retry")
            _atomic_write_text(local_path, remote.decode("utf-8"), private=True)
            status, final_sha = "resolved-pulled", remote_sha
        else:
            raise ContinuityError("Continuity conflict: both machines changed STATE.md; compare both versions, then run sync --resolve local|remote --apply")

    if config["last_sha256"] != final_sha:
        config["last_sha256"] = final_sha
        _save_config(root, config)
    result = {"status": status, "project_key": config["project_key"], "sha256": final_sha}
    if backup:
        result["backup"] = backup
    return result
