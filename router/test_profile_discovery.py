from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

from router.profiles import load_catalog, resolve_profile
from router.skills_cli import (SkillDiscoveryError, list_profiles, profile_candidates,
                               skill_metadata, list_packs, pack_candidates)
from scripts.build_profile_index import build, validate_coverage

ROOT = Path(__file__).resolve().parents[1]


class ProfileDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()
        cls.metadata = skill_metadata()

    def test_every_canonical_skill_has_a_source_neutral_domain_home(self):
        validate_coverage(self.catalog, self.metadata)
        covered = set()
        for profile_id, profile in self.catalog["profiles"].items():
            if profile_id != "all" and not profile.get("compatibility_alias"):
                self.assertFalse(profile_id.startswith("ecc"))
                covered.update(resolve_profile(profile_id, self.catalog))
        self.assertEqual(set(self.metadata), covered)
        self.assertEqual(set(self.metadata), set(resolve_profile("all", self.catalog)))

    def test_catch_all_and_compatibility_alias_do_not_hide_orphans(self):
        catalog = {"profiles": {
            "core": {"description": "entry", "skills": ["entry"]},
            "ecc": {"description": "legacy", "compatibility_alias": True, "skills": ["orphan"]},
            "all": {"description": "inventory", "extends": ["core", "ecc"]},
        }}
        with self.assertRaisesRegex(SkillDiscoveryError, "without a domain profile: orphan"):
            validate_coverage(catalog, {"entry": {}, "orphan": {}})

    def test_profiles_only_expose_metadata_and_cost_including_unique_inheritance(self):
        with patch("router.skills_cli.load_skill_bodies", side_effect=AssertionError("must not activate")):
            profiles = list_profiles()
        self.assertNotIn("ecc-web", {item["id"] for item in profiles})
        self.assertIn("ecc-web", {item["id"] for item in list_profiles(include_aliases=True)})
        item = next(item for item in profiles if item["id"] == "frontend")
        ids = resolve_profile("frontend", self.catalog)
        self.assertEqual(len(ids), item["skill_count"])
        self.assertEqual(sum(self.metadata[sid]["body_bytes"] for sid in ids), item["body_bytes"])
        self.assertTrue(all("content" not in item for item in profiles))
        self.assertIn("references/agentit-profile-index.md#frontend", item["reference"])

    def test_candidates_are_unified_bounded_and_do_not_activate(self):
        with patch("router.skills_cli.load_skill_bodies", side_effect=AssertionError("must not activate")):
            items = profile_candidates(["frontend", "frontend"], direct=True)
        ids = [item["id"] for item in items]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("frontend-ui-engineering", ids)
        self.assertIn("react-patterns", ids)
        self.assertNotIn("using-agentit", ids)
        self.assertNotIn("executive-finance", ids)
        self.assertEqual({"agentit", "ecc"}, {item["source"] for item in items})
        for item in items:
            self.assertNotIn("content", item)
            self.assertEqual((ROOT / item["path"]).stat().st_size, item["body_bytes"])
            self.assertEqual((item["body_bytes"] + 3) // 4, item["estimated_tokens"])

    def test_domains_do_not_inherit_unrelated_frameworks_or_authoring_workflows(self):
        mobile = set(resolve_profile("mobile", self.catalog))
        design = set(resolve_profile("design", self.catalog))
        artifacts = set(resolve_profile("artifacts", self.catalog))
        self.assertIn("frontend-ui-engineering", mobile)
        self.assertIn("app-security-gate", mobile)
        self.assertNotIn("angular-developer", mobile)
        self.assertNotIn("vue-patterns", mobile)
        self.assertIn("web-design-guidelines", design)
        self.assertIn("browser-testing-with-devtools", design)
        self.assertNotIn("react-testing", design)
        self.assertNotIn("nextjs-turbopack", design)
        self.assertIn("artifact-production", artifacts)
        self.assertNotIn("skill-authoring-and-evals", artifacts)
        self.assertNotIn("i-have-adhd", artifacts)

    def test_legacy_pack_id_resolves_to_unified_domain_without_duplicate_catalog(self):
        self.assertFalse(any(item["id"].startswith("ecc-") for item in list_packs()))
        items = pack_candidates(["ecc-web", "ecc-web"])
        self.assertEqual(set(resolve_profile("frontend", self.catalog)), {item["id"] for item in items})
        self.assertEqual(len(items), len({item["id"] for item in items}))

    def test_pack_metadata_covers_all_non_global_skills(self):
        ids = {item["id"] for item in pack_candidates([item["id"] for item in list_packs()])}
        self.assertEqual(set(), ids - self.metadata.keys())
        self.assertEqual(set(), self.metadata.keys() - ids - set(resolve_profile("core", self.catalog)))

    def test_cli_profiles_and_profile_candidates_and_invalid_selection(self):
        result = subprocess.run([sys.executable, str(ROOT / "agentit"), "skills", "candidates",
                                 "--profile", "healthcare", "--direct", "--format", "json"],
                                capture_output=True, text=True, check=True)
        candidates = json.loads(result.stdout)["candidates"]
        self.assertEqual(set(self.catalog["profiles"]["healthcare"]["skills"]), {item["id"] for item in candidates})
        for flags in ([], ["engineering", "--profile", "frontend"], ["engineering", "--direct"], ["--profile", "nonexistent"]):
            result = subprocess.run([sys.executable, str(ROOT / "agentit"), "skills", "candidates", *flags],
                                    capture_output=True, text=True)
            self.assertEqual(2, result.returncode, result.stderr)

    def test_generator_detects_drift_without_writing_in_check_mode(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "skills/using-agentit").mkdir(parents=True)
            (root / "references").mkdir()
            core = root / "skills/using-agentit/SKILL.md"
            core.write_text("---\nname: using-agentit\ndescription: Enter Agentit\n---\n\n<!-- profile-pointers:start -->\nold\n<!-- profile-pointers:end -->\n")
            catalog = {"schema_version": 1, "default_profile": "core", "global_profiles": ["core"], "profiles": {
                "core": {"description": "Enter Agentit", "skills": ["using-agentit"]},
                "all": {"description": "Explicit inventory", "extends": ["core"]},
            }}
            path = root / "profiles.yaml"
            path.write_text(yaml.safe_dump(catalog))
            self.assertEqual(2, len(build(root, check=True)))
            self.assertIn("old", core.read_text())
            build(root, check=False)
            self.assertEqual([], build(root, check=True))
            catalog["profiles"]["core"]["description"] = "Changed purpose"
            path.write_text(yaml.safe_dump(catalog))
            before = core.read_bytes()
            self.assertEqual(2, len(build(root, check=True)))
            self.assertEqual(before, core.read_bytes())

    def test_repository_profile_pointers_and_costs_are_current(self):
        self.assertEqual([], build(ROOT, check=True), "run python3 scripts/build_profile_index.py")


if __name__ == "__main__":
    unittest.main()
