"""Unit tests for private project-local Agentit Scout state."""

import json
import stat
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

    def test_direct_state_is_project_local_private(self) -> None:
        item = add_candidate("https://example.com/tool", project_root=self.project_dir)
        state = self.project_dir / ".agentit" / "scout" / "candidates.yaml"
        self.assertTrue(state.is_file())
        self.assertEqual(stat.S_IMODE(state.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(state.parent.stat().st_mode), 0o700)
        self.assertEqual(item["source"], "https://example.com/tool")
        self.assertEqual(1, len(load_candidates(self.project_dir)["candidates"]))

    def test_reject_roundtrip_stays_project_local(self) -> None:
        item = add_candidate("candidate alpha", project_root=self.project_dir)
        self.assertTrue(reject_candidate(item["id"], "not useful", self.project_dir))
        inspected = inspect_candidate(item["id"], self.project_dir)
        self.assertIsNotNone(inspected)
        self.assertEqual("rejected", inspected["decision"])
        self.assertEqual("not useful", inspected["reason"])

    def test_scout_status_cli(self) -> None:
        proc = subprocess.run(
            [str(AGENTIT_CLI), "scout", "status", "--project", str(self.project_dir)],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertEqual(0, data["active_candidates"])
        self.assertIn("candidates", data)

    def test_scout_add_and_inspect_cli_uses_project_argument(self) -> None:
        add_proc = subprocess.run(
            [str(AGENTIT_CLI), "scout", "add", "https://x.com/test_idea", "--project", str(self.project_dir)],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(add_proc.stdout)
        cand_id = data["id"]
        self.assertEqual(data["source"], "https://x.com/test_idea")
        self.assertTrue((self.project_dir / ".agentit" / "scout" / "candidates.yaml").is_file())

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
