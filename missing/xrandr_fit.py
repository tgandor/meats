#!/usr/bin/env python

import os
import re
import sys

KEY = lambda x: -x[0]*x[1]

def get_resolutions(xrandr_output):
    devices = []
    resolutions = []
    names = []

    for line in xrandr_output.split('\n'):
        if line.find('connected') != -1:
            if resolutions:
                devices.append(sorted(resolutions, key=KEY))
                resolutions = []
            elif len(names):
                names.pop()
            names.append(line.split()[0])
            continue
        m = re.match('\s+(\d+)x(\d+)', line)
        if m:
            resolutions.append((
                int(m.group(1)),
                int(m.group(2)),
            ))

    if resolutions:
        devices.append(sorted(resolutions, key=KEY))

    return zip(names, devices)


def find_best_pairs(local, remote):
    results = []
    for local_device, local_resolutions in local:
        for remote_device, remote_resolutions in remote:
            for res in remote_resolutions:
                good = [res2 for res2 in local_resolutions
                        if res2[0] >= res[0] and res2[1] >= res[1]]
                # print good
                if len(good):
                    results.append((local_device, good[0], remote_device, res))
                    break
    return results


def print_devices(results):
    for name, resolutions in results:
        print name
        for res in resolutions:
            print '%4.2f MPix' % (res[0]*res[1]*1e-6,), res

if __name__ == '__main__':
    xrandr_output = os.popen('xrandr').read()

    show = False
    if len(sys.argv) == 1:
        print_devices(get_resolutions(xrandr_output))
    else:
        local = get_resolutions(xrandr_output)
        for arg in sys.argv[1:]:
            if arg == '-show':
                show = True
                continue

            if arg == '-':
                remote = get_resolutions(sys.stdin.read())
            else:
                remote = get_resolutions(open(arg).read())

            if show:
                print_devices(remote)
                show = False
                continue

            for best in find_best_pairs(local, remote):
                mpix = best[3][0] * best[3][1] / 1.0e6
                percent = 100.0 * (best[3][0] * best[3][1]) / (best[1][0] * best[1][1])
                print "On {2:6}: use {5:14} ({0:.2f} MPix, {1:.1f}%)".format(mpix, percent, *best)
                print "    rdesktop -g {0}x{1}".format(*best[3])
                print "    xrandr -s {0}x{1}".format(*best[3])
