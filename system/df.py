#!/usr/bin/env python

import datetime
import os
import sqlite3


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
        cursor.executescript("""
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
""")
    conn.text_factory = str  # which == unicode on Py3, and works!
    return conn, cursor


data = os.popen('df -m').read().split('\n')[1:]
df_date = datetime.datetime.now()

conn, cursor = open_database()

for row in data:
    columns = row.split(None, 6)
    if len(columns) != 6:
        continue
    cursor.execute(
        'insert into df (filesystem, size, used, available, use, mountpoint, df_date) values (?,?,?,?,?,?,?)',
        columns + [df_date]
    )
conn.commit()
cursor.close()
conn.close()
