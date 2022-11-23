#!/usr/bin/env python

import argparse
import glob
import re
import time

import requests

parser = argparse.ArgumentParser()
parser.add_argument("--get", "-g", help="prefix for sending the value via GET")
parser.add_argument("--sleep", "-s", type=float, help="sleep between reads", default=60)
args = parser.parse_args()

data_files = glob.glob("/sys/bus/w1/devices/28-*/w1_slave")
if not data_files:
    print("No files like: /sys/bus/w1/devices/28-*/w1_slave")
    print("Ensure all connected, and w1-gpio w1-therm loaded.")
    exit()

if len(data_files) > 1:
    print("Too many matches:")
    print(data_files)
    exit()

data_file = data_files[0]

while True:
    with open(data_file) as dtf:
        data = dtf.read()

    temp = re.search(r"t=(\d+)", data).group(1)
    print(time.strftime("%Y-%m-%d %H:%M ") + temp)

    if args.get:
        requests.get(args.get + temp)

    time.sleep(args.sleep)
