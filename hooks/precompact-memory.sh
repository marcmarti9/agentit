#!/usr/bin/env bash
# Compatibility no-op for previously installed PreCompact hooks.
# Never launch a paid/unrestricted model with the transcript, persist raw chats,
# or overwrite native MEMORY.md automatically. The active authorized agent can
# maintain a bounded .agentit/STATE.md through long-horizon-recovery instead.
set -euo pipefail
cat >/dev/null
exit 0
