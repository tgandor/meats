#!/usr/bin/env python

import time
import fcntl
import os
import signal
import sys

"""
Listen to filesystem events - modified, deleted or created files within a directory.
There is no information about what exactly happened - only a signal that it happened.
"""

watched_directory = sys.argv[1] if len(sys.argv) > 1 else "/sys/class/power_supply/BAT0"


def handler(signal_code, frame):
    print("Directory %s modified" % (watched_directory,))
    # reload signal
    signal.signal(signal.SIGIO, handler)


def main():
    signal.signal(signal.SIGIO, handler)
    fd = os.open(watched_directory, os.O_RDONLY)
    fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
    fcntl.fcntl(fd, fcntl.F_NOTIFY,
                fcntl.DN_MODIFY |  # file was changed (not just touched)
                fcntl.DN_CREATE |  # signal about file creation
                fcntl.DN_DELETE |  # signal about file deletion
                fcntl.DN_MULTISHOT)  # keep notifying after first

    while True:
        if '-v' in sys.argv:
            print("Nothing happens...")
        time.sleep(5)

if __name__ == '__main__':
    main()
