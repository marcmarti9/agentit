"""Provider-neutral capability catalog and resolution contract tests."""

from __future__ import annotations

import tempfile
import json
import subprocess
import unittest
from pathlib import Path

import yaml

from router.capabilities import (
    CapabilityCatalogError,
    load_capability_catalog,
    resolve_capabilities,
    specialist_capability_requirements,
)


REPOSITORY = Path(__file__).resolve().parents[1]
CAPABILITY_CATALOG = REPOSITORY / "capabilities" / "catalog.yaml"
SPECIALIST_CATALOG = REPOSITORY / "agents" / "catalog.yaml"


class CapabilityCatalogTests(unittest.TestCase):
    def test_repository_catalog_is_valid_and_provider_neutral(self):
        catalog = load_capability_catalog(CAPABILITY_CATALOG)

        self.assertEqual(1, catalog["schema_version"])
        self.assertTrue(catalog["policy"]["explicit_inventory_required"])
        self.assertGreaterEqual(len(catalog["capabilities"]), 12)
        self.assertGreaterEqual(len(catalog["providers"]), 12)

    def test_rejects_capability_with_unknown_provider_binding(self):
        payload = {
            "schema_version": 1,
            "policy": {"explicit_inventory_required": True},
            "providers": {},
            "capabilities": {
                "repository.read": {
                    "description": "Read a repository",
                    "implementations": [
                        {"provider": "mcp.missing", "permissions": ["repository:read"]}
                    ],
                }
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.yaml"
            path.write_text(yaml.safe_dump(payload), encoding="utf-8")
            with self.assertRaises(CapabilityCatalogError):
                load_capability_catalog(path)

    def test_all_specialist_capability_references_exist(self):
        catalog = load_capability_catalog(CAPABILITY_CATALOG)
        specialists = yaml.safe_load(SPECIALIST_CATALOG.read_text(encoding="utf-8"))
        known = set(catalog["capabilities"])

        for specialist in specialists["specialists"]:
            declared = specialist["capabilities"]
            self.assertTrue(declared["required"] or declared["preferred"], specialist["id"])
            self.assertTrue(set(declared["required"]).issubset(known), specialist["id"])
            self.assertTrue(set(declared["preferred"]).issubset(known), specialist["id"])
            for capability_id in declared["required"] + declared["preferred"]:
                self.assertNotIn("chatgpt.", capability_id)
                self.assertNotIn("mcp.", capability_id)
                self.assertNotIn("cli.", capability_id)

    def test_mcp_provider_bindings_exist_in_agentit_mcp_catalog(self):
        catalog = load_capability_catalog(CAPABILITY_CATALOG)
        mcp_catalog = yaml.safe_load(
            (REPOSITORY / "mcp" / "catalog.yaml").read_text(encoding="utf-8")
        )
        known_mcp = {item["id"] for item in mcp_catalog["servers"]}
        bound_mcp = {
            provider_id.removeprefix("mcp.")
            for provider_id, provider in catalog["providers"].items()
            if provider["kind"] == "mcp"
        }
        self.assertTrue(bound_mcp.issubset(known_mcp), bound_mcp - known_mcp)


class CapabilityResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_capability_catalog(CAPABILITY_CATALOG)

    def test_uses_ordered_fallback_when_mcp_is_unavailable(self):
        envelope = resolve_capabilities(
            required=["repository.read"],
            preferred=[],
            available_providers=["cli.git"],
            host="codex",
            catalog=self.catalog,
        )

        self.assertEqual("resolved", envelope["status"])
        self.assertEqual("cli.git", envelope["grants"][0]["provider"])
        self.assertEqual(["repository:read"], envelope["grants"][0]["permissions"])
        chain = envelope["resolution"]["repository.read"]["candidates"]
        self.assertEqual("chatgpt.github", chain[0]["provider"])
        self.assertEqual("host_incompatible", chain[0]["reason"])
        self.assertEqual("provider_unavailable", chain[1]["reason"])
        self.assertTrue(chain[2]["selected"])

    def test_skips_available_binding_that_is_incompatible_with_host(self):
        envelope = resolve_capabilities(
            required=["design.inspect"],
            preferred=[],
            available_providers=["chatgpt.figma", "mcp.figma"],
            host="codex",
            catalog=self.catalog,
        )

        self.assertEqual("mcp.figma", envelope["grants"][0]["provider"])
        first = envelope["resolution"]["design.inspect"]["candidates"][0]
        self.assertEqual("host_incompatible", first["reason"])

    def test_reports_missing_required_without_granting_unrelated_providers(self):
        envelope = resolve_capabilities(
            required=["mail.send"],
            preferred=["calendar.read"],
            available_providers=["chatgpt.google-calendar", "cli.git"],
            host="chatgpt",
            catalog=self.catalog,
        )

        self.assertEqual("degraded", envelope["status"])
        self.assertEqual(["mail.send"], envelope["unresolved_required"])
        self.assertEqual(["calendar.read"], [g["capability"] for g in envelope["grants"]])
        self.assertNotIn("cli.git", {g["provider"] for g in envelope["grants"]})

    def test_omitted_inventory_is_unknown_not_unavailable(self):
        envelope = resolve_capabilities(
            required=["repository.read"],
            preferred=[],
            available_providers=None,
            host="codex",
            catalog=self.catalog,
        )

        self.assertEqual("inventory_required", envelope["status"])
        self.assertFalse(envelope["inventory_provided"])
        self.assertEqual([], envelope["grants"])
        self.assertEqual([], envelope["unresolved_required"])
        self.assertEqual(["repository.read"], envelope["pending_inventory"])

    def test_unknown_host_fails_closed(self):
        with self.assertRaises(CapabilityCatalogError):
            resolve_capabilities(
                required=["repository.read"],
                preferred=[],
                available_providers=["cli.git"],
                host="unknown-host",
                catalog=self.catalog,
            )

    def test_specialist_requirements_merge_and_deduplicate(self):
        requirements = specialist_capability_requirements(
            ["frontend-developer", "design-critic"],
            specialist_catalog_path=SPECIALIST_CATALOG,
            capability_catalog=self.catalog,
        )

        self.assertIn("repository.read", requirements["required"])
        self.assertIn("design.inspect", requirements["preferred"])
        self.assertEqual(
            len(requirements["required"]), len(set(requirements["required"]))
        )


class CapabilityCliTests(unittest.TestCase):
    def test_cli_resolves_specialist_with_explicit_inventory(self):
        proc = subprocess.run(
            [
                str(REPOSITORY / "agentit"),
                "capabilities",
                "resolve",
                "--specialist",
                "frontend-developer",
                "--host",
                "codex",
                "--available",
                "mcp.github,local.filesystem",
            ],
            cwd=REPOSITORY,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(proc.stdout)
        grants = {item["capability"]: item["provider"] for item in payload["grants"]}
        self.assertEqual("mcp.github", grants["repository.read"])
        self.assertEqual("local.filesystem", grants["filesystem.write"])


if __name__ == "__main__":
    unittest.main()
