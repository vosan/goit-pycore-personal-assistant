"""
Handles reading and writing JSON files for persistent storage.

Responsibilities:
- Read data from JSON files (contacts.json, notes.json).
- Write updated data to disk.
- Ensure files are created if they don't exist.
- Keep all file paths and disk operations isolated here.
"""

import json
from pathlib import Path
from typing import Any


def _to_path(path: str | Path) -> Path:
    """Normalize input to a Path."""
    return Path(path)


def _ensure_parent_dir(path: Path) -> None:
    """Ensure the parent directory exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def load_data(file_path: str | Path, default: Any) -> Any:
    """Load JSON data from file_path. If the file does not exist, create it by default and return default.
    If the file is invalid JSON, return default (without overwriting).
    """
    path = _to_path(file_path)
    if not path.exists():
        _ensure_parent_dir(path)
        save_data(path, default)
        return default

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Return default without altering the file
        return default


def save_data(file_path: str | Path, data: Any) -> None:
    """Write JSON data to file_path. Creates parent directories if needed."""
    path = _to_path(file_path)
    _ensure_parent_dir(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
