#!/usr/bin/env python

import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("data1")
parser.add_argument("data2")
args = parser.parse_args()

df1 = pd.read_excel(args.data1)
df2 = pd.read_excel(args.data2)

print(df1.compare(df2))
