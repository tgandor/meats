#!/usr/bin/env python3
"""Install dotfile-style files into the current user's home directory.

Each positional argument is expected to be a file whose basename starts with
"_". The script copies it to "$HOME/" with the leading underscore replaced by
".". Existing targets are not overwritten.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def install_file(source: Path, destination_dir: Path) -> bool:
    if not source.is_file():
        print(f"FAIL: source not a file: {source}", file=sys.stderr)
        return False

    basename = source.name
    if not basename.startswith("_"):
        print(f"FAIL: expected basename to start with '_': {source}", file=sys.stderr)
        return False

    target_name = "." + basename[1:]
    destination = destination_dir / target_name

    if destination.exists():
        print(f"FAIL: target already exists: {destination}")
        return False

    try:
        shutil.copy2(source, destination)
    except OSError as exc:
        print(f"FAIL: could not copy {source} -> {destination}: {exc}", file=sys.stderr)
        return False

    print(f"OK: installed {source} -> {destination}")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {Path(sys.argv[0]).name} <file> [<file> ...]", file=sys.stderr)
        return 1

    home_dir = Path(os.environ.get("HOME") or os.path.expanduser("~"))
    if not home_dir.exists():
        print(f"FAIL: home directory does not exist: {home_dir}", file=sys.stderr)
        return 1

    success = True
    for arg in sys.argv[1:]:
        source = Path(arg)
        if not install_file(source, home_dir):
            success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
