#!/usr/bin/env python

"""
After running Tesseract on a bunch of (e.g.) PNM-s, we get a bunch of TXT-s.
Aside from minor typos or letter repetitions from bad print, it fea-
tures annoying word breaks, which are re-
tained from the original typesetting.

They even sometimes cross page boun-

1
^L
daries, possibly splitting paragraphs (especially with gib-
berish like page numbers).

2
^L
"""

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--singles', '-pl', help='carry over single letters (PL typography)')
args = parser.parse_args()

PARAGRAPH  = ''
output = []
carry = None

for f in args.files:
    # print(f)
    lines = open(f).read().split('\n')
    N = len(lines)
    for i, line in enumerate(lines):
        if i in (N-1, N-2, N-3, N-4) and len(line) < 5:
            continue

        if carry:
            line = carry + line
            carry = None

        if line.endswith('-'):
            words = line.split()
            carry = words[-1][:-1]
            line = ' '.join(words[:-1])

        if args.singles:
            # Not too great, actually. For full success I'd need to put
            # NBSP-s inside the lines. Probably this should then check
            # if it's (.lower()) in 'aiouwz'
            words = line.split()
            while len(words) > 2 and len(words[-1]) == 1:
                word = words.pop()
                if carry:
                    carry = word + '\u00A0' + carry
                else:
                    carry = word + '\u00A0'
            line = ' '.join(words)

        print(line)
