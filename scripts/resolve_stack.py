#!/usr/bin/env python3
"""Resolve the active design-workflow stack adapter.

Resolution order:
    1. STACK env var
    2. .design-workflow.yaml `stack:` field
    3. Default: flutter

Prints the resolved value to stdout. Exits non-zero on unknown stack.

Usage:
    python3 scripts/resolve_stack.py
    STACK=nextjs-tailwind python3 scripts/resolve_stack.py
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

AVAILABLE = ("flutter", "nextjs-tailwind", "react-native")
DEFAULT = "flutter"
CONFIG_NAMES = (".design-workflow.yaml", ".design-workflow.yml", "config.example.yaml")


def _read_yaml_stack(path: Path) -> str | None:
    """Minimal stack-field reader. Avoids hard PyYAML dep when not installed."""
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(path.read_text())
        val = data.get("stack") if isinstance(data, dict) else None
        return val if isinstance(val, str) else None
    except ModuleNotFoundError:
        for line in path.read_text().splitlines():
            line = line.strip()
            if line.startswith("stack:"):
                value = line.split(":", 1)[1].strip().strip('"\'')
                if value and " " not in value and ":" not in value:
                    return value
        return None


def resolve(project_root: Path | None = None) -> str:
    env = os.environ.get("STACK", "").strip()
    if env:
        return env
    root = project_root or Path.cwd()
    for name in CONFIG_NAMES:
        cfg = root / name
        if cfg.exists():
            value = _read_yaml_stack(cfg)
            if value:
                return value
    return DEFAULT


def main() -> int:
    stack = resolve()
    if stack not in AVAILABLE:
        print(
            f"Error: adapter '{stack}' not found. "
            f"Available adapters: {', '.join(AVAILABLE)}.",
            file=sys.stderr,
        )
        print(
            "See docs/adapter-protocol.md §\"How to add a new adapter\" "
            "if you'd like to contribute one.",
            file=sys.stderr,
        )
        return 1
    print(stack)
    return 0


if __name__ == "__main__":
    sys.exit(main())
