#!/usr/bin/env python

import argparse
import os
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--ascii', '-t', action='store_true')
args = parser.parse_args()

conn = sqlite3.connect(os.path.expanduser('~/usage.db'))
df = pd.read_sql_query("select * from df where mountpoint='/'", conn)
df.df_date = pd.to_datetime(df['df_date'])

if args.ascii:
    import asciiplotlib
    fig = asciiplotlib.figure()
    fig.plot(x=df['df_date'], y=df['used'], label='used', width=70, height=50)
    fig.show()
else:
    df.plot(x='df_date', y='used')
    plt.show()
