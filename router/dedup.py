"""Exact deduplication engine for Agentit turn context.

Tracks SHA-256 hashes of seen context blocks and replaces exact duplicate
blocks across conversation turns with a lightweight omission reference.
"""

from __future__ import annotations

import hashlib
from typing import Any


class ContextDeduplicator:
    """Tracks seen text blocks and replaces exact duplicates."""

    def __init__(self, min_block_length: int = 100) -> None:
        self.min_block_length = min_block_length
        self.seen_hashes: set[str] = set()

    def process_block(self, text: str) -> dict[str, Any]:
        """Process a text block, returning deduplicated output if already seen."""
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
        return {"duplicate": False, "sha256": sha256_hash, "content": text}
