#!/usr/bin/env python

import argparse
import datetime
import re

FACTORS = {suffix: 1024 ** (i + 1) for i, suffix in enumerate("KMGTP")}
# no generator possible: dict size changed during iteration
FACTORS.update([(k.lower(), v) for k, v in FACTORS.items()])
# enable speed specification in e.g. Mb(its)/s
bytes = [(k + "B", v) for k, v in FACTORS.items()]
bits = [(k + "b", v // 8) for k, v in FACTORS.items()]
FACTORS.update(bytes + bits)
FACTORS[None] = 1
HUMAN = r"(\d+)?([.,]\d*)?([kmgtp]?b?)$"


def parse_human(size):
    """Return number of bytes in

    >>> parse_human('12')
    12
    >>> parse_human('1k')
    1024
    """

    # special cases:
    if size.lower().startswith("usb2"):
        return 27 * FACTORS["M"]
    if size.lower().startswith("usb3"):
        return 125 * FACTORS["M"]

    # normal parsing
    m = re.match(HUMAN, size, re.IGNORECASE)
    assert m, f"size must match {HUMAN}"
    # print(m, m.groups())
    whole, frac, unit = m.groups()

    result = int(whole) if whole else 0
    if frac:
        frac = frac.replace(",", ".")
        result += float(frac) if frac != "." else 0
    if not frac and not whole:
        result = 1
    if unit:
        result *= FACTORS[unit]

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("size")
    parser.add_argument("speed_per_second")
    parser.add_argument("--current", "-c", help="current progress (already downloaded)")
    args = parser.parse_args()

    num_bytes = parse_human(args.size)
    if args.current:
        curr_bytes = parse_human(args.current)
        num_bytes -= curr_bytes
        print(f"Remaining to download: {num_bytes:,} bytes.")
    bauds = parse_human(args.speed_per_second)

    seconds = num_bytes / bauds
    print(
        "ETA: {:.1f} seconds:\n=    {}".format(
            seconds, datetime.timedelta(seconds=seconds)
        )
    )
    print(
        "ETD: {}".format(datetime.datetime.now() + datetime.timedelta(seconds=seconds))
    )
