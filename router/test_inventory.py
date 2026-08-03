import stat
import tempfile
import unittest
from pathlib import Path

import yaml

try:
    from .inventory import build_inventory, write_inventory
except ImportError:
    from inventory import build_inventory, write_inventory


class LocalInventoryTests(unittest.TestCase):
    def test_generated_inventory_records_machine_observations_outside_catalog(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            home = root / "home"
            skill = home / "skill" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("fixture\n", encoding="utf-8")
            registry = root / "registry.yaml"
            registry.write_text(
                yaml.safe_dump(
                    {
                        "schema_version": 1,
                        "providers": [
                            {
                                "id": "fixture-provider",
                                "executable_names": [],
                                "target_roots": ["${HOME}/.fixture"],
                            }
                        ],
                        "entries": [
                            {
                                "id": "fixture-skill",
                                "kind": "skill",
                                "state": "ACTIVE_GLOBAL",
                                "paths": ["${HOME}/skill/SKILL.md"],
                                "essential_dependencies": [],
                            }
                        ],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            output = root / "reports" / "local" / "inventory.yaml"

            write_inventory(output, build_inventory(registry, home))
            observed = yaml.safe_load(output.read_text(encoding="utf-8"))

            path_observation = observed["entries"]["fixture-skill"]["paths"][0]
            self.assertEqual(path_observation["path"], str(skill))
            self.assertTrue(path_observation["exists"])
            self.assertEqual(len(path_observation["sha256"]), 64)
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            self.assertEqual(list(output.parent.glob(".*.tmp-*")), [])


if __name__ == "__main__":
    unittest.main()
