from __future__ import annotations

import unittest

from loop_runtime import (
    LoopRuntimeError,
    loop_receipt,
    new_loop,
    record_attempt,
    validate_loop,
    validate_loop_receipt,
)


class LoopRuntimeTests(unittest.TestCase):
    def test_success_requires_evidence_and_verifier_result(self):
        loop = new_loop(goal="Build page", verifier="pytest -q", stop_condition="tests pass")
        with self.assertRaises(LoopRuntimeError):
            record_attempt(loop, passed=True, strategy="implement", evidence="")
        with self.assertRaises(LoopRuntimeError):
            record_attempt(loop, passed=True, strategy="implement", evidence="pytest failed", verifier_exit_code=1)

    def test_default_budget_allows_one_retry_then_escalates(self):
        loop = new_loop(goal="Fix bug", verifier="pytest -q", stop_condition="target test passes")
        loop = record_attempt(loop, passed=False, strategy="first hypothesis", evidence="exit 1: assertion failed", verifier_exit_code=1)
        self.assertEqual("retryable", loop["status"])
        loop = record_attempt(loop, passed=False, strategy="second hypothesis", evidence="exit 1: different failure", verifier_exit_code=1)
        self.assertEqual("escalated", loop["status"])
        self.assertEqual(2, len(loop["attempts"]))

    def test_retry_needs_fresh_evidence_or_strategy(self):
        loop = new_loop(goal="Fix bug", verifier="pytest -q", stop_condition="target test passes")
        loop = record_attempt(loop, passed=False, strategy="same", evidence="same", verifier_exit_code=1)
        with self.assertRaises(LoopRuntimeError):
            record_attempt(loop, passed=False, strategy="same", evidence="same", verifier_exit_code=1)

    def test_contract_tampering_is_rejected(self):
        loop = new_loop(goal="Original", verifier="pytest -q", stop_condition="tests pass")
        loop["contract"]["goal"] = "Tampered"
        with self.assertRaises(LoopRuntimeError):
            validate_loop(loop)

    def test_passed_receipt_is_hash_checked(self):
        loop = new_loop(goal="Ship change", verifier="python -m unittest", stop_condition="suite passes")
        loop = record_attempt(loop, passed=True, strategy="targeted implementation", evidence="Ran 10 tests: OK", verifier_exit_code=0, artifacts=["diff.patch"])
        receipt = loop_receipt(loop)
        validate_loop_receipt(receipt)
        self.assertEqual("passed", receipt["status"])
        receipt["artifacts"] = ["tampered"]
        with self.assertRaises(LoopRuntimeError):
            validate_loop_receipt(receipt)

    def test_non_passed_receipt_cannot_unlock_downstream_work(self):
        loop = new_loop(goal="Try change", verifier="pytest -q", stop_condition="tests pass", max_attempts=1)
        loop = record_attempt(loop, passed=False, strategy="attempt", evidence="exit 1", verifier_exit_code=1)
        receipt = loop_receipt(loop)
        with self.assertRaises(LoopRuntimeError):
            validate_loop_receipt(receipt, require_passed=True)


if __name__ == "__main__":
    unittest.main()
