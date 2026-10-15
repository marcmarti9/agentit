#!/usr/bin/env python3
"""Classify GitHub CI changes: cheap checks for skill content, full gates for code.

Unknown/empty diffs, failed Git lookups, and changes to Agentit's core skills
fail closed to the full test matrix. This never selects or activates skills.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

CORE_SKILLS = {"using-agentit", "task-router", "using-agent-skills"}
CATALOG_FILES = {
    "profiles.yaml",
    "references/agentit-skill-packs.md",
    "skills/UPSTREAM_LOCK.json",
    "skills/UPSTREAM_SOURCES.md",
    "skills/ADAPTATION_SOURCES.json",
    "THIRD_PARTY_NOTICES.md",
    "README.md",
}
SKILL_CONTENT_SUFFIXES = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".csv",
    ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".css",
    ".woff", ".woff2",
}


def content_only_path(path: str) -> bool:
    """Allowlist safe, non-executable content and catalog metadata."""
    if path in CATALOG_FILES:
        return True
    if path.startswith(("docs/", "reports/")):
        return Path(path).suffix.lower() in {".md", ".txt"}
    if path.startswith("vendor/licenses/"):
        return Path(path).name in {"LICENSE", "NOTICE"} or Path(path).suffix.lower() in {".md", ".txt"}
    if path.startswith("skills/"):
        parts = Path(path).parts
        if len(parts) < 3 or parts[1] in CORE_SKILLS:
            return False
        return Path(path).suffix.lower() in SKILL_CONTENT_SUFFIXES
    return False


def needs_full_suite(paths: list[str]) -> bool:
    return not paths or any(not content_only_path(path) for path in paths)


def changed_paths(base: str, head: str) -> list[str]:
    """Use exact commits, never just the last commit in a multi-commit push."""
    if not base or set(base) == {"0"}:
        raise ValueError("missing base commit")
    if subprocess.run(["git", "cat-file", "-e", f"{base}^{{commit}}"], capture_output=True).returncode:
        subprocess.run(
            ["git", "fetch", "--no-tags", "--depth=1", "origin", base],
            check=True, capture_output=True, timeout=60,
        )
    completed = subprocess.run(
        ["git", "diff", "--name-only", "-z", base, head],
        check=True, capture_output=True, timeout=60,
    )
    return sorted(set(os.fsdecode(path) for path in completed.stdout.split(b"\0") if path))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="", help="PR base SHA or push before SHA")
    parser.add_argument("--head", default="HEAD", help="Checked-out commit")
    args = parser.parse_args()

    try:
        paths = changed_paths(args.base, args.head)
        full = needs_full_suite(paths)
        print(f"CI scope: {'full' if full else 'skill-content'} ({len(paths)} changed files)")
        if not full:
            print("Only non-executable skills/catalog/docs changed; skipping full OS bootstrap.")
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        full = True
        print(f"CI scope: full (unable to prove a content-only diff: {error})")

    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as target:
            target.write(f"run_full={'true' if full else 'false'}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
