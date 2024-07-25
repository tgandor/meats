#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="Print positions of circle centers distributed evenly on a line segment.")
parser.add_argument("length", type=float)
parser.add_argument("diameter", type=float)
parser.add_argument("num_circles", type=int, nargs="?", help="number of circles; <= length/diameter")
parser.add_argument("--round", "-r", type=int, help="decimal places to round")

args = parser.parse_args()

if args.num_circles is None:
    args.num_circles = int(args.length // args.diameter)
    print(f"Max num_circles = {args.num_circles}")
if args.num_circles * args.diameter > args.length:
    raise ValueError("Won't fit")

pad = (args.length - args.diameter * args.num_circles) / (args.num_circles + 1)
w = args.length / args.num_circles
r = args.diameter / 2
centers = [pad + r + i * (pad + 2 * r) for i in range(args.num_circles)]

if args.round is not None:
    centers = [round(c, args.round) for c in centers]

print(centers)
for c in centers:
    print((c-r, c+r))

