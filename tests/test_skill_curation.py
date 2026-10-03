from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_skill_curation import check_catalog, check_sources, checked_file
from router.skill_loader import load_reference_bodies, load_skill_bodies, validate_bodies
from router.skills_cli import pack_candidates

ROOT = Path(__file__).resolve().parents[1]
NEW = {"property-based-testing", "data-analysis-quality", "security-analysis",
       "mobile-runtime-engineering", "artifact-production"}


class SkillCurationTests(unittest.TestCase):
    def test_complete_catalog_and_provenance_invariants(self):
        result = check_catalog()
        self.assertEqual(result["status"], "verified")

    def test_new_skills_discover_without_delivering_bodies(self):
        candidates = pack_candidates(["engineering", "backend", "data", "mobile", "writing"])
        self.assertTrue(NEW <= {c["id"] for c in candidates})
        self.assertTrue(all(set(c) == {"pack", "id", "description"} for c in candidates))

    def test_single_selected_body_is_exact_and_branch_references_remain_explicit(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            for skill in sorted(NEW):
                bodies = load_skill_bodies([skill], project_root=project)
                validate_bodies([skill], bodies)
                self.assertEqual([skill], [b["id"] for b in bodies])
                self.assertEqual((ROOT / "skills" / skill / "SKILL.md").read_text(), bodies[0]["content"])
                for ref in (ROOT / "skills" / skill / "references").glob("*.md"):
                    uri = f"skill:{skill}/references/{ref.name}"
                    refs = load_reference_bodies([uri], project_root=project)
                    self.assertEqual([uri], [r["id"] for r in refs])
                    self.assertEqual(ref.read_text(), refs[0]["content"])
                    # A branch body must not be silently appended to activation.
                    self.assertNotIn(ref.read_text(), bodies[0]["content"])

    def test_provenance_rejects_license_tampering_unfixed_revision_and_missing_target(self):
        manifest = json.loads((ROOT / "skills/ADAPTATION_SOURCES.json").read_text())
        mutations = [lambda d: d["sources"][0].update(license_sha256="0" * 64),
                     lambda d: d["sources"][0].update(revision="main"),
                     lambda d: d["sources"][0].update(source_license="free-for-any-use"),
                     lambda d: d["sources"][0].update(adaptation_license="Apache-99.0"),
                     lambda d: d["sources"][0].update(targets=["skills/missing/SKILL.md"])]
        for mutate in mutations:
            bad = copy.deepcopy(manifest)
            mutate(bad)
            with self.assertRaises(ValueError):
                check_sources(ROOT, bad)

    def test_provenance_rejects_traversal_and_symlink_components(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "real").mkdir()
            (root / "real/license").write_text("license")
            (root / "link").symlink_to(root / "real", target_is_directory=True)
            for path in ("../license", "/tmp/license", "link/license", "real\\license"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    checked_file(root, path)

    def test_coverage_fixtures_have_negative_boundaries_and_valid_explicit_choices(self):
        data = json.loads((ROOT / "evals/skill-curation-cases.json").read_text())
        ids = [c["id"] for c in data["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        known = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        for case in data["cases"]:
            self.assertTrue(case["prompt"] and case["quality_assertions"])
            self.assertTrue(set(case["required"] + case["forbidden"]) <= known)
            self.assertFalse(set(case["required"]) & set(case["forbidden"]))
            for choice in case.get("acceptable_primary_sets", []):
                self.assertTrue(choice and set(choice) <= known)
                self.assertFalse(set(choice) & set(case["forbidden"]))
        for skill in NEW:
            self.assertTrue(any(skill in c["required"] for c in data["cases"]), skill)
            self.assertTrue(any(skill in c["forbidden"] for c in data["cases"]), skill)


if __name__ == "__main__":
    unittest.main()
