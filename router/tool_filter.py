"""Tool output filtering module for Agentit (RTK-style format-aware noise reduction).

Filters large build logs, passing test output, and noisy listings using
format-aware adapters (unittest, pytest, jest, cargo, generic).
The generic adapter NEVER deletes lines containing error or warning signals.
"""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
from pathlib import Path
from typing import Any

ERROR_SIGNAL_PATTERN = re.compile(
    r"\b(error|err|warning|warn|traceback|exception|stacktrace|panic|panicked|failed|failure|assert|assertionerror|fatal|exit status|exit code|sigsegv|sigabrt)\b",
    re.IGNORECASE,
)


def _filter_pytest(lines: list[str]) -> list[str]:
    retained: list[str] = []
    in_failure = False
    for line in lines:
        if re.match(r"^=+\s*(FAILURES|ERRORS)\s*=+", line) or line.startswith("FAIL ") or line.startswith("ERROR "):
            in_failure = True
            retained.append(line)
        elif re.match(r"^=+\s*short test summary info\s*=+", line) or re.match(r"^=+\s*\d+ passed", line):
            in_failure = False
            retained.append(line)
        elif in_failure or ERROR_SIGNAL_PATTERN.search(line):
            retained.append(line)
    return retained


def _filter_unittest(lines: list[str]) -> list[str]:
    retained: list[str] = []
    in_failure = False
    for line in lines:
        if line.startswith("FAIL:") or line.startswith("ERROR:") or line.startswith("======================================================================"):
            in_failure = True
            retained.append(line)
        elif line.startswith("----------------------------------------------------------------------") or line.startswith("Ran ") or line.startswith("OK") or line.startswith("FAILED"):
            in_failure = False
            retained.append(line)
        elif in_failure or ERROR_SIGNAL_PATTERN.search(line):
            retained.append(line)
    return retained


def _filter_jest(lines: list[str]) -> list[str]:
    retained: list[str] = []
    for line in lines:
        if "FAIL " in line or "● " in line or "Test Suites:" in line or "Tests:" in line or ERROR_SIGNAL_PATTERN.search(line):
            retained.append(line)
    return retained


def _filter_cargo(lines: list[str]) -> list[str]:
    retained: list[str] = []
    for line in lines:
        if "error:" in line or "warning:" in line or "panicked at" in line or "test result:" in line or ERROR_SIGNAL_PATTERN.search(line):
            retained.append(line)
    return retained


def _filter_generic(lines: list[str], max_lines: int = 40) -> list[str]:
    retained: list[str] = []
    for i, line in enumerate(lines):
        if ERROR_SIGNAL_PATTERN.search(line) or i < 5 or i >= len(lines) - 5:
            retained.append(line)
    return retained


def filter_tool_output(
    output: str,
    artifact_dir: Path | None = None,
    adapter: str = "auto",
    max_lines: int = 40,
    content_type: str | None = None,
) -> dict[str, Any]:
    """Filter raw tool output using format-aware adapters without losing error evidence."""
    lines = output.splitlines()

    # Protected content types (commands, diff, sql, secrets) must NEVER use lossy filtering
    if content_type in {"commands", "diff", "sql", "secrets"}:
        return {
            "filtered": False,
            "content": output,
            "saved_tokens_approx": 0,
            "reason": f"Content type '{content_type}' is protected from lossy filtering",
        }

    if len(lines) <= max_lines:
        return {
            "filtered": False,
            "content": output,
            "saved_tokens_approx": 0,
        }

    if adapter == "auto":
        if "=== FAILURES ===" in output or "=== ERRORS ===" in output or "short test summary info" in output:
            adapter = "pytest"
        elif "FAIL:" in output or "ERROR:" in output or "----------------------------------------------------------------------" in output:
            adapter = "unittest"
        elif "FAIL " in output and ("Test Suites:" in output or "Jest" in output):
            adapter = "jest"
        elif "error[" in output or "panicked at" in output or "running " in output and "tests" in output:
            adapter = "cargo"
        else:
            adapter = "generic"

    if adapter == "pytest":
        retained = _filter_pytest(lines)
    elif adapter == "unittest":
        retained = _filter_unittest(lines)
    elif adapter == "jest":
        retained = _filter_jest(lines)
    elif adapter == "cargo":
        retained = _filter_cargo(lines)
    else:
        retained = _filter_generic(lines, max_lines=max_lines)

    log_path: Path | None = None
    sha256_hash = hashlib.sha256(output.encode("utf-8")).hexdigest()
    short_hash = sha256_hash[:16]

    if artifact_dir is not None:
        artifact_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(artifact_dir.parent, 0o700)
        os.chmod(artifact_dir, 0o700)
        log_path = artifact_dir / f"tool-output-{short_hash}.log"
        if not log_path.is_file():
            fd, temp_path_str = tempfile.mkstemp(prefix=".tool-tmp-", dir=artifact_dir, text=True)
            temp_path = Path(temp_path_str)
            try:
                os.fchmod(fd, 0o600)
                with os.fdopen(fd, "w", encoding="utf-8") as stream:
                    stream.write(output)
                    stream.flush()
                    os.fsync(fd)
                os.replace(temp_path, log_path)
                os.chmod(log_path, 0o600)
            finally:
                temp_path.unlink(missing_ok=True)

    filtered_content = "\n".join(retained)
    if log_path:
        filtered_content += f"\n\n[Full log saved: {log_path} | SHA-256: {sha256_hash}]"

    tokens_saved = max(0, (len(output) - len(filtered_content)) // 4)

    return {
        "filtered": True,
        "adapter_used": adapter,
        "content": filtered_content,
        "full_log_path": str(log_path) if log_path else None,
        "sha256": sha256_hash,
        "lines_total": len(lines),
        "lines_retained": len(retained),
        "saved_tokens_approx": tokens_saved,
    }
