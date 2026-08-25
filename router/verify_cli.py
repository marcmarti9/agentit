"""Dedicated public CLI for Agentit's signal-gated verification runtime.

Semantic task interpretation stays with the active AI. This CLI accepts only
explicit semantic signals selected by that AI plus mechanical project facts
that ``router.verify`` can detect without parsing the task text.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from router.verify import VerifyError, apply_verification, format_plan, plan_verification
except ImportError:  # direct execution from router/
    from verify import VerifyError, apply_verification, format_plan, plan_verification


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentit verify",
        description=(
            "Plan or run Agentit verification. Natural-language task text is receipt "
            "context only; semantic verification signals must be passed explicitly."
        ),
    )
    parser.add_argument(
        "task",
        nargs="*",
        help="Human-readable task summary retained in the verification receipt.",
    )
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--signal",
        action="append",
        default=[],
        metavar="ID",
        help=(
            "Explicit semantic signal chosen by the active AI, e.g. auth, api, "
            "frontend, postgres. Repeat for multiple signals."
        ),
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Execute runnable probes and persist a receipt. Default is plan-only.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
    )
    parser.add_argument(
        "--no-advisory",
        action="store_true",
        help="Exclude advisory probes from the plan.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    task_text = " ".join(args.task).strip()
    explicit_signals = [signal.strip().lower() for signal in args.signal if signal.strip()]

    # ``--repo-root`` is a deprecated compatibility flag retained for callers
    # from the pre-split CLI. Runtime code now resolves its own harness root;
    # semantic routing never depends on this value.
    _ = args.repo_root

    try:
        if args.apply:
            payload = apply_verification(
                args.project,
                task_text=task_text,
                explicit_signals=explicit_signals,
                include_advisory=not args.no_advisory,
            )
        else:
            payload = plan_verification(
                args.project,
                task_text=task_text,
                explicit_signals=explicit_signals,
                include_advisory=not args.no_advisory,
            )
    except VerifyError as exc:
        parser.error(str(exc))
        return 2

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(format_plan(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
