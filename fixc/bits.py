#!/usr/bin/env python

import sys

def process(s):
    word = int(s, 16)
    bits = []
    idx = 0
    while word:
        if word & 1:
            bits.append(idx)
        idx += 1
        word >>= 1
    for idx in bits[::-1]:
        print("bit {} set".format(idx))


if len(sys.argv) > 1:
    for word in sys.argv[1:]:
        process(word)
else:
    while True:
        word = sys.stdin.readline().strip()
        if not word:
            break
        process(word)
