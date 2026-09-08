#!/usr/bin/env python3
"""Verify or refresh pinned upstream skills without executing upstream code.

Default is an offline integrity check. --refresh plans a current-source refresh;
only --apply changes distributed files. Downloads and candidate state are private.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
LOCK = "skills/UPSTREAM_LOCK.json"
SOURCES = "skills/UPSTREAM_SOURCES.md"
ROOT_PACKAGES = {
    "humanizer": ["SKILL.md", "agents", "scripts"],
    "stop-slop": ["SKILL.md", "references"],
}


class SyncError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if not value or not path.parts or path.is_absolute() or ".." in path.parts or "\\" in value:
        raise SyncError(f"unsafe relative path: {value!r}")
    return path.as_posix()


def destination(root: Path, value: str) -> Path:
    path = root / relative_path(value)
    current = path
    while current != root:
        if current.is_symlink():
            raise SyncError(f"symlink in managed path: {current.relative_to(root)}")
        current = current.parent
    return path


def package_destination(item: dict) -> str:
    return relative_path(item.get("destination", f"skills/{item['skill']}"))


def file_record(data: bytes, mode: int) -> dict:
    return {"sha256": digest(data), "mode": mode}


def add_owned_files(target: dict, entries: dict) -> None:
    for raw, content in entries.items():
        path = relative_path(raw)
        if path in target:
            raise SyncError(f"overlapping file ownership: {path}")
        target[path] = content


def validate_layout(lock: dict) -> None:
    """Reject overlapping ownership before reading sources or planning writes."""
    paths = [package_destination(item) for item in lock["mappings"]]
    paths += [relative_path(item["destination"]) for item in lock.get("shared", [])]
    paths += [relative_path(item["destination"]) for item in lock.get("licenses", [])]
    paths += [LOCK, SOURCES]
    accepted = []
    for raw in paths:
        path = PurePosixPath(raw)
        if any(path == other or path in other.parents or other in path.parents for other in accepted):
            raise SyncError(f"overlapping managed destinations: {raw}")
        accepted.append(path)
    for item in lock.get("shared", []):
        path = PurePosixPath(relative_path(item["manifest"]))
        own_root = PurePosixPath(relative_path(item["destination"]))
        for other in accepted:
            if other == own_root and other in path.parents:
                continue
            if path == other or path in other.parents or other in path.parents:
                raise SyncError(f"overlapping shared manifest: {path}")
        accepted.append(path)


def installed_files(root: Path, package: str) -> dict[str, dict]:
    base = destination(root, package)
    if not base.is_dir():
        raise SyncError(f"missing package: {package}")
    result = {}
    for path in sorted(base.rglob("*")):
        if "__pycache__" in path.parts:
            continue
        if path.is_symlink():
            raise SyncError(f"symlink in package: {path.relative_to(root)}")
        if path.is_file():
            result[path.relative_to(base).as_posix()] = file_record(path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
    return result


def managed_files(lock: dict) -> dict[str, dict]:
    result = {}
    for item in [*lock["mappings"], *lock.get("shared", [])]:
        base = package_destination(item) if "skill" in item else relative_path(item["destination"])
        for path, record in item.get("files", {}).items():
            add_owned_files(result, {f"{base}/{relative_path(path)}": record})
    for item in lock.get("licenses", []):
        add_owned_files(result, {item["destination"]: {"sha256": item["sha256"], "mode": item["mode"]}})
    return result


def check_integrity(root: Path, lock: dict) -> dict:
    validate_layout(lock)
    if not all(item.get("files") for item in lock["mappings"]):
        raise SyncError("lock has no file integrity records; run a reviewed --refresh first")
    for item in lock["mappings"]:
        actual = installed_files(root, package_destination(item))
        if actual != item["files"]:
            changed = sorted(k for k in actual.keys() | item["files"].keys() if actual.get(k) != item["files"].get(k))
            raise SyncError(f"package integrity differs: {item['skill']}: {', '.join(changed[:8])}")
    files = managed_files(lock)
    for relative, record in files.items():
        path = destination(root, relative)
        if not path.is_file() or file_record(path.read_bytes(), stat.S_IMODE(path.stat().st_mode)) != record:
            raise SyncError(f"managed file integrity differs: {relative}")
    return {"status": "verified", "packages": len(lock["mappings"]), "files": len(files), "sources": len({item["repo"] for item in lock.get("licenses", [])})}


def archive_path(cache: Path, repo: str, snapshot: str, *, offline: bool) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise SyncError(f"invalid upstream repository: {repo!r}")
    if not re.fullmatch(r"[0-9a-f]{40}", snapshot):
        raise SyncError(f"upstream snapshot must be a full commit SHA: {repo}")
    target = cache / (repo.replace("/", "--") + "@" + snapshot + ".tar.gz")
    if target.is_symlink():
        raise SyncError("archive cache must not contain symlinks")
    if not target.is_file():
        if offline:
            raise SyncError(f"missing cached snapshot: {repo}@{snapshot}")
        cache.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(f"https://codeload.github.com/{repo}/tar.gz/{snapshot}", headers={"User-Agent": "Agentit-upstream-sync"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read(128 * 1024 * 1024 + 1)
        if len(data) > 128 * 1024 * 1024:
            raise SyncError(f"archive exceeds size limit: {repo}")
        atomic_write(target, data, 0o600)
    return target


def read_archive(path: Path) -> dict[str, tuple[bytes, int]]:
    files = {}
    total = 0
    with tarfile.open(path, "r:gz") as archive:
        members = archive.getmembers()
        if not members:
            raise SyncError("empty upstream archive")
        prefix = members[0].name.split("/", 1)[0] + "/"
        for member in members:
            if not member.name.startswith(prefix) or member.isdir():
                continue
            relative = relative_path(member.name[len(prefix):])
            if not member.isfile():
                # Never extract links/devices. Selected packages reject these
                # entries explicitly rather than following them outside a tree.
                files[relative] = (b"", -1)
                continue
            total += member.size
            if total > 256 * 1024 * 1024 or member.size > 32 * 1024 * 1024:
                raise SyncError("upstream archive exceeds unpacked size limit")
            if relative in files:
                raise SyncError(f"duplicate archive path: {relative}")
            stream = archive.extractfile(member)
            assert stream is not None
            files[relative] = (stream.read(), 0o755 if member.mode & 0o111 else 0o644)
    return files


def select_package(files: dict, item: dict) -> dict:
    source = item["path"].strip("/")
    result = {}
    for path, content in files.items():
        if source == ".":
            include = item.get("include", ROOT_PACKAGES.get(item["skill"], []))
            if not any(path == entry or path.startswith(entry + "/") for entry in include):
                continue
            relative = path
        elif path.startswith(source + "/"):
            relative = path[len(source) + 1:]
        else:
            continue
        if content[1] == -1:
            raise SyncError(f"non-regular upstream package entry: {path}")
        result[relative] = content
    if "SKILL.md" not in result:
        raise SyncError(f"upstream skill body missing: {item['skill']}")
    return result


def source_heads(lock: dict) -> dict[str, str]:
    result = {}
    for repo in sorted({item["repo"] for item in lock["mappings"]}):
        output = subprocess.check_output(["git", "ls-remote", f"https://github.com/{repo}.git", "HEAD"], text=True, timeout=30)
        result[repo] = output.split()[0]
    return result


def build_candidate(root: Path, lock: dict, heads: dict, cache: Path, *, offline: bool) -> tuple[dict, dict, dict]:
    validate_layout(lock)
    archives = {}

    def snapshot(repo, sha):
        key = repo, sha
        if key not in archives:
            archives[key] = read_archive(archive_path(cache, repo, sha, offline=offline))
        return archives[key]

    # Initial migration from the historical hash-free lock authenticates every
    # current package against its exact old upstream snapshot first.
    old = copy.deepcopy(lock)
    for item in old["mappings"]:
        if not item.get("files"):
            package = select_package(snapshot(item["repo"], item["snapshot"]), item)
            item["files"] = {path: file_record(*content) for path, content in package.items()}
    for item in old.get("shared", []):
        if not item.get("files"):
            files = snapshot(item["repo"], item["snapshot"])
            prefix = item["path"] + "/"
            item["files"] = {path[len(prefix):]: file_record(*content) for path, content in files.items() if path.startswith(prefix) and content[1] != -1}
    check_integrity(root, old)

    updated = copy.deepcopy(old)
    updated["generated_by"] = "scripts/sync_upstream_skills.py"
    updated["integrity_version"] = 1
    updated["licenses"] = []
    desired = {}
    for item in updated["mappings"]:
        item["snapshot"] = heads[item["repo"]]
        item.pop("replaces", None)
        # The upstream meta-workflow remains verbatim source material; Agentit's
        # own global adapter keeps the stable using-agent-skills public ID.
        if item["skill"] == "using-agent-skills":
            item["destination"] = "vendor/agent-skills/using-agent-skills"
        if item["path"] == ".":
            item["include"] = ROOT_PACKAGES[item["skill"]]
        item["kind"] = "canonical-vendored"
        package = select_package(snapshot(item["repo"], item["snapshot"]), item)
        item["files"] = {path: file_record(*content) for path, content in sorted(package.items())}
        base = package_destination(item)
        add_owned_files(desired, {f"{base}/{path}": content for path, content in package.items()})
    for item in updated.get("shared", []):
        item["snapshot"] = heads[item["repo"]]
        prefix = item["path"] + "/"
        shared = {path[len(prefix):]: content for path, content in snapshot(item["repo"], item["snapshot"]).items() if path.startswith(prefix)}
        if any(mode == -1 for _, mode in shared.values()):
            raise SyncError("non-regular upstream shared reference")
        item["files"] = {path: file_record(*content) for path, content in sorted(shared.items())}
        add_owned_files(desired, {f"{item['destination']}/{path}": content for path, content in shared.items()})
        add_owned_files(desired, {item["manifest"]: (("\n".join(sorted(shared)) + "\n").encode(), 0o644)})
    for repo, sha in sorted(heads.items()):
        files = snapshot(repo, sha)
        licenses = {path: content for path, content in files.items() if "/" not in path and path.lower().startswith(("license", "notice", "copying"))}
        if not licenses or any(mode == -1 for _, mode in licenses.values()):
            raise SyncError(f"upstream license missing or unsafe: {repo}")
        for source, content in sorted(licenses.items()):
            target = f"vendor/licenses/{repo.replace('/', '--')}/{source}"
            updated["licenses"].append({"repo": repo, "snapshot": sha, "source": source, "destination": target, **file_record(*content)})
            add_owned_files(desired, {target: content})
    validate_layout(updated)
    return old, updated, desired


def provenance_markdown(lock: dict) -> bytes:
    lines = ["# Skill provenance registry", "", "Canonical packages are copied byte-for-byte from pinned upstream commits. File hashes, modes, repository-root package selections and original license/NOTICE files are recorded in `UPSTREAM_LOCK.json`. Agentit authority and composition remain outside these packages.", "", "| Skill source | Distributed path | Upstream snapshot |", "| --- | --- | --- |"]
    for item in lock["mappings"]:
        link = f"https://github.com/{item['repo']}/tree/{item['snapshot']}/{item['path']}"
        lines.append(f"| `{item['skill']}` | `{package_destination(item)}` | [{item['repo']}@{item['snapshot'][:12]}]({link}) |")
    lines += ["", "`skills/using-agent-skills` is an Agentit-owned adapter; its raw upstream source is retained separately under `vendor/agent-skills`. Other packages absent from this registry are Agentit-owned or source-informed composites described in `THIRD_PARTY_NOTICES.md`.", "", "Verify offline with `python3 scripts/sync_upstream_skills.py`. Plan a refresh with `--refresh`; use `--refresh --apply` only after reviewing the source changes. No upstream scripts or dependency installers are executed.", ""]
    return "\n".join(lines).encode()


def atomic_write(path: Path, data: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".agentit-upstream-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def apply_candidate(root: Path, old: dict, updated: dict, desired: dict) -> dict:
    check_integrity(root, old)
    validate_layout(updated)
    previous = managed_files(old)
    normalized = {}
    add_owned_files(normalized, desired)
    desired = normalized
    add_owned_files(desired, {SOURCES: (provenance_markdown(updated), 0o644)})
    add_owned_files(desired, {LOCK: ((json.dumps(updated, indent=2) + "\n").encode(), 0o644)})
    special = {LOCK, SOURCES, *(item["manifest"] for item in old.get("shared", []))}
    changed = {}
    for relative in sorted(previous.keys() | desired.keys()):
        path = destination(root, relative)
        current = (path.read_bytes(), stat.S_IMODE(path.stat().st_mode)) if path.is_file() else None
        wanted = desired.get(relative)
        if current == wanted:
            continue
        if path.exists() and not path.is_file():
            raise SyncError(f"managed destination is not a file: {relative}")
        if current is not None and relative not in previous and relative not in special:
            raise SyncError(f"refusing to overwrite an unowned file: {relative}")
        changed[relative] = (current, wanted)
    applied = []
    try:
        # Keep the integrity lock last, so a partial external interruption is
        # detectable by the next offline check and recoverable through Git.
        for relative in sorted(changed, key=lambda path: (path == LOCK, path)):
            before, wanted = changed[relative]
            path = destination(root, relative)
            current = (path.read_bytes(), stat.S_IMODE(path.stat().st_mode)) if path.is_file() else None
            if current != before:
                raise SyncError(f"managed file changed during refresh: {relative}")
            applied.append(relative)
            if wanted is None:
                path.unlink()
            else:
                atomic_write(path, *wanted)
        verified = check_integrity(root, updated)
    except BaseException as error:
        conflicts = []
        for relative in reversed(applied):
            before, wanted = changed[relative]
            try:
                path = destination(root, relative)
                if path.exists() and not path.is_file():
                    raise SyncError("recovery destination is not a regular file")
                current = (path.read_bytes(), stat.S_IMODE(path.stat().st_mode)) if path.is_file() else None
            except (SyncError, OSError):
                conflicts.append(relative)
                continue
            if current == before:
                continue
            if current != wanted:
                conflicts.append(relative)
                continue
            if before is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, *before)
        if conflicts:
            raise SyncError("refresh recovery preserved modified paths: " + ", ".join(sorted(conflicts))) from error
        raise
    return {**verified, "status": "applied", "changed_files": len(changed)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Plan a current-source refresh; no distributed writes without --apply.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--cache-dir", type=Path, default=ROOT / ".agentit/upstream/archives")
    parser.add_argument("--heads-file", type=Path, help="Use a reviewed JSON repository-to-commit map instead of querying HEAD.")
    parser.add_argument("--offline", action="store_true", help="Require cached snapshots and --heads-file for a refresh.")
    args = parser.parse_args(argv)
    try:
        lock = json.loads((ROOT / LOCK).read_text())
        if not args.refresh:
            if args.apply or args.heads_file:
                raise SyncError("--apply and --heads-file require --refresh")
            result = check_integrity(ROOT, lock)
        else:
            if args.offline and not args.heads_file:
                raise SyncError("offline refresh requires --heads-file")
            raw = json.loads(args.heads_file.read_text()) if args.heads_file else source_heads(lock)
            heads = {repo: value["sha"] if isinstance(value, dict) else value for repo, value in raw.items()}
            expected = {item["repo"] for item in lock["mappings"]}
            if set(heads) != expected:
                raise SyncError("heads map must contain exactly the locked source repositories")
            old, updated, desired = build_candidate(ROOT, lock, heads, args.cache_dir, offline=args.offline)
            result = {"status": "plan", "packages": len(updated["mappings"]), "source_commits": heads, "candidate_files": len(desired)}
            if args.apply:
                result.update(apply_candidate(ROOT, old, updated, desired))
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (SyncError, OSError, ValueError, tarfile.TarError, subprocess.SubprocessError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
