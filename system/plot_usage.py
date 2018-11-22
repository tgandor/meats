#!/usr/bin/env python

import argparse
import datetime
import os
import sqlite3

import pandas as pd
from matplotlib import pyplot as plt


def fake_date(dt):
    dt = dt[0]
    day = 100 * dt.month + dt.day
    # day += 10000 * (dt.year % 100)
    fraction = (3600 * dt.hour + 60 * dt.minute  + dt.second) / float(24 * 3600)
    return day + fraction


parser = argparse.ArgumentParser()
parser.add_argument('--ascii', '-t', action='store_true')
parser.add_argument('--fake-date', '-d', action='store_true')
parser.add_argument('--mountpoint', '-m', default='/', help='mountpoint to show')
parser.add_argument('--days', '-D', type=int, help='number of last days to show')
parser.add_argument('--width', '-w', type=int, help='width of plot (--ascii only)', default=170)
parser.add_argument('--height', '-H', type=int, help='height of plot (--ascii only)', default=60)
args = parser.parse_args()

conn = sqlite3.connect(os.path.expanduser('~/usage.db'))
params = (args.mountpoint,)
query = 'select * from df where mountpoint=?'
if args.days:
    query += ' and df_date > ?'
    params += (datetime.datetime.now() - datetime.timedelta(days=args.days),)

df = pd.read_sql_query(query, conn, params=params)
df.df_date = pd.to_datetime(df['df_date'])

if args.ascii:
    if args.fake_date:
        df.df_date = df[['df_date']].apply(fake_date, axis=1)
        xlabel = 'day.fraction'
    else:
        df.df_date = df[['df_date']].apply((lambda x: int(x[0].timestamp())), axis=1)
        xlabel = 'timestamp'

    import asciiplotlib
    fig = asciiplotlib.figure()
    fig.plot(x=df['df_date'], y=df['used'], label='used MB', xlabel=xlabel, width=args.width, height=args.height)
    fig.show()
else:
    df.plot(x='df_date', y='used')
    plt.show()
