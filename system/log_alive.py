#!/usr/bin/env python

import argparse
import datetime
import time

parser = argparse.ArgumentParser()
parser.add_argument("--interval", "-i", type=float, default=600)  # 10 min
parser.add_argument("--logfile", "-l", default="alive.log")
args = parser.parse_args()

with open(args.logfile, "w") as log:
    msg = "{} -- starting".format(datetime.datetime.now())
    log.write(msg + "\n")
    print(msg)

while True:
    time.sleep(args.interval)
    with open(args.logfile, "a") as log:
        msg = "{} -- alive".format(datetime.datetime.now())
        log.write(msg + "\n")
        print(msg)
