#!/usr/bin/env python

import argparse
import hashlib
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "--sha256", "-S", action="store_true", help="Use SHA256 instead of MD5"
)
parser.add_argument("--sha", "-s", action="store_true", help="Use SHA-1 instead of MD5")
parser.add_argument(
    "--verbose",
    "-v",
    action="count",
    default=0,
    help="Print subdirectory hashes; repeat to include file hashes",
)
parser.add_argument("dirs", nargs="*", type=Path, help="Directories to process")
args = parser.parse_args()


def _get_hasher():
    if args.sha256:
        return hashlib.sha256()
    elif args.sha:
        return hashlib.sha1()
    else:
        return hashlib.md5()


def md5dir(dirname: Path) -> bytes:
    hasher = _get_hasher()
    if not dirname.is_dir():
        raise ValueError(f"{dirname} is not a directory")
    for file in sorted(path for path in dirname.iterdir() if path.is_file()):
        file_hasher = _get_hasher()
        with file.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                file_hasher.update(chunk)
        if args.verbose >= 2:
            print(f"{file_hasher.hexdigest()}  {file}")
        hasher.update(file_hasher.digest())
    for subdir in sorted(path for path in dirname.iterdir() if path.is_dir()):
        dir_hash = md5dir(subdir)
        if args.verbose >= 1:
            print(f"{dir_hash.hex()}  {subdir}")
        hasher.update(dir_hash)
    return hasher.digest()


if args.dirs:
    for dirname in args.dirs:
        print(f"{md5dir(dirname).hex()}  {dirname}")
else:
    print(f"{md5dir(Path('.')).hex()}  .")
