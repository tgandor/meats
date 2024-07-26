#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="Print positions of points distributed evenly on a line segment.")
parser.add_argument("length", type=float)
parser.add_argument("num_screws", type=int)
parser.add_argument("--round", "-r", type=int, help="decimal places to round")
parser.add_argument("--splay", "-s", type=int, help="make screw pairs split by this")

args = parser.parse_args()

w = args.length / args.num_screws
holes = [w / 2 + i * w for i in range(args.num_screws)]

if args.splay:
    r = args.splay / 2
    holes = [x for h in holes for x in (h-r, h+r)]

if args.round is not None:
    holes = [round(c, args.round) for c in holes]

print(holes)

