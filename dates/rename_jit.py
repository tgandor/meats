#!/usr/bin/env python3

import argparse
import signal
import subprocess
import sys
import time
from pathlib import Path


RUNNING = True


def sigint_handler(signum, frame):
    global RUNNING
    RUNNING = False


def is_open(path: Path) -> bool:
    """
    Devuelve True si algún proceso tiene abierto el archivo.
    """
    try:
        result = subprocess.run(
            ["lsof", "--", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("ERROR: lsof no está instalado.", file=sys.stderr)
        sys.exit(1)


def next_name(path: Path) -> Path:
    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    n = 1
    while True:
        candidate = parent / f"{stem}_{n:03d}{suffix}"
        if not candidate.exists():
            return candidate
        n += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, sigint_handler)

    watched = Path(args.filename)

    print(f"Vigilando: {watched}")

    while RUNNING:
        try:
            if watched.exists():
                if not is_open(watched):
                    target = next_name(watched)

                    try:
                        watched.rename(target)
                        print(f"{watched.name} -> {target.name}")
                    except OSError as e:
                        print(f"Error renombrando: {e}")

            time.sleep(0.2)

        except KeyboardInterrupt:
            break

    print("\nFinalizado.")


if __name__ == "__main__":
    main()
