#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "sync-upstream-design-skills.sh is deprecated; syncing the complete canonical skill registry." >&2
exec "$ROOT/scripts/sync-upstream-skills.sh" "$@"
