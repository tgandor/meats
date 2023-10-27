#!/usr/bin/env python

import argparse
import os
import re


parser = argparse.ArgumentParser()
parser.add_argument("folders", nargs="+")
args = parser.parse_args()

r_date = re.compile(r"(img_|vid_)?(\d{4}-?\d{2}-?\d{2})", re.IGNORECASE)

for folder in args.folders:
    files = os.listdir(folder)
    dates = [r_date.match(file).group(2) for file in files if r_date.match(file)]
    dates.sort(key=lambda x: x.replace("-", ""))
    if not dates:
        print("No dates found in", folder)
        continue
    date = dates[0]
    if len(date) == 8:
        date = "-".join((date[:4], date[4:6], date[6:]))
    target = date + "_" + folder
    print(folder, "->", target)
    os.rename(folder, target)
