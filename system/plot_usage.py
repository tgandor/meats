#!/usr/bin/env python

import argparse
import datetime
import os
import sqlite3

import pandas as pd


def fake_date(dt):
    dt = dt[0]
    day = 100 * dt.month + dt.day
    # day += 10000 * (dt.year % 100)
    fraction = (3600 * dt.hour + 60 * dt.minute + dt.second) / float(24 * 3600)
    return day + fraction


parser = argparse.ArgumentParser()
parser.add_argument("--ascii", "-t", action="store_true")
parser.add_argument("--column", "-c", default="available")
parser.add_argument("--used", "-u", action="store_true", help="show 'used' column")
parser.add_argument("--fake-date", "-d", action="store_true")
parser.add_argument(
    "--mountpoint",
    "-m",
    default=("C:\\" if os.name == "nt" else "/",),
    help="mountpoint to show",
    nargs="+",
)
parser.add_argument(
    "--absolute", "-a", action="store_true", help="Y axis from 0 to size"
)
parser.add_argument("--style", default="-", help="matplotlib plotting style")
parser.add_argument("--list-mountpoints", "-l", action="store_true")
parser.add_argument("--days", "-D", type=int, help="number of last days to show")
parser.add_argument(
    "--width", "-w", type=int, help="width of plot (--ascii only)", default=170
)
parser.add_argument(
    "--height", "-H", type=int, help="height of plot (--ascii only)", default=60
)
parser.add_argument("--debug", "-v", action="store_true")
args = parser.parse_args()
if args.used:
    args.column = "used"

conn = sqlite3.connect(os.path.expanduser("~/usage.db"))
mpts = pd.read_sql_query("select distinct mountpoint from df", conn)

if args.list_mountpoints:
    for row in mpts["mountpoint"].sort_values():
        print(row)
    conn.close()
    exit()

known_mpts = set(mpts["mountpoint"])
chosen_mpts = []
for mp in args.mountpoint:
    if mp in known_mpts:
        chosen_mpts.append(mp)
        continue
    if mp.endswith("/") and mp[:-1] in known_mpts:
        chosen_mpts.append(mp[:-1])
        continue
    print("Ignoring mountpoint:", mp)

if not chosen_mpts:
    print("No known mountpoints found.")
    exit()

params = ()
query = "select * from df where mountpoint in ({})".format(
    ", ".join(f"'{mp}'" for mp in chosen_mpts)
)

if args.days:
    query += " and df_date > ?"
    params += (datetime.datetime.now() - datetime.timedelta(days=args.days),)

if args.debug:
    print(query, params)

df = pd.read_sql_query(query, conn, params=params)
df.df_date = pd.to_datetime(df["df_date"])

if args.ascii:
    import asciiplotlib

    if args.fake_date:
        df.df_date = df[["df_date"]].apply(fake_date, axis=1)
        xlabel = "day.fraction"
    else:
        df.df_date = df[["df_date"]].apply((lambda x: int(x[0].timestamp())), axis=1)
        xlabel = "timestamp"

    kwargs = dict(label="used GB", xlabel=xlabel, width=args.width, height=args.height)

    if args.absolute:
        kwargs["ylim"] = (0, df["size"].max() / 1024)

    fig = asciiplotlib.figure()
    fig.plot(x=df["df_date"], y=df["used"] / 1024, **kwargs)
    fig.show()
else:
    from matplotlib import pyplot as plt

    # df.set_index("df_date")[args.column].plot(style=args.style)
    pivot = df.pivot_table(index="df_date", columns="mountpoint", values=args.column)
    pivot.plot(style=args.style)
    plt.title(f"{args.column} on: {', '.join(chosen_mpts)}")
    if args.absolute:
        # 'size' is a bad column name in Pandas. df.size returns int, df['size'] - Series
        plt.ylim(bottom=0, top=df["size"].max())
    plt.show()
