"""User preferences and persistent agent memory management for Agentit.

Manages ~/.agentit/preferences.yaml with strict file permissions (0600).
Stores user coding preferences, preferred skills, auto-JIT profile rules, and auto-plan policy.
"""

from __future__ import annotations

import os
import sys
import yaml
from pathlib import Path
from typing import Any

PREFERENCES_DIR = Path.home() / ".agentit"
PREFERENCES_FILE = PREFERENCES_DIR / "preferences.yaml"

DEFAULT_PREFERENCES: dict[str, Any] = {
    "version": 1,
    "user_style_preferences": {
        "preferred_language": "es",
        "code_style": "clean_modular",
        "testing_framework": "pytest",
        "ui_styling": "vanilla_css_oklch",
    },
    "auto_jit_profiles": True,
    "auto_plan_mode": True,
    "preferred_skills": [
        "frontend-ui-engineering",
        "test-driven-development",
        "security-and-hardening",
    ],
    "project_history": {},
}


def load_preferences() -> dict[str, Any]:
    """Load user preferences from ~/.agentit/preferences.yaml or return defaults."""
    if not PREFERENCES_FILE.is_file():
        return dict(DEFAULT_PREFERENCES)
    try:
        content = PREFERENCES_FILE.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        if isinstance(data, dict):
            merged = dict(DEFAULT_PREFERENCES)
            merged.update(data)
            return merged
    except Exception:
        pass
    return dict(DEFAULT_PREFERENCES)


def save_preferences(data: dict[str, Any]) -> Path:
    """Save user preferences to ~/.agentit/preferences.yaml with 0600 permissions."""
    PREFERENCES_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(PREFERENCES_DIR, 0o700)
    
    content = yaml.safe_dump(data, default_flow_style=False, sort_keys=False)
    
    # Atomic write
    tmp_path = PREFERENCES_DIR / ".preferences.yaml.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        os.chmod(f.fileno(), 0o600)
        f.write(content)
        
    os.replace(tmp_path, PREFERENCES_FILE)
    return PREFERENCES_FILE


def get_preference(key: str, default: Any = None) -> Any:
    """Get a specific preference key."""
    prefs = load_preferences()
    return prefs.get(key, default)


def set_preference(key: str, value: Any) -> dict[str, Any]:
    """Set a specific preference key and save."""
    prefs = load_preferences()
    prefs[key] = value
    save_preferences(prefs)
    return prefs


def main() -> None:
    """CLI entrypoint for managing preferences."""
    args = sys.argv[1:]
    if not args or args[0] == "show":
        prefs = load_preferences()
        print(yaml.safe_dump(prefs, default_flow_style=False))
        return
    
    if args[0] == "get" and len(args) >= 2:
        key = args[1]
        prefs = load_preferences()
        print(yaml.safe_dump({key: prefs.get(key)}, default_flow_style=False))
        return
        
    if args[0] == "set" and len(args) >= 3:
        key, value = args[1], args[2]
        # Parse boolean or int values
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.isdigit():
            value = int(value)
        set_preference(key, value)
        print(f"Updated {key} = {value}")
        return

    print("Usage: python3 -m router.preferences [show|get <key>|set <key> <val>]")


if __name__ == "__main__":
    main()
