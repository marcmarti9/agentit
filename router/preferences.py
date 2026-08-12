"""User preferences and persistent agent memory management for Agentit.

Manages ~/.agentit/preferences.yaml with strict file permissions (0600).
Supports nested dotted key access (e.g. user_style_preferences.ui_styling).
"""

from __future__ import annotations

import os
import sys
import tempfile
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
        "response_style": "terse",
    },
    "auto_jit_profiles": True,
    "auto_plan_mode": True,
    # Soft preference only — does not force multi-agent. Values: low|medium|high|max
    "parallelism_preference": "medium",
    "local_models": {
        "enabled": False,
        "endpoints": [],
        # Example endpoint:
        # {"id": "local-coding", "base_url": "http://127.0.0.1:11434/v1",
        #  "model": "qwen2.5-coder", "tier": "coding", "tools": True, "context_tokens": 32768}
    },
    "preferred_skills": [
        "test-driven-development",
        "security-and-hardening",
        "mcp-tooling-fit",
    ],
    "project_history": {},
}


def _get_nested(data: dict[str, Any], dotted_key: str, default: Any = None) -> Any:
    """Traverse nested dictionaries using dot notation."""
    parts = dotted_key.split(".")
    current: Any = data
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def _set_nested(data: dict[str, Any], dotted_key: str, value: Any) -> None:
    """Set a nested dictionary value using dot notation, creating sub-dicts as needed."""
    parts = dotted_key.split(".")
    current = data
    for part in parts[:-1]:
        child = current.get(part)
        if not isinstance(child, dict):
            child = {}
            current[part] = child
        current = child
    current[parts[-1]] = value


def load_preferences(preferences_path: Path | None = None) -> dict[str, Any]:
    """Load user preferences from path or ~/.agentit/preferences.yaml or return defaults."""
    target = Path(preferences_path) if preferences_path is not None else PREFERENCES_FILE
    if not target.is_file() or target.is_symlink():
        return dict(DEFAULT_PREFERENCES)
    try:
        content = target.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        if isinstance(data, dict):
            merged = dict(DEFAULT_PREFERENCES)
            for k, v in data.items():
                if isinstance(v, dict) and isinstance(merged.get(k), dict):
                    merged[k] = dict(merged[k])
                    merged[k].update(v)
                else:
                    merged[k] = v
            return merged
    except Exception:
        pass
    return dict(DEFAULT_PREFERENCES)


def save_preferences(data: dict[str, Any], preferences_path: Path | None = None) -> Path:
    """Save user preferences securely with 0600 permissions using mkstemp atomic write."""
    target = Path(preferences_path) if preferences_path is not None else PREFERENCES_FILE
    parent = target.parent
    parent.mkdir(parents=True, exist_ok=True)
    os.chmod(parent, 0o700)

    content = yaml.safe_dump(data, default_flow_style=False, sort_keys=False)

    fd, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.tmp-", dir=parent, text=True)
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(fd)
        os.replace(temporary_path, target)
    finally:
        temporary_path.unlink(missing_ok=True)

    return target


def get_preference(key: str, default: Any = None, preferences_path: Path | None = None) -> Any:
    """Get a specific nested preference key using dot notation."""
    prefs = load_preferences(preferences_path)
    return _get_nested(prefs, key, default)


def set_preference(key: str, value: Any, preferences_path: Path | None = None) -> dict[str, Any]:
    """Set a specific nested preference key using dot notation and save."""
    prefs = load_preferences(preferences_path)
    _set_nested(prefs, key, value)
    save_preferences(prefs, preferences_path)
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
        val = get_preference(key)
        print(yaml.safe_dump({key: val}, default_flow_style=False))
        return

    if args[0] == "set" and len(args) >= 3:
        key, value_str = args[1], args[2]
        value: Any = value_str
        if value_str.lower() == "true":
            value = True
        elif value_str.lower() == "false":
            value = False
        elif value_str.isdigit():
            value = int(value)
        set_preference(key, value)
        print(f"Updated {key} = {value}")
        return

    print("Usage: python3 -m router.preferences [show|get <key>|set <key> <val>]")


if __name__ == "__main__":
    main()
