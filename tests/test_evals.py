import json
import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


class DecisionContractEvaluationTests(unittest.TestCase):
    def test_representative_decision_contract_cases_pass(self):
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
        self.assertGreaterEqual(report["total"], 10)
        self.assertEqual(report["total"], report["passed"])
        self.assertEqual(0, report["failed"])
        self.assertIn("decision-contract invariants", report["scope"])
        self.assertIn("host LLM owns semantic classification", report["scope"])


if __name__ == "__main__":
    unittest.main()
