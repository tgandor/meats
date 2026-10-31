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


def parse_duration(duration):
    """Return a duration in seconds.

    Accepted formats are MM:SS, [H]H:MM:SS, and e.g. 1m31.833s or 46s.
    """

    def as_number(value):
        return float(value.replace(",", "."))

    clock = re.fullmatch(r"(?:(\d+):)?(\d{2}):(\d{2}(?:[.,]\d+)?)", duration)
    if clock:
        hours, minutes, seconds = clock.groups()
        total_minutes = int(minutes)
        seconds = as_number(seconds)
        if seconds >= 60 or (hours is not None and total_minutes >= 60):
            raise ValueError("minutes and seconds in a clock duration must be below 60")
        return (int(hours or 0) * 60 + total_minutes) * 60 + seconds

    units = re.fullmatch(r"(?:(\d+(?:[.,]\d+)?)m)?(?:(\d+(?:[.,]\d+)?)s)?", duration)
    if not units or not any(units.groups()):
        raise ValueError(
            "duration must be MM:SS, [H]H:MM:SS, or a value such as 1m31.833s"
        )
    minutes, seconds = units.groups()
    return as_number(minutes or "0") * 60 + as_number(seconds or "0")


def format_speed(bytes_per_second):
    """Format a byte rate using the units accepted by parse_human."""
    for suffix in "PTGMK":
        factor = FACTORS[suffix + "B"]
        if bytes_per_second >= factor:
            return f"{bytes_per_second / factor:.3g}{suffix}B/s"
    return f"{bytes_per_second:.3g}B/s"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("size", help="total size to download (e.g. 92M)")
    parser.add_argument(
        "speed_per_second",
        help=(
            "download speed (e.g. 2MB/s); with --reverse, a duration "
            "(MM:SS, [H]H:MM:SS, or e.g. 1m31.833s)"
        ),
    )
    parser.add_argument("--current", "-c", help="current progress (already downloaded)")
    parser.add_argument(
        "--reverse",
        "-r",
        action="store_true",
        help="calculate required speed from size and duration instead of ETA",
    )
    args = parser.parse_args()

    num_bytes = parse_human(args.size)
    if args.current:
        curr_bytes = parse_human(args.current)
        num_bytes -= curr_bytes
        print(f"Remaining to download: {num_bytes:,} bytes.")
    if args.reverse:
        duration = parse_duration(args.speed_per_second)
        if duration <= 0:
            parser.error("duration must be greater than zero")
        print(f"Required speed: {format_speed(num_bytes / duration)}")
        raise SystemExit(0)

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
