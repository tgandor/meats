#!/usr/bin/env python

import argparse
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
args = parser.parse_args()

conn = sqlite3.connect(os.path.expanduser('~/usage.db'))
df = pd.read_sql_query("select * from df where mountpoint='/'", conn)
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
    fig.plot(x=df['df_date'], y=df['used'], label='used MB', xlabel=xlabel, width=170, height=60)
    fig.show()
else:
    df.plot(x='df_date', y='used')
    plt.show()
