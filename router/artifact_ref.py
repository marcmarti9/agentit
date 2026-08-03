"""Artifact reference and CCR (Context Content Retention) module for Agentit.

Archives large text blocks (>200 lines or >10KB) into .agentit/artifacts/
and emits a lightweight recoverable reference payload.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


def create_artifact_reference(
    content: str,
    description: str,
    artifact_dir: Path,
    min_lines: int = 150,
) -> dict[str, Any]:
    """Archive content if it exceeds min_lines and return a reference payload."""
    lines = content.splitlines()
    if len(lines) < min_lines:
        return {
            "archived": False,
            "content": content,
        }

    artifact_dir.mkdir(parents=True, exist_ok=True)
    sha256_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    short_hash = sha256_hash[:12]
    artifact_file = artifact_dir / f"ref-{short_hash}.txt"
    artifact_file.write_text(content, encoding="utf-8")

    summary_head = lines[:5]
    summary_tail = lines[-5:]

    reference_payload = {
        "archived": True,
        "content_ref": f"agentit://artifacts/ref-{short_hash}.txt",
        "description": description,
        "total_lines": len(lines),
        "sha256": sha256_hash,
        "preview_head": summary_head,
        "preview_tail": summary_tail,
        "retrieval_path": str(artifact_file),
    }

    return reference_payload
