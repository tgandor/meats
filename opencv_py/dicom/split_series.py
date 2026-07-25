#!/usr/bin/env python3
"""Copy or move DICOM files into per-SeriesInstanceUID directories."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

try:
    import pydicom
except ImportError as exc:  # pragma: no cover
    raise SystemExit("pydicom is required: pip install pydicom") from exc


def iter_dicom_files(root: Path):
    return sorted(
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() == ".dcm"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src", nargs="?", default=".", help="Directory to scan (default: current directory)")
    parser.add_argument("-d", "--dest", default=".", help="Destination root (default: current directory)")
    parser.add_argument("--move", action="store_true", help="Move files instead of copying them")
    args = parser.parse_args()

    src = Path(args.src).expanduser().resolve()
    dest_root = Path(args.dest).expanduser().resolve()
    dest_root.mkdir(parents=True, exist_ok=True)

    files = iter_dicom_files(src)
    if not files:
        print(f"No .dcm files found under {src}")
        return

    for path in files:
        ds = pydicom.dcmread(path, stop_before_pixels=True)
        series_uid = getattr(ds, "SeriesInstanceUID", None)
        if not series_uid:
            print(f"Skipping {path}: missing SeriesInstanceUID")
            continue

        target_dir = dest_root / str(series_uid)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / path.name

        if args.move:
            shutil.move(str(path), str(target_path))
        else:
            shutil.copy2(path, target_path)

        print(f"{'Moved' if args.move else 'Copied'} {path} -> {target_path}")


if __name__ == "__main__":
    main()
