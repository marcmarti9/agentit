#!/usr/bin/env python3
"""Run the checked-in router regression cases.

This evaluates deterministic routing fields only. It is not an agent-quality,
token-cost, or production-readiness benchmark.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from router.route import route_task  # noqa: E402


def load_cases(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise ValueError("evaluation cases must be a list of mappings")
    return payload


def evaluate_case(
    case: dict[str, Any], *, registry_path: Path, home: Path
) -> dict[str, Any]:
    result = route_task(
        case["prompt"],
        registry_path=registry_path,
        home=home,
    )
    expected = case["expected"]
    mismatches: dict[str, dict[str, Any]] = {}
    for field, expected_value in expected.items():
        if field == "routing_advice_contains":
            actual_value = result.get("routing_advice", [])
            passed = expected_value in actual_value
        else:
            actual_value = result.get(field)
            passed = actual_value == expected_value
        if not passed:
            mismatches[field] = {"expected": expected_value, "actual": actual_value}
    return {
        "id": case.get("id"),
        "passed": not mismatches,
        "mismatches": mismatches,
    }


def run(cases: list[dict[str, Any]], *, registry_path: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="agentit-eval-home-") as temporary_home:
        results = [
            evaluate_case(case, registry_path=registry_path, home=Path(temporary_home))
            for case in cases
        ]
    passed = sum(1 for result in results if result["passed"])
    return {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "results": results,
        "scope": "deterministic router regression cases only",
        "confidence_calibrated": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    parser.add_argument("--registry", type=Path, default=REPOSITORY / "registry.yaml")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    try:
        report = run(load_cases(args.cases), registry_path=args.registry)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            f"Router evals: {report['passed']}/{report['total']} passed "
            f"({report['failed']} failed)"
        )
        for result in report["results"]:
            marker = "PASS" if result["passed"] else "FAIL"
            print(f"{marker} {result['id']}")
    return 0 if report["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
