import json
import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


class RouterEvaluationTests(unittest.TestCase):
    def test_representative_router_cases_pass(self):
        completed = subprocess.run(
            [sys.executable, str(REPOSITORY / "evals" / "run.py"), "--json"],
            cwd=REPOSITORY,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(9, report["total"])
        self.assertEqual(9, report["passed"])
        self.assertEqual(0, report["failed"])
        self.assertFalse(report["confidence_calibrated"])


if __name__ == "__main__":
    unittest.main()
