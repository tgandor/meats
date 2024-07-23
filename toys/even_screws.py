#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="Print positions of points distributed evenly on a line segment.")
parser.add_argument("length", type=float)
parser.add_argument("num_screws", type=int)

args = parser.parse_args()

w = args.length / args.num_screws
print([w / 2 + i * w for i in range(args.num_screws)])

