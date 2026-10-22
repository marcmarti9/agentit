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
from urllib.parse import unquote, urlsplit

try:
    from .continuity import ContinuityError, _atomic_write_text, parse_state, state_path
except ImportError:  # Direct script invocation.
    from continuity import ContinuityError, _atomic_write_text, parse_state, state_path

CONFIG_RELATIVE = Path(".agentit/continuity-sync.json")
MAX_STATE_BYTES = 1024 * 1024
KEY_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


def _git(*argv: str, cwd: Path | None = None, raw: bool = False, input_data: bytes | None = None) -> str | bytes:
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
        env.pop(name, None)
    try:
        result = subprocess.run(
            ["git", "-c", f"core.hooksPath={os.devnull}", "-c", f"core.attributesFile={os.devnull}",
             "-c", "core.fsmonitor=false", *argv], cwd=cwd, capture_output=True, text=not raw,
            input=input_data, timeout=60, env=env, check=False,
        )
    except (OSError, UnicodeError, subprocess.TimeoutExpired) as exc:
        raise ContinuityError(f"Git transport failed: {type(exc).__name__}") from exc
    if result.returncode:
        # Git diagnostics sometimes echo credentials/remote URLs; do not expose them.
        raise ContinuityError(f"Git operation failed ({argv[0]}, exit {result.returncode}); check remote access and retry")
    return result.stdout if raw else result.stdout.strip()


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


def _remote_identity(remote: str, root: Path) -> tuple[str, str, str]:
    """Compare repositories, without making credentials acceptable for sync.

    Origin may contain credentials from the project's existing configuration;
    they are deliberately excluded from identity and never returned or logged.
    Only GitHub's repository path has a known case-insensitive contract.
    """
    if remote.startswith("/"):
        return ("local", "", str(Path(remote).resolve()))
    scp = re.fullmatch(r"(?:[^@/\s]+@)?([^:/\s]+):(.+)", remote) if "://" not in remote else None
    if scp:
        host, path = scp.groups()
        host = host.lower()
    else:
        try:
            parsed = urlsplit(remote)
            if parsed.scheme == "file":
                if parsed.netloc not in {"", "localhost"}:
                    raise ValueError("nonlocal file URL")
                return ("local", "", str(Path(unquote(parsed.path)).resolve()))
            if not parsed.scheme:
                return ("local", "", str((root / remote).resolve()))
            host, path = parsed.hostname, unquote(parsed.path)
            port = parsed.port
            if host and port and port != {"https": 443, "http": 80, "ssh": 22, "git": 9418}.get(parsed.scheme):
                host = f"{host}:{port}"
        except ValueError as exc:
            raise ContinuityError("Cannot identify Git remote repository") from exc
    if not host or not path:
        raise ContinuityError("Cannot identify Git remote repository")
    path = path.strip("/").removesuffix(".git")
    if host == "github.com":
        path = path.lower()
    return ("network", host.lower(), path)


def _origin(root: Path) -> str | None:
    try:
        # get-url applies Git's configured insteadOf expansion as transport does.
        return _git("-C", str(root), "remote", "get-url", "origin")
    except ContinuityError:
        return None


def _require_separate_remote(root: Path, remote: str) -> str:
    origin = _origin(root)
    # Resolve aliases without contacting the remote, using the same Git config
    # context as ls-remote/clone. Rewrites must not bypass remote validation.
    effective = _validate_remote(_git("ls-remote", "--get-url", "--", remote, cwd=root))
    if origin and _remote_identity(origin, root) == _remote_identity(effective, root):
        raise ContinuityError("Continuity remote must be separate from the project's Git origin; verify the separate remote is private")
    return effective


def _require_push_destination(root: Path, cloned: Path, expected_remote: str) -> None:
    """Inherited pushurl/pushInsteadOf must not export state elsewhere."""
    destinations = _git("-C", str(cloned), "remote", "get-url", "--push", "--all", "origin").splitlines()
    expected = _remote_identity(expected_remote, root)
    if not destinations:
        raise ContinuityError("No continuity push destination configured")
    for destination in destinations:
        if _remote_identity(_validate_remote(destination), root) != expected:
            raise ContinuityError("Continuity push destination differs from the verified separate remote; check Git pushurl and pushInsteadOf configuration")


def _key_for_project(project_root: Path) -> str:
    origin = _origin(project_root)
    if not origin:
        raise ContinuityError("No Git origin found; supply a portable project key when linking")
    try:
        kind, host, path = _remote_identity(origin, project_root)
    except ContinuityError as exc:
        raise ContinuityError("Cannot derive a portable project key; supply one explicitly") from exc
    if kind != "network":
        raise ContinuityError("Cannot derive a portable project key; supply one explicitly")
    canonical = f"{host}/{path}"
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


def _require_untracked_state(root: Path) -> None:
    """Never enable remote sync if normal project Git could publish local state."""
    try:
        inside = _git("-C", str(root), "rev-parse", "--is-inside-work-tree")
    except ContinuityError:
        return  # Non-Git projects can use a shared explicit project key.
    if inside != "true":
        return
    for relative in (".agentit/STATE.md", ".agentit/continuity-sync.json", ".agentit/conflicts/backup.md"):
        try:
            _git("-C", str(root), "check-ignore", "--", relative)
        except ContinuityError as exc:
            raise ContinuityError(
                "Private Agentit state is not ignored by project Git. Add .agentit/ to the project's .gitignore before linking or syncing."
            ) from exc


def link_remote(project_root: Path, remote: str, *, project_key: str | None = None) -> dict:
    """Explicit opt-in only. Caller must confirm remote is private before invoking."""
    root = Path(project_root).resolve()
    with _project_lock(root):
        _require_untracked_state(root)
        remote = _validate_remote(remote)
        _require_separate_remote(root, remote)
        key = project_key or _key_for_project(root)
        if not KEY_PATTERN.fullmatch(key):
            raise ContinuityError("Project key must be 1-64 letters, digits, underscores or hyphens")
        if _config_path(root).exists() or _config_path(root).is_symlink():
            raise ContinuityError("Continuity remote already linked; unlink explicitly before changing it")
        _git("ls-remote", "--", remote, cwd=root)
        config = {"schema_version": 1, "remote": remote, "project_key": key, "last_sha256": None}
        # Persist only after initial reconciliation succeeds. A failed link must
        # not leave configuration that silently enables future transport.
        result = _sync_locked(root, resolve=None, config=config)
        return {"status": "linked", "project_key": key, "sync": result}


def unlink_remote(project_root: Path) -> dict:
    root = Path(project_root).resolve()
    with _project_lock(root):
        path = _config_path(root)
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


def _remote_state(cloned: Path, key: str, scratch: Path) -> tuple[bool, bytes | None]:
    """Read only the state blob, never checking out executable Git attributes."""
    try:
        _git("-C", str(cloned), "rev-parse", "--verify", "HEAD")
    except ContinuityError:
        return False, None  # An empty remote has an unborn HEAD.
    relative = f"projects/{key}/STATE.md"
    for path in ("projects", f"projects/{key}", relative):
        entry = _git("-C", str(cloned), "ls-tree", "-z", "HEAD", "--", path)
        if not entry:
            return True, None
        mode, kind, oid = entry.partition("\t")[0].split()
        if (path != relative and (mode != "040000" or kind != "tree")) or (path == relative and (mode not in {"100644", "100755"} or kind != "blob")):
            raise ContinuityError("Unsafe symlink or object in continuity remote")
    if int(_git("-C", str(cloned), "cat-file", "-s", oid)) > MAX_STATE_BYTES:
        raise ContinuityError("Continuity state exceeds 1 MiB")
    body = _git("-C", str(cloned), "show", f"HEAD:{relative}", raw=True)
    scratch.write_bytes(body)
    return True, _read_state(scratch)


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


def _sync_locked(root: Path, *, resolve: str | None, config: dict | None = None) -> dict:
    new_link = config is not None
    config = config if new_link else _load_config(root)
    if config is None:
        return {"status": "disabled"}
    _require_untracked_state(root)
    effective_remote = _require_separate_remote(root, config["remote"])
    local_path = state_path(root)
    local = _read_state(local_path)
    backup = None
    with tempfile.TemporaryDirectory(prefix="agentit-continuity-") as tmp:
        cloned = Path(tmp) / "remote"
        _git("clone", "--quiet", "--no-checkout", "--depth", "1", "--", config["remote"], str(cloned), cwd=root)
        _require_push_destination(root, cloned, effective_remote)
        has_head, remote = _remote_state(cloned, config["project_key"], Path(tmp) / "STATE.md")
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
            # Seed the complete index, then replace only our blob without clean
            # filters. Other projects and remote files remain byte-for-byte intact.
            _git("-C", str(cloned), "read-tree", "HEAD" if has_head else "--empty")
            oid = _git("-C", str(cloned), "hash-object", "-w", "--no-filters", "--stdin", raw=True, input_data=local).decode("ascii").strip()
            _git("-C", str(cloned), "update-index", "--add", "--cacheinfo", "100644", oid, f"projects/{config['project_key']}/STATE.md")
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
            preview = _backup(root, "REMOTE", remote) if remote is not None else None
            detail = f"; remote snapshot: {preview}" if preview else "; remote state is missing"
            raise ContinuityError(f"Continuity conflict: both machines changed STATE.md{detail}; compare both versions, then run sync --resolve local|remote --apply")

    if new_link or config["last_sha256"] != final_sha:
        config["last_sha256"] = final_sha
        _save_config(root, config)
    result = {"status": status, "project_key": config["project_key"], "sha256": final_sha}
    if backup:
        result["backup"] = backup
    return result
