"""Cheap project signals for project-aware token estimates and domain packs."""

from __future__ import annotations

from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".tox",
    "dist",
    "build",
    ".next",
    "coverage",
    ".agentit",
}


def collect_project_signals(project_root: Path | None) -> dict[str, Any]:
    """Return lightweight repo facts. Safe on missing/unreadable roots."""
    if project_root is None:
        return {"available": False, "basis": ["no_project_root"]}
    root = Path(project_root)
    try:
        if not root.is_dir() or root.is_symlink():
            return {"available": False, "basis": ["project_root_unusable"]}
    except OSError:
        return {"available": False, "basis": ["project_root_error"]}

    file_count = 0
    code_files = 0
    max_files = 4000
    extensions: dict[str, int] = {}
    markers: list[str] = []

    def note_marker(name: str, label: str) -> None:
        if (root / name).exists():
            markers.append(label)

    note_marker("package.json", "node")
    note_marker("tsconfig.json", "typescript")
    note_marker("pyproject.toml", "python")
    note_marker("requirements.txt", "python")
    note_marker("setup.cfg", "python")
    note_marker("pytest.ini", "python")
    note_marker("Cargo.toml", "rust")
    note_marker("go.mod", "go")
    note_marker("pubspec.yaml", "flutter")
    note_marker("supabase/config.toml", "supabase")
    note_marker("docker-compose.yml", "docker")
    note_marker("Dockerfile", "docker")
    note_marker(".github/workflows", "ci")

    try:
        for path in root.rglob("*"):
            if file_count >= max_files:
                break
            try:
                parts = set(path.parts)
                if parts & SKIP_DIRS:
                    continue
                if not path.is_file() or path.is_symlink():
                    continue
            except OSError:
                continue
            file_count += 1
            ext = path.suffix.lower()
            if ext:
                extensions[ext] = extensions.get(ext, 0) + 1
            if ext in {
                ".py",
                ".ts",
                ".tsx",
                ".js",
                ".jsx",
                ".go",
                ".rs",
                ".java",
                ".rb",
                ".php",
                ".dart",
                ".css",
                ".scss",
            }:
                code_files += 1
            if ext == ".py" and "python" not in markers:
                markers.append("python")
            if ext in {".ts", ".tsx"} and "typescript" not in markers:
                markers.append("typescript")
    except OSError:
        pass

    # Size bonus in "thousands of tokens" units used by route estimator.
    # Include docs weight lightly so doc-heavy harnesses are not always "tiny".
    weighted = code_files + min(file_count // 10, 40)
    if weighted >= 800 or code_files >= 500:
        size_bonus = 40
        size_class = "large"
    elif weighted >= 200 or code_files >= 120:
        size_bonus = 22
        size_class = "medium"
    elif weighted >= 40 or code_files >= 25:
        size_bonus = 10
        size_class = "small"
    else:
        size_bonus = 3
        size_class = "tiny"

    top_ext = sorted(extensions.items(), key=lambda item: (-item[1], item[0]))[:8]
    basis = [
        f"files_scanned={file_count}",
        f"code_files≈{code_files}",
        f"size_class={size_class}",
        f"markers={','.join(markers) or 'none'}",
    ]
    return {
        "available": True,
        "project_root": str(root.resolve()),
        "file_count_scanned": file_count,
        "code_file_count": code_files,
        "size_class": size_class,
        "size_bonus": size_bonus,
        "stack_markers": markers,
        "top_extensions": top_ext,
        "basis": basis,
    }
