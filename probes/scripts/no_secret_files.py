#!/usr/bin/env python3
"""Fail if secret-looking files are present at common project paths."""

from __future__ import annotations

import sys
from pathlib import Path

SUSPECT_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "service-account.json",
    "id_rsa",
    "id_ed25519",
}


def main() -> int:
    project = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    hits: list[str] = []
    for path in project.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(project).as_posix()
        if any(part in {".git", "node_modules", ".venv", "venv", "dist", "build"} for part in path.parts):
            continue
        name = path.name
        if name in SUSPECT_NAMES or name.endswith(".pem"):
            # Allow documented examples
            if "example" in name.lower() or rel.endswith(".example"):
                continue
            hits.append(rel)
        if name == ".env" or name.startswith(".env."):
            if "example" not in name.lower() and not name.endswith(".example"):
                if rel not in hits:
                    hits.append(rel)
    if hits:
        print("FAIL no-secret-files: suspect files present")
        for hit in sorted(set(hits))[:50]:
            print(f"  {hit}")
        return 1
    print("PASS no-secret-files: no suspect credential files found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
