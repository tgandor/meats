import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('regex')
parser.add_argument('--only', '-o', action='store_true')
args = parser.parse_args()

rx = re.compile(args.regex)

for line in sys.stdin:
    match = rx.search(line)
    if match:
        print(match.group() if args.only else line.rstrip())

