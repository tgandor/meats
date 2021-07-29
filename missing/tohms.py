#!/usr/bin/env python
from __future__ import print_function
import re
import sys


def print_secs(secs):
    h, s = divmod(secs, 3600)
    m, s = divmod(s, 60)
    print("%d seconds - %02d:%02d:%02d" % (secs, h, m, s))


if len(sys.argv) < 2:
    print("Usage:")
    print("  %s [[H:]M:]S[.sss]" % sys.argv[0])
    print("      hours, minutes, seconds; M and S can be greater than 60")
    print("      examples: 10 - 10s, 2:65 - 3m5s, 641 - 10m41s")
    print("  %s [[<D>d]<H>h]<M>m<S.sss>s" % sys.argv[0])
    print("      <M> minutes <S.sss> seconds, <M> can be greater than 60")
    print("      examples: 0m1.000s, 234m57.234s")
    print("  %s - read time expression from standard input" % sys.argv[0])
    exit()

for data in sys.argv[1:]:
    if data == "-":
        data = sys.stdin.readline().strip()

    # for real - you should use the 'dateparser' library
    # with one minor nuisance: 2d 3h 5m will be 2 days, 3 hours plus 5 months

    m = re.search(
        r"(?:(?P<days>\d+)\s*d\s*)?"
        r"(?:(?P<hours>\d+)\s*h\s*)?"
        r"(?P<mins>\d+)\s*m\s*"
        r"(?:(?P<secs>\d+)(?:[,.]\d+)?\s*s)?",
        data,
    )
    if m:
        gd = m.groupdict()
        hms = [0, 0, 0]
        if gd["days"]:
            hms[0] += 24 * int(gd["days"])
        if gd["hours"]:
            hms[0] += int(gd["hours"])
        hms[1] = int(gd["mins"])
        if gd["secs"]:
            hms[2] += int(gd["secs"])
        # print(gd, hms)
        hms = [str(x) for x in hms]
    elif data.endswith("s"):
        hms = data[:-1].split("m")
        if "h" in hms[0]:
            hms = hms[0].split("h") + [hms[1]]
    else:
        hms = data.split(":")

    secs = float(hms[0].replace(",", "."))
    for limb in hms[1:]:
        secs *= 60
        secs += float(limb.replace(",", "."))

    print_secs(secs)

    if secs > 24 * 3600:
        days, rest = divmod(secs, 24 * 3600)
        print(days, "days", end=" ")
        print_secs(rest)
        if days > 7:
            weeks, rdays = divmod(days, 7)
            print(weeks, "weeks", rdays, "days", end=" ")
            print_secs(rest)
            if weeks > 52:  # rough!
                years, rweeks = divmod(weeks, 52)
                print(years, "years", rweeks, "weeks", rdays, "days", end=" ")
                print_secs(rest)
