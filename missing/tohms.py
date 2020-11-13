#!/usr/bin/env python
from __future__ import print_function
import sys


def print_secs(secs):
    h, s = divmod(secs, 3600)
    m, s = divmod(s, 60)
    print("%d seconds - %02d:%02d:%02d" % (secs, h, m, s))


if len(sys.argv) != 2:
    print("Usage:")
    print("  %s [[H:]M:]S[.sss]      hours, minutes, seconds; M and S can be greater than 60" % sys.argv[0])
    print("                              examples: 10 - 10s, 2:65 - 3m5s, 641 - 10m41s")
    print("  %s <M>m<S.sss>s         <M> minutes <S.sss> seconds, <M> can be greater than 60" % sys.argv[0])
    print("                              examples: 0m1.000s, 234m57.234s")
    print("  %s -                    read time expression from standard input" % sys.argv[0])
    exit()

if sys.argv[1] == '-':
    data = sys.stdin.readline().strip()
else:
    data = sys.argv[1]

if data.endswith('s'):
    hms = data[:-1].split('m')
else:
    hms = data.split(':')

secs = float(hms[0])
for limb in hms[1:]:
    secs *= 60
    secs += float(limb.replace(',', '.'))

print_secs(secs)

if secs > 24 * 3600:
    days, rest = divmod(secs, 24 * 3600)
    print(days, 'days', end=' ')
    print_secs(rest)
    if days > 7:
        weeks, rdays = divmod(days, 7)
        print(weeks, 'weeks', rdays, 'days', end=' ')
        print_secs(rest)
        if weeks > 52:  # rough!
            years, rweeks = divmod(weeks, 52)
            print(years, 'years', rweeks, 'weeks', rdays, 'days', end=' ')
            print_secs(rest)
