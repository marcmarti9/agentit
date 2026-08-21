import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


class ProfileCatalogTests(unittest.TestCase):
    def test_growth_and_agency_profiles_add_real_skill_bodies(self):
        from router.profiles import load_catalog, resolve_profile

        catalog = load_catalog(REPOSITORY / "profiles.yaml")
        product = resolve_profile("product", catalog, repo_root=REPOSITORY)
        growth = resolve_profile("growth", catalog, repo_root=REPOSITORY)
        agency = resolve_profile("agency", catalog, repo_root=REPOSITORY)

        self.assertGreater(len(growth), len(product))
        self.assertIn("shipping-and-launch", growth)
        self.assertGreater(len(agency), len(growth))
        self.assertIn("incremental-implementation", agency)
        self.assertIn("git-workflow-and-versioning", agency)
