"""Artifact reference and CCR (Context Content Retention) module for Agentit.

Archives large text blocks (>150 lines or >10KB) into .agentit/artifacts/
with sidecar metadata JSON files, SHA-256 sidecar integrity verification, 
0600 permissions, atomic mkstemp writing, and full symlink component protection.

Note: SHA-256 sidecar verification provides tamper/corruption detection against
accidental edits. For cryptographic non-repudiation against arbitrary local writers,
use project-level permissions or signed manifests.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

PROTECTED_CONTENT_TYPES = {"commands", "diff", "sql", "secrets", "configs"}


def reject_symlink_components(path: Path, stop: Path) -> None:
    """Walk up parent directory components from path to stop, rejecting any symlinks."""
    current = path
    stop_resolved = stop.resolve()
    while True:
        if current.is_symlink():
            raise PermissionError(f"Symlink component rejected: {current}")
        if current.resolve() == stop_resolved or current == current.parent:
            break
        current = current.parent


def verify_artifact_integrity(artifact_file: Path, expected_hash_check: str | None = None) -> dict[str, Any]:
    """Verify that the artifact file content matches its sidecar metadata SHA-256."""
    sidecar_file = artifact_file.with_suffix(".json")
    actual_hash = hashlib.sha256(artifact_file.read_bytes()).hexdigest()

    # Automatic recovery for orphan .txt files missing a sidecar .json
    if not sidecar_file.is_file() and artifact_file.is_file():
        if expected_hash_check is not None and actual_hash != expected_hash_check:
            raise ValueError(f"Orphan artifact content mismatch for {artifact_file.name}")

        metadata = {
            "sha256": actual_hash,
            "content_type": "recovered_text",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "description": "Recovered sidecar for orphan artifact",
            "total_lines": len(artifact_file.read_text(encoding="utf-8").splitlines()),
            "total_bytes": artifact_file.stat().st_size,
        }
        meta_content = json.dumps(metadata, indent=2)

        fd_m, temp_meta_str = tempfile.mkstemp(prefix=".meta-tmp-", dir=artifact_file.parent, text=True)
        temp_meta = Path(temp_meta_str)
        try:
            os.fchmod(fd_m, 0o600)
            with os.fdopen(fd_m, "w", encoding="utf-8") as stream:
                stream.write(meta_content)
                stream.flush()
                os.fsync(fd_m)
            os.replace(temp_meta, sidecar_file)
            os.chmod(sidecar_file, 0o600)
        finally:
            temp_meta.unlink(missing_ok=True)

        return metadata

    if sidecar_file.is_symlink():
        raise PermissionError(f"Symlink sidecar rejected: {sidecar_file}")

    metadata = json.loads(sidecar_file.read_text(encoding="utf-8"))
    expected_hash = metadata.get("sha256")

    if actual_hash != expected_hash:
        raise ValueError(f"Artifact integrity failure for {artifact_file.name}: expected {expected_hash}, got {actual_hash}")

    return metadata


def resolve_agentit_uri(uri: str, project_root: Path | None = None) -> Path:
    """Resolve an agentit://artifacts/ref-<hash>.txt URI to an absolute Path securely."""
    base_dir = Path(project_root) if project_root is not None else Path.cwd()
    expected_root = (base_dir / ".agentit" / "artifacts").absolute()
    prefix = "agentit://artifacts/"

    if not uri.startswith(prefix):
        raise ValueError(f"Invalid URI scheme: {uri}")

    rel_name = uri[len(prefix):]
    if ".." in rel_name or "/" in rel_name or "\\" in rel_name:
        raise ValueError(f"Path traversal detected in URI: {uri}")

    raw_target_path = expected_root / rel_name
    reject_symlink_components(raw_target_path, stop=base_dir)

    target_path = raw_target_path.resolve()
    resolved_root = expected_root.resolve()

    try:
        if not target_path.is_relative_to(resolved_root):
            raise ValueError(f"Resolved path outside artifacts directory: {target_path}")
    except ValueError:
        raise ValueError(f"Resolved path outside artifacts directory: {target_path}")

    if not target_path.is_file() or target_path.is_symlink():
        raise FileNotFoundError(f"Artifact file missing or invalid: {target_path}")

    verify_artifact_integrity(target_path)
    return target_path


def create_artifact_reference(
    content: str,
    description: str,
    artifact_dir: Path,
    min_lines: int = 150,
    min_bytes: int = 10240,
    content_type: str | None = None,
) -> dict[str, Any]:
    """Archive content securely with sidecar metadata if threshold met or protected content type."""
    content_bytes = content.encode("utf-8")
    lines = content.splitlines()
    is_protected = content_type in PROTECTED_CONTENT_TYPES

    if not is_protected and len(lines) < min_lines and len(content_bytes) < min_bytes:
        return {
            "archived": False,
            "content": content,
        }

    artifact_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(artifact_dir.parent, 0o700)
    os.chmod(artifact_dir, 0o700)

    sha256_hash = hashlib.sha256(content_bytes).hexdigest()
    short_hash = sha256_hash[:16]
    base_name = f"ref-{short_hash}"
    artifact_file = artifact_dir / f"{base_name}.txt"
    sidecar_file = artifact_dir / f"{base_name}.json"

    reject_symlink_components(artifact_file, stop=artifact_dir.parent.parent)

    if artifact_file.is_file():
        verify_artifact_integrity(artifact_file, expected_hash_check=sha256_hash)
    else:
        # Write .txt file atomically
        fd, temp_path_str = tempfile.mkstemp(prefix=".artifact-tmp-", dir=artifact_dir, text=True)
        temp_path = Path(temp_path_str)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(fd)
            os.replace(temp_path, artifact_file)
            os.chmod(artifact_file, 0o600)
        finally:
            temp_path.unlink(missing_ok=True)

        # Write sidecar .json metadata file atomically
        metadata = {
            "sha256": sha256_hash,
            "content_type": content_type or "text",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "description": description,
            "total_lines": len(lines),
            "total_bytes": len(content_bytes),
        }
        meta_content = json.dumps(metadata, indent=2)

        fd_m, temp_meta_str = tempfile.mkstemp(prefix=".meta-tmp-", dir=artifact_dir, text=True)
        temp_meta = Path(temp_meta_str)
        try:
            os.fchmod(fd_m, 0o600)
            with os.fdopen(fd_m, "w", encoding="utf-8") as stream:
                stream.write(meta_content)
                stream.flush()
                os.fsync(fd_m)
            os.replace(temp_meta, sidecar_file)
            os.chmod(sidecar_file, 0o600)
        finally:
            temp_meta.unlink(missing_ok=True)

    summary_head = lines[:5]
    summary_tail = lines[-5:]

    reference_payload = {
        "archived": True,
        "content_ref": f"agentit://artifacts/{base_name}.txt",
        "description": description,
        "content_type": content_type,
        "total_lines": len(lines),
        "total_bytes": len(content_bytes),
        "sha256": sha256_hash,
        "preview_head": summary_head,
        "preview_tail": summary_tail,
        "retrieval_path": str(artifact_file),
        "sidecar_path": str(sidecar_file),
    }

    return reference_payload
