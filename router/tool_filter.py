"""Tool output filtering module for Agentit (RTK-style noise reduction).

Filters large build logs, passing test output, and noisy directory listings
without losing failing stack traces, errors, or exact verification evidence.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any


def filter_tool_output(
    output: str,
    artifact_dir: Path | None = None,
    max_lines: int = 40,
) -> dict[str, Any]:
    """Filter raw tool output and save the full unedited output as an artifact reference."""
    lines = output.splitlines()
    if len(lines) <= max_lines:
        return {
            "filtered": False,
            "content": output,
            "saved_tokens_approx": 0,
        }

    sha256_hash = hashlib.sha256(output.encode("utf-8")).hexdigest()
    short_hash = sha256_hash[:12]

    # Detect test output pattern
    failing_blocks: list[str] = []
    summary_lines: list[str] = []
    in_failure_block = False
    current_block: list[str] = []

    for line in lines:
        if line.startswith("FAIL:") or line.startswith("ERROR:") or line.startswith("======================================================================"):
            if current_block:
                failing_blocks.append("\n".join(current_block))
                current_block = []
            in_failure_block = True
            current_block.append(line)
        elif line.startswith("----------------------------------------------------------------------") or line.startswith("Ran ") or line.startswith("OK") or line.startswith("FAILED"):
            if current_block:
                failing_blocks.append("\n".join(current_block))
                current_block = []
            in_failure_block = False
            summary_lines.append(line)
        elif in_failure_block:
            current_block.append(line)

    if current_block:
        failing_blocks.append("\n".join(current_block))

    log_path: Path | None = None
    if artifact_dir is not None:
        artifact_dir.mkdir(parents=True, exist_ok=True)
        log_path = artifact_dir / f"tool-output-{short_hash}.log"
        log_path.write_text(output, encoding="utf-8")

    filtered_lines: list[str] = []
    if failing_blocks:
        filtered_lines.append(f"[{len(failing_blocks)} failing test/error block(s) retained below]")
        filtered_lines.extend(failing_blocks)
    if summary_lines:
        filtered_lines.append("[Test Execution Summary]")
        filtered_lines.extend(summary_lines)

    if not filtered_lines:
        # Fallback to head + tail truncation if no structured test pattern was found
        head = lines[:15]
        tail = lines[-15:]
        filtered_lines = head + [f"\n... [{len(lines) - 30} lines suppressed; full output saved] ...\n"] + tail

    filtered_content = "\n".join(filtered_lines)
    if log_path:
        filtered_content += f"\n\n[Full log saved: {log_path} | SHA-256: {sha256_hash}]"

    tokens_saved = max(0, (len(output) - len(filtered_content)) // 4)

    return {
        "filtered": True,
        "content": filtered_content,
        "full_log_path": str(log_path) if log_path else None,
        "sha256": sha256_hash,
        "lines_total": len(lines),
        "lines_retained": len(filtered_lines),
        "saved_tokens_approx": tokens_saved,
    }
