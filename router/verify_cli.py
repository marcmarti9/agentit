"""Dedicated public CLI for Agentit's signal-gated verification runtime.

Semantic task interpretation stays with the active AI. This CLI accepts only
explicit semantic signals and reference decisions selected by that AI plus
mechanical project facts that ``router.verify`` can detect without parsing the
task text.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from router.verify import (
        VALID_REFERENCE_MODES,
        VerifyError,
        apply_verification,
        format_plan,
        plan_verification,
    )
except ImportError:  # direct execution from router/
    from verify import (  # type: ignore
        VALID_REFERENCE_MODES,
        VerifyError,
        apply_verification,
        format_plan,
        plan_verification,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentit verify",
        description=(
            "Plan or run Agentit verification. Natural-language task text is receipt "
            "context only; semantic verification signals/reference mode must be passed explicitly."
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
        "--reference-mode",
        choices=tuple(sorted(VALID_REFERENCE_MODES)),
        default="none",
        help=(
            "Explicit reference decision from TASK_DECISION: none, catalog, live, or mixed. "
            "The CLI never infers this from task text."
        ),
    )
    parser.add_argument(
        "--reference-source",
        action="append",
        default=[],
        metavar="ID_OR_URL",
        help="Reference pack/source ID or live URL actually selected/inspected. Repeat as needed.",
    )
    parser.add_argument(
        "--reference-evidence",
        action="append",
        default=[],
        metavar="TEXT",
        help=(
            "Compact evidence of what was actually inspected/verified and how it affected the work. "
            "Required by --apply when reference-mode is not none."
        ),
    )
    parser.add_argument(
        "--reference-provenance",
        default=None,
        metavar="PATH_OR_CITATIONS",
        help="Ledger path, citation record, or equivalent provenance output.",
    )
    parser.add_argument(
        "--reference-provenance-required",
        action="store_true",
        help="Require provenance output before a passing apply receipt.",
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
        common = {
            "task_text": task_text,
            "explicit_signals": explicit_signals,
            "include_advisory": not args.no_advisory,
            "reference_mode": args.reference_mode,
            "reference_sources": args.reference_source,
            "reference_provenance_required": args.reference_provenance_required,
        }
        if args.apply:
            payload = apply_verification(
                args.project,
                **common,
                reference_evidence=args.reference_evidence,
                reference_provenance=args.reference_provenance,
            )
        else:
            if args.reference_evidence or args.reference_provenance:
                parser.error(
                    "--reference-evidence/--reference-provenance are apply-time evidence; use --apply"
                )
            payload = plan_verification(args.project, **common)
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
