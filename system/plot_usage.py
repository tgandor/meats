#!/usr/bin/env python

import os
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt


conn = sqlite3.connect(os.path.expanduser('~/usage.db'))
df = pd.read_sql_query("select * from df where mountpoint='/'", conn)

df.plot(x='df_date', y='used')
plt.show()
