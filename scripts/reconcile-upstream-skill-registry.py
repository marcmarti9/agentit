#!/usr/bin/env python3
"""Reconcile Agentit-owned routing/runtime around canonical upstream skill packages.

The vendored skill directories themselves are deliberately never rewritten here.
This script only migrates Agentit-owned catalog IDs, pack-map paths, installers,
notices, and regression coverage after ``sync-upstream-skills.sh`` refreshes the
canonical packages.
"""

from __future__ import annotations

import json
import re
import stat
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "skills" / "UPSTREAM_LOCK.json"

ALIASES = {
    "anti-ai-slop-design": "hallmark",
    "anti-ai-slop-writing": "humanizer",
    "ui-ux-pro-max-intelligence": "ui-ux-pro-max",
    "mobile-native-app-design": "appllama-app-design-skill",
    "diagram-and-architecture-visuals": "diagram-design",
}

PATH_REPLACEMENTS = {
    "skills/using-agent-skills/references/packs.md": "references/agentit-skill-packs.md",
}

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".json", ".sh", ".toml", ".txt"}


def load_lock() -> dict:
    payload = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or not isinstance(payload.get("mappings"), list):
        raise SystemExit("invalid skills/UPSTREAM_LOCK.json")
    return payload


def vendored_roots(lock: dict) -> set[Path]:
    return {ROOT / "skills" / str(item["skill"]) for item in lock["mappings"]}


def inside_any(path: Path, roots: set[Path]) -> bool:
    return any(path == root or root in path.parents for root in roots)


def migrate_agentit_owned_text(lock: dict) -> None:
    """Migrate old adapter IDs and pack-map references outside vendored packages."""
    vendored = vendored_roots(lock)
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or inside_any(path, vendored):
            continue
        if path == LOCK_PATH:
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name != "agentit":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = text
        for old, new in PATH_REPLACEMENTS.items():
            updated = updated.replace(old, new)
        for old, new in ALIASES.items():
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def patch_skills_cli() -> None:
    path = ROOT / "router" / "skills_cli.py"
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        r'^PACKS_PATH\s*=.*$',
        'PACKS_PATH = HARNESS_ROOT / "references" / "agentit-skill-packs.md"',
        text,
        count=1,
        flags=re.M,
    )
    if count != 1:
        raise SystemExit("could not migrate router/skills_cli.py PACKS_PATH")
    path.write_text(updated, encoding="utf-8")


def patch_profiles() -> None:
    path = ROOT / "profiles.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    profiles = payload.get("profiles")
    if not isinstance(profiles, dict):
        raise SystemExit("profiles.yaml has no profiles mapping")

    for profile in profiles.values():
        skills = profile.get("skills", [])
        if not isinstance(skills, list):
            continue
        for old, new in ALIASES.items():
            skills[:] = [new if item == old else item for item in skills]
        # The two old compact wrappers represented two upstream packages each.
        if "humanizer" in skills and "stop-slop" not in skills:
            skills.insert(skills.index("humanizer") + 1, "stop-slop")
        if "appllama-app-design-skill" in skills and "appllama-usage" not in skills:
            skills.insert(skills.index("appllama-app-design-skill") + 1, "appllama-usage")

    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def replace_function(text: str, name: str, replacement: str) -> str:
    pattern = re.compile(
        rf"(?ms)^def {re.escape(name)}\(.*?(?=^def |\Z)",
    )
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"could not find function {name}")
    return text[: match.start()] + replacement.rstrip() + "\n\n\n" + text[match.end() :]


def patch_private_jit() -> None:
    path = ROOT / "router" / "profile_jit_cli.py"
    text = path.read_text(encoding="utf-8")

    package_function = '''def _package_files(source_dir: Path) -> list[str]:
    """Return every regular file in a complete skill package."""
    if not source_dir.is_dir() or source_dir.is_symlink():
        raise ProfileError(f"skill source is not a regular directory: {source_dir}")
    skill_md = source_dir / "SKILL.md"
    if not skill_md.is_file() or skill_md.is_symlink():
        raise ProfileError(f"skill source body missing: {skill_md}")
    files = ["SKILL.md"]
    for file_path in sorted(source_dir.rglob("*")):
        if file_path.is_symlink():
            raise ProfileError(f"skill package rejects symlinks: {file_path}")
        if file_path.is_file() and file_path != skill_md:
            files.append(file_path.relative_to(source_dir).as_posix())
    return files'''
    text = replace_function(text, "_package_files", package_function)

    constants_marker = 'LEGACY_HOST_ROOT = Path(".agents") / "skills"\n'
    constants = (
        constants_marker
        + 'PRIVATE_SHARED_REFERENCE_ROOT = Path(".agentit") / "references"\n'
        + 'ADDY_SHARED_REFERENCE_MANIFEST = Path("references") / ".addy-agent-skills-files"\n'
    )
    if "PRIVATE_SHARED_REFERENCE_ROOT" not in text:
        if constants_marker not in text:
            raise SystemExit("could not find private JIT constants insertion point")
        text = text.replace(constants_marker, constants, 1)

    helper_marker = "def _source_dir(repo_root: Path, skill_id: str) -> Path:\n"
    if "def _shared_reference_files(" not in text:
        helpers = '''def _shared_reference_files(repo_root: Path) -> list[str]:
    manifest = repo_root / ADDY_SHARED_REFERENCE_MANIFEST
    if not manifest.exists():
        return []
    if not manifest.is_file() or manifest.is_symlink():
        raise ProfileError(f"shared reference manifest is unsafe: {manifest}")
    result: list[str] = []
    for raw in manifest.read_text(encoding="utf-8").splitlines():
        relative = raw.strip()
        if not relative:
            continue
        rel = Path(relative)
        if rel.is_absolute() or ".." in rel.parts:
            raise ProfileError(f"unsafe shared reference path: {relative}")
        source = repo_root / "references" / rel
        if not source.is_file() or source.is_symlink():
            raise ProfileError(f"shared reference source missing or unsafe: {source}")
        result.append(rel.as_posix())
    return sorted(set(result))


def _sync_shared_references(*, project: Path, repo_root: Path) -> None:
    destination_root = project / PRIVATE_SHARED_REFERENCE_ROOT
    destination_manifest = destination_root / ".addy-agent-skills-files"
    if destination_manifest.exists():
        if not destination_manifest.is_file() or destination_manifest.is_symlink():
            raise ProfileError(
                f"private shared reference manifest is unsafe: {destination_manifest}"
            )
        for raw in destination_manifest.read_text(encoding="utf-8").splitlines():
            relative = raw.strip()
            if not relative:
                continue
            rel = Path(relative)
            if rel.is_absolute() or ".." in rel.parts:
                raise ProfileError(f"unsafe cached shared reference path: {relative}")
            stale = destination_root / rel
            _assert_project_path(stale, project=project)
            if stale.exists():
                if not stale.is_file() or stale.is_symlink():
                    raise ProfileError(f"private shared reference cache is unsafe: {stale}")
                stale.unlink()

    for relative in _shared_reference_files(repo_root):
        _copy_atomic(
            repo_root / "references" / relative,
            destination_root / relative,
            project=project,
        )

    source_manifest = repo_root / ADDY_SHARED_REFERENCE_MANIFEST
    if source_manifest.exists():
        _copy_atomic(source_manifest, destination_manifest, project=project)


'''
        if helper_marker not in text:
            raise SystemExit("could not find shared reference helper insertion point")
        text = text.replace(helper_marker, helpers + helper_marker, 1)

    # Add shared-reference planning to _enable exactly once.
    if "sync shared reference:" not in text:
        old = (
            "    stale = _private_cleanup_plan(project=project, old_manifest=old, payload=payload)\n"
            "    operations: list[str] = []\n"
        )
        new = (
            "    stale = _private_cleanup_plan(project=project, old_manifest=old, payload=payload)\n"
            "    shared_references = _shared_reference_files(repo_root)\n"
            "    operations: list[str] = []\n"
            "    operations.extend(\n"
            "        f\"sync shared reference: {project / PRIVATE_SHARED_REFERENCE_ROOT / relative}\"\n"
            "        for relative in shared_references\n"
            "    )\n"
        )
        if old not in text:
            raise SystemExit("could not add shared reference plan to profile JIT enable")
        text = text.replace(old, new, 1)

    # Execute sync only in the apply path and before stale cleanup.
    if "_sync_shared_references(project=project, repo_root=repo_root)" not in text:
        enable_start = text.index("def _enable(")
        stale_loop = text.index("    for item in stale:\n", enable_start)
        text = (
            text[:stale_loop]
            + "    _sync_shared_references(project=project, repo_root=repo_root)\n\n"
            + text[stale_loop:]
        )

    path.write_text(text, encoding="utf-8")


def patch_bootstrap() -> None:
    path = ROOT / "router" / "bootstrap.py"
    text = path.read_text(encoding="utf-8")
    if 'category=f"provider:{provider}:shared-reference"' in text:
        return

    needle = '''            _append_tree_specs(
                specs,
                source_base=src,
                destination_base=skills_root / skill_id,
                category=f"provider:{provider}:skill",
            )

        if provider == "codex" and config.get("codex_agents_source"):
'''
    insertion = '''            _append_tree_specs(
                specs,
                source_base=src,
                destination_base=skills_root / skill_id,
                category=f"provider:{provider}:skill",
            )

        addy_reference_manifest = source_root / "references" / ".addy-agent-skills-files"
        if "using-agent-skills" in core_skills and addy_reference_manifest.is_file():
            for raw in addy_reference_manifest.read_text(encoding="utf-8").splitlines():
                relative = raw.strip()
                if not relative:
                    continue
                rel = _assert_relative(relative)
                src = _source(source_root, Path("references") / rel)
                specs.append(
                    CopySpec(
                        source=src,
                        destination=skills_root.parent / "references" / rel,
                        mode=stat.S_IMODE(src.stat().st_mode),
                        category=f"provider:{provider}:shared-reference",
                    )
                )

        if provider == "codex" and config.get("codex_agents_source"):
'''
    if needle not in text:
        raise SystemExit("could not extend provider bootstrap with shared references")
    path.write_text(text.replace(needle, insertion, 1), encoding="utf-8")


def patch_design_sync_wrapper() -> None:
    path = ROOT / "scripts" / "sync-upstream-design-skills.sh"
    path.write_text(
        '''#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "sync-upstream-design-skills.sh is deprecated; syncing the complete canonical skill registry." >&2
exec "$ROOT/scripts/sync-upstream-skills.sh" "$@"
''',
        encoding="utf-8",
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def replace_notice_section(text: str, heading: str, body: str) -> str:
    pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\n.*?(?=^## |\Z)")
    replacement = f"## {heading}\n\n{body.strip()}\n\n"
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    return text.rstrip() + "\n\n" + replacement


def patch_notices() -> None:
    path = ROOT / "THIRD_PARTY_NOTICES.md"
    text = path.read_text(encoding="utf-8")
    sections = {
        "Addy Osmani / Agent Skills": """Source: https://github.com/addyosmani/agent-skills

MIT License. Copyright (c) 2025 Addy Osmani.

Agentit vendors the canonical upstream packages for its matching engineering skill IDs without compressing or rewriting their skill bodies. Addy's repo-level shared `references/` checklists are vendored at Agentit's root `references/` so upstream relative links remain valid. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "GreenSock / GSAP Skills": """Source: https://github.com/greensock/gsap-skills

Agentit vendors the canonical upstream `gsap-scrolltrigger` and `gsap-performance` skill packages without compressing or rewriting their bodies. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "Next Level Builder / UI UX Pro Max Skill": """Source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

Agentit vendors the canonical `.claude/skills/ui-ux-pro-max` package in full, including its data, references and scripts. The former compact `ui-ux-pro-max-intelligence` adapter is retired. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "Appllama / Appllama Skills": """Source: https://github.com/Appllama/appllama-skills

Agentit vendors the canonical `appllama-app-design-skill` and `appllama-usage` packages in full. The former compact `mobile-native-app-design` adapter is retired. Live Appllama MCP availability remains an external capability decision, not bundled credentials or access. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "Siqi Chen / Humanizer": """Source: https://github.com/blader/humanizer

Agentit vendors the canonical Humanizer skill package, including its upstream agents/scripts, instead of maintaining a compressed prose synthesis. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "Hardik Pandya / Stop Slop": """Source: https://github.com/hardikpandya/stop-slop

Agentit vendors the canonical Stop Slop skill package and references instead of folding it into a compressed local writing wrapper. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "Cathryn Lavery / Diagram Design": """Source: https://github.com/cathrynlavery/diagram-design

Agentit vendors the canonical `diagram-design` package in full. The former compact `diagram-and-architecture-visuals` adapter is retired. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "Supabase / Agent Skills": """Source: https://github.com/supabase/agent-skills

MIT License. Copyright (c) 2026 Supabase.

Agentit vendors the canonical `supabase-postgres-best-practices` package in full. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "Nutlope / Hallmark": """Source: https://github.com/Nutlope/hallmark

Agentit vendors the canonical `hallmark` anti-AI-design-slop package in full. The former local `anti-ai-slop-design` adapter is retired. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "Vercel Labs / Skills": """Source: https://github.com/vercel-labs/skills

Agentit vendors the canonical `find-skills` package in full. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
        "Jesse Vincent / Superpowers": """Source: https://github.com/obra/superpowers

Agentit vendors the canonical `verification-before-completion` package in full. Agentit-specific Loop/Graph receipt enforcement remains in Agentit's own runtime/core policy rather than being injected into the vendored skill body. Exact snapshots are recorded in `skills/UPSTREAM_LOCK.json`.""",
    }
    for heading, body in sections.items():
        text = replace_notice_section(text, heading, body)
    path.write_text(text, encoding="utf-8")


def write_registry_tests() -> None:
    path = ROOT / "router" / "test_upstream_skill_registry.py"
    path.write_text(
        '''import json
import tempfile
import unittest
from pathlib import Path

from router.profile_jit_cli import _package_files, _shared_reference_files
from router.profiles import load_catalog, resolve_profile

ROOT = Path(__file__).resolve().parents[1]


class UpstreamSkillRegistryTests(unittest.TestCase):
    def test_every_canonical_mapping_exists_as_complete_skill_package(self):
        lock = json.loads((ROOT / "skills" / "UPSTREAM_LOCK.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(lock["mappings"]), 39)
        for item in lock["mappings"]:
            skill = ROOT / "skills" / item["skill"]
            self.assertTrue((skill / "SKILL.md").is_file(), item["skill"])

    def test_retired_compact_aliases_are_absent(self):
        for skill_id in (
            "anti-ai-slop-design",
            "anti-ai-slop-writing",
            "ui-ux-pro-max-intelligence",
            "mobile-native-app-design",
            "diagram-and-architecture-visuals",
        ):
            self.assertFalse((ROOT / "skills" / skill_id).exists(), skill_id)

    def test_multifile_private_jit_package_includes_every_regular_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "skill"
            (skill / "scripts").mkdir(parents=True)
            (skill / "assets").mkdir()
            (skill / "agents").mkdir()
            (skill / "SKILL.md").write_text("# skill\\n", encoding="utf-8")
            (skill / "scripts" / "x.mjs").write_text("export {};\\n", encoding="utf-8")
            (skill / "assets" / "x.txt").write_text("asset\\n", encoding="utf-8")
            (skill / "agents" / "x.toml").write_text('name="x"\\n', encoding="utf-8")
            self.assertEqual(
                _package_files(skill),
                ["SKILL.md", "agents/x.toml", "assets/x.txt", "scripts/x.mjs"],
            )

    def test_addy_shared_reference_manifest_resolves(self):
        refs = _shared_reference_files(ROOT)
        self.assertTrue(refs)
        self.assertIn("definition-of-done.md", refs)
        for relative in refs:
            self.assertTrue((ROOT / "references" / relative).is_file())

    def test_profiles_resolve_canonical_replacements(self):
        catalog = load_catalog(ROOT / "profiles.yaml")
        resolved = resolve_profile("all", catalog, repo_root=ROOT)
        for skill_id in (
            "humanizer",
            "stop-slop",
            "hallmark",
            "ui-ux-pro-max",
            "appllama-app-design-skill",
            "appllama-usage",
            "diagram-design",
        ):
            self.assertIn(skill_id, resolved)


if __name__ == "__main__":
    unittest.main()
''',
        encoding="utf-8",
    )


def main() -> int:
    lock = load_lock()
    migrate_agentit_owned_text(lock)
    patch_skills_cli()
    patch_profiles()
    patch_private_jit()
    patch_bootstrap()
    patch_design_sync_wrapper()
    patch_notices()
    write_registry_tests()
    print(f"Reconciled Agentit around {len(lock['mappings'])} canonical upstream skill packages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
