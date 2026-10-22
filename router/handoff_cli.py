"""Explicit private handoff commands; no implicit transport or tool execution."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agentit continuity",
        description="Verified private handoff between machines.",
        epilog="Existing state commands also remain available: status, init, checkpoint NAME, link REMOTE [KEY], sync and unlink. Use --project PATH; sync conflict resolution requires --resolve local|remote --apply. See docs/PROJECT_CONTINUITY.md.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    handoff = commands.add_parser("handoff", help="Plan or create a private verified handoff directory.")
    handoff.add_argument("--project", type=Path, default=Path.cwd())
    handoff.add_argument("--output", type=Path, required=True)
    handoff.add_argument("--profile", action="append", default=[])
    handoff.add_argument("--skill", action="append", default=[])
    handoff.add_argument("--artifact", action="append", default=[], help="Explicit project-relative evidence file; never a directory.")
    handoff.add_argument("--apply", action="store_true", help="Write the reviewed private package; default is preview.")
    for command in ("resume", "inspect"):
        selected = commands.add_parser(command, help="Check project/code/skills/artifacts before any state restoration.")
        selected.add_argument("handoff", type=Path)
        selected.add_argument("--project", type=Path, default=Path.cwd())
        if command == "resume":
            selected.add_argument("--apply", action="store_true")
            selected.add_argument("--replace-state", action="store_true", help="Explicitly replace differing local state with a private backup.")
    args = parser.parse_args(argv)
    try:
        from router.handoff import prepare_handoff, resume_handoff
        from router.continuity import ContinuityError
        if args.command == "handoff":
            result = prepare_handoff(
                args.project, args.output, profile_ids=args.profile, skill_ids=args.skill,
                artifact_paths=args.artifact, apply=args.apply,
            )
        else:
            result = resume_handoff(
                args.project, args.handoff, apply=getattr(args, "apply", False),
                replace_state=getattr(args, "replace_state", False),
            )
    except (ContinuityError, OSError, ValueError) as exc:
        parser.exit(2, f"Handoff blocked: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("ready") else 2


if __name__ == "__main__":
    raise SystemExit(main())
