#!/usr/bin/env python

from argparse import ArgumentParser
from pathlib import Path
import shutil

LOCATIONS = [
    '~/.config/chromium/Default/Service Worker/CacheStorage/',
    '~/.config/google-chrome/Default/Service Worker/CacheStorage/',
]

def get_size(path: str) -> int:
    return sum(p.stat().st_size for p in Path(path).expanduser().rglob('*'))


parser = ArgumentParser()
parser.add_argument('--dry-run', '-n', action='store_true')
parser.add_argument('--exclude', '-x', nargs='+')
args = parser.parse_args()

total = 0
after = 0

for location in LOCATIONS:
    print(location)
    if any(x in location for x in args.exclude):
        print('Excluded.')
        continue
    size = get_size(location)
    total += size
    print("- before: {:,}".format(size))
    p = Path(location).expanduser()
    if not args.dry_run:
        for subdir in p.glob('*/'):
            shutil.rmtree(subdir)
    size = get_size(location)
    after += size
    print("- after:  {:,}".format(size))

print("Total deleted: {:,}".format(total - after))
