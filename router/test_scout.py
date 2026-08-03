"""Unit tests for Agentit Scout & Incubator pipeline."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from router.scout import add_candidate, inspect_candidate, load_candidates, reject_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTIT_CLI = REPO_ROOT / "agentit"


class ScoutPipelineTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.project_dir = Path(self.tmpdir.name)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_scout_status_cli(self) -> None:
        proc = subprocess.run(
            [str(AGENTIT_CLI), "scout", "status", "--project", str(self.project_dir)],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertIn("active_candidates", data)
        self.assertIn("candidates", data)

    def test_scout_add_and_inspect_cli(self) -> None:
        add_proc = subprocess.run(
            [str(AGENTIT_CLI), "scout", "add", "https://x.com/test_idea", "--project", str(self.project_dir)],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(add_proc.stdout)
        self.assertEqual(data["source"], "https://x.com/test_idea")
        cand_id = data["id"]

        inspect_proc = subprocess.run(
            [str(AGENTIT_CLI), "scout", "inspect", cand_id, "--project", str(self.project_dir)],
            capture_output=True,
            text=True,
            check=True,
        )
        inspected = json.loads(inspect_proc.stdout)
        self.assertEqual(inspected["id"], cand_id)


if __name__ == "__main__":
    unittest.main()
