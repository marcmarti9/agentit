#!/usr/bin/env python3
"""Keep Agentit-owned policy compatible with canonical vendored skill behavior."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise SystemExit(f"expected policy text not found in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> int:
    replace_once(
        ROOT / "agents" / "catalog.yaml",
        "  interview_batch_all_current_questions: true\n",
        "  interview_one_question_at_a_time: true\n",
    )
    replace_once(
        ROOT / "docs" / "AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md",
        "When several current material questions are known, batch them coherently. Follow up only when new evidence creates genuinely new decisions.",
        "When an interactive interview is actually needed, follow the canonical `interview-me` workflow: ask one focused question at a time, attach the agent's current best guess, and stop once the user's intent is explicitly confirmed. Non-interactive execution must still escalate unresolved material decisions rather than guessing.",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
