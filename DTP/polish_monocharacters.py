#!/usr/bin/env python

import re
import sys


def polish_monocharacters(text):
    phase1 = re.sub(r'\b([iwzoua]) (\w|\(|\\)', r'\1~\2', text, flags=re.IGNORECASE)
    phase2 = re.sub(r'~([iwzoua]) (\w|\(|\\)', r'~\1~\2', phase1)
    return phase2


def _main():
    data = sys.stdin.read()
    result = polish_monocharacters(data)
    sys.stdout.write(result)


if __name__ == '__main__':
    _main()
