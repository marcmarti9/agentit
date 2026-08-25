"""Portable Agentit CLI entrypoint.

The CLI is an agent-facing mechanical surface. Semantic task understanding stays
with the active model. This module only dispatches explicit subcommands.
"""

from __future__ import annotations

import sys
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if args and args[0] == "verify":
        from router.verify_cli import main as verify_main

        return verify_main(args[1:])

    if args and args[0] == "bootstrap":
        from router.bootstrap import main as bootstrap_main

        return bootstrap_main(args[1:])

    from router.profiles import main as profiles_main

    return profiles_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
