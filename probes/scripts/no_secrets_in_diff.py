#!/usr/bin/env python3
"""Fail if git diff looks like it introduces secrets."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)secret\s*[:=]\s*['\"][^'\"]{8,}"),
    re.compile(r"(?i)password\s*[:=]\s*['\"][^'\"]{6,}"),
    re.compile(r"(?i)BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY"),
    re.compile(r"(?i)aws_secret_access_key"),
    re.compile(r"(?i)xox[baprs]-[0-9A-Za-z-]{10,}"),
    re.compile(r"(?i)sk-[A-Za-z0-9]{20,}"),
]


def _git_diff(project: Path) -> str:
    chunks: list[str] = []
    for args in (
        ["git", "diff", "--"],
        ["git", "diff", "--cached", "--"],
    ):
        try:
            completed = subprocess.run(
                args,
                cwd=project,
                text=True,
                capture_output=True,
                check=False,
                timeout=30,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if completed.returncode == 0 and completed.stdout:
            chunks.append(completed.stdout)
    return "\n".join(chunks)


def main() -> int:
    project = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    if not (project / ".git").exists():
        print("SKIP no-secrets-in-diff: not a git working tree")
        return 0
    diff = _git_diff(project)
    if not diff.strip():
        print("PASS no-secrets-in-diff: empty diff")
        return 0
    hits: list[str] = []
    for line in diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for pattern in PATTERNS:
            if pattern.search(line):
                hits.append(line[:200])
                break
    if hits:
        print("FAIL no-secrets-in-diff: possible secrets in added lines")
        for hit in hits[:20]:
            print(f"  {hit}")
        return 1
    print("PASS no-secrets-in-diff: no secret-like additions detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
