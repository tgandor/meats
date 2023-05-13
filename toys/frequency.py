#!/usr/bin/env python

import time


def go():
    print("Keep pressing <Enter> or enter something to quit.")

    last_hit = time.time()
    line = ""
    lagavg = 0

    while line == "":
        line = input()
        hit = time.time()
        delay = hit - last_hit
        lagavg = (4 * lagavg + delay) / 5
        print(
            "%6.2f ms, %3.2f Hz (FPS), pulse %2.1f (RPM) | last 5 avg: %.1f ms %.1f Hz %.1f bpm"
            % (
                delay * 1000,
                1 / delay,
                60 / delay,
                lagavg * 1000,
                1 / lagavg,
                60 / lagavg,
            )
        )
        last_hit = hit

    print("Bye!")


go()
