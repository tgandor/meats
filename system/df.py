#!/usr/bin/env python

from __future__ import print_function

import argparse
import datetime
import os
import shutil
import sqlite3
import sys
import time

# Filesystem     1M-blocks   Used Available Use% Mounted on
# udev                7900      0      7900   0% /dev
# tmpfs               1587      2      1586   1% /run
# ...


def open_database():
    labels_file = os.path.expanduser("~/usage.db")
    initialize = not os.path.exists(labels_file)
    conn = sqlite3.connect(labels_file)
    cursor = conn.cursor()
    # initialization
    if initialize:
        cursor.executescript(
            """
            create table df
            (
                id integer not null primary key autoincrement,
                filesystem varchar not null,
                size integer not null,
                used integer not null,
                available integer not null,
                use varchar not null,
                mountpoint varchar not null,
                df_date datetime not null
            );
            """
        )
    conn.text_factory = str  # which == unicode on Py3, and works!
    return conn, cursor


def normal_df():
    data = os.popen("df -m").read().split("\n")[1:]
    df_date = datetime.datetime.now()

    conn, cursor = open_database()

    for row in data:
        columns = row.split(None, 6)
        if len(columns) != 6:
            continue
        cursor.execute(
            "insert into df (filesystem, size, used, available, use, mountpoint, df_date)"
            " values (?,?,?,?,?,?,?)",
            columns + [df_date],
        )
    conn.commit()
    cursor.close()
    conn.close()


_DELTAS = {}


def windows_emulation():
    df_date = datetime.datetime.now()

    conn, cursor = open_database()
    print(time.strftime("%D %T"))
    for drive in enumerate_windows_drives():
        print(drive, end=" ")

        try:
            usage = shutil.disk_usage(drive)
        except FileNotFoundError:
            print(
                "Failed to get usage for",
                drive,
                "- a disconnected network drive? (FileNotFoundError)",
            )
            continue
        except PermissionError:
            print(
                "Failed to get usage for",
                drive,
                "- not ready USB storage? (PermissionError)",
            )
            continue

        print(
            "{:,} B = {:.1f}% used, {:,} B free".format(
                usage.used, usage.used * 100 / usage.total, usage.free
            )
        )

        delta = _DELTAS.get(drive)
        if delta:
            print("Delta: {:,} B".format(usage.used - delta))
        else:
            _DELTAS[drive] = usage.used

        cursor.execute(
            "insert into df (filesystem, size, used, available, use, mountpoint, df_date)"
            " values (?,?,?,?,?,?,?)",
            (
                drive,
                usage.total,
                usage.used,
                usage.free,
                usage.used / usage.total * 100,
                drive,
                df_date,
            ),
        )
    conn.commit()
    cursor.close()
    conn.close()


def enumerate_windows_drives():
    try:
        import win32api

        # print(repr(win32api.GetLogicalDriveStrings()))
        for drive in win32api.GetLogicalDriveStrings().split("\0"):
            if drive:
                yield drive
    except ImportError:
        print("Missing win32api", file=sys.stderr)
        import string

        for letter in string.ascii_uppercase:
            path = letter + ":\\"
            if os.path.exists(path):
                yield path


if __name__ == "__main__":
    if os.name == "nt":
        parser = argparse.ArgumentParser()
        parser.add_argument("--loop", "-l", action="store_true")
        parser.add_argument("--period", "-t", type=float, default=60)
        args = parser.parse_args()
        if args.loop:
            while True:
                windows_emulation()
                time.sleep(args.period)
        else:
            windows_emulation()
    else:
        normal_df()
