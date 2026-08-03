"""Artifact reference and CCR (Context Content Retention) module for Agentit.

Archives large text blocks (>150 lines or >10KB) into .agentit/artifacts/
with 0600 permissions, atomic mkstemp writing, and symlink protection.
"""

from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path
from typing import Any

PROTECTED_CONTENT_TYPES = {"commands", "diff", "sql", "secrets", "configs"}


def resolve_agentit_uri(uri: str, project_root: Path | None = None) -> Path:
    """Resolve an agentit://artifacts/ref-<hash>.txt URI to an absolute Path securely."""
    base_dir = Path(project_root) if project_root is not None else Path.cwd()
    prefix = "agentit://artifacts/"
    if not uri.startswith(prefix):
        raise ValueError(f"Invalid URI scheme: {uri}")

    rel_name = uri[len(prefix):]
    if ".." in rel_name or "/" in rel_name or "\\" in rel_name:
        raise ValueError(f"Path traversal detected in URI: {uri}")

    target_path = (base_dir / ".agentit" / "artifacts" / rel_name).resolve()
    expected_root = (base_dir / ".agentit" / "artifacts").resolve()
    if not str(target_path).startswith(str(expected_root)):
        raise ValueError(f"Resolved path outside artifacts directory: {target_path}")

    if target_path.is_symlink():
        raise PermissionError(f"Symlink rejected: {target_path}")

    return target_path


def create_artifact_reference(
    content: str,
    description: str,
    artifact_dir: Path,
    min_lines: int = 150,
    min_bytes: int = 10240,
    content_type: str | None = None,
) -> dict[str, Any]:
    """Archive content securely if it exceeds line/byte threshold or is a protected content type."""
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
    artifact_filename = f"ref-{short_hash}.txt"
    final_path = artifact_dir / artifact_filename

    if final_path.is_symlink():
        raise PermissionError(f"Symlink target rejected: {final_path}")

    if final_path.is_file():
        existing_hash = hashlib.sha256(final_path.read_bytes()).hexdigest()
        if existing_hash != sha256_hash:
            raise ValueError(f"Hash mismatch on existing artifact file: {final_path}")
    else:
        fd, temp_path_str = tempfile.mkstemp(prefix=".artifact-tmp-", dir=artifact_dir, text=True)
        temp_path = Path(temp_path_str)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(fd)
            os.replace(temp_path, final_path)
            os.chmod(final_path, 0o600)
        finally:
            temp_path.unlink(missing_ok=True)

    summary_head = lines[:5]
    summary_tail = lines[-5:]

    reference_payload = {
        "archived": True,
        "content_ref": f"agentit://artifacts/{artifact_filename}",
        "description": description,
        "content_type": content_type,
        "total_lines": len(lines),
        "total_bytes": len(content_bytes),
        "sha256": sha256_hash,
        "preview_head": summary_head,
        "preview_tail": summary_tail,
        "retrieval_path": str(final_path),
    }

    return reference_payload
