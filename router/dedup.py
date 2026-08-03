"""Persistent exact deduplication engine for Agentit turn context.

Tracks SHA-256 hashes of seen context blocks per session in
.agentit/sessions/<session_id>/dedup.json with 0600 file permissions.
Replaces exact duplicate blocks across conversation turns.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


class ContextDeduplicator:
    """Tracks seen text blocks per session across CLI executions."""

    def __init__(
        self,
        session_id: str = "default",
        project_dir: Path | None = None,
        min_block_length: int = 100,
    ) -> None:
        self.session_id = session_id
        self.min_block_length = min_block_length
        base_dir = Path(project_dir) if project_dir is not None else Path.cwd()
        self.session_dir = base_dir / ".agentit" / "sessions" / session_id
        self.session_file = self.session_dir / "dedup.json"
        self.seen_hashes: set[str] = set()
        self._load_session_state()

    def _load_session_state(self) -> None:
        if not self.session_file.is_file() or self.session_file.is_symlink():
            return
        try:
            content = self.session_file.read_text(encoding="utf-8")
            data = json.loads(content)
            if isinstance(data, list):
                self.seen_hashes = set(data)
        except Exception:
            self.seen_hashes = set()

    def _save_session_state(self) -> None:
        self.session_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self.session_dir.parent, 0o700)
        os.chmod(self.session_dir, 0o700)

        hashes_list = sorted(self.seen_hashes)
        content = json.dumps(hashes_list, indent=2)

        fd, temp_path_str = tempfile.mkstemp(prefix=".dedup-tmp-", dir=self.session_dir, text=True)
        temp_path = Path(temp_path_str)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(fd)
            os.replace(temp_path, self.session_file)
            os.chmod(self.session_file, 0o600)
        finally:
            temp_path.unlink(missing_ok=True)

    def process_block(self, text: str) -> dict[str, Any]:
        """Process a text block, returning deduplicated output if already seen in session."""
        if len(text) < self.min_block_length:
            return {"duplicate": False, "content": text}

        sha256_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if sha256_hash in self.seen_hashes:
            return {
                "duplicate": True,
                "sha256": sha256_hash,
                "content": f"[Exact duplicate context omitted | SHA-256: {sha256_hash[:12]}...]",
            }

        self.seen_hashes.add(sha256_hash)
        self._save_session_state()
        return {"duplicate": False, "sha256": sha256_hash, "content": text}
