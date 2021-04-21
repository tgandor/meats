#!/usr/bin/env python

import argparse
import os
from collections import Counter
from pprint import pprint


def plot_counter_bar(counter):
    import matplotlib.pyplot as plt

    items, counts = zip(*sorted(counter.items()))
    x = range(len(counter))
    plt.bar(x, counts, align="center")
    plt.xticks(x, items)
    plt.show()


def gen_lines(root=".", verbose=False):
    for (
        path,
        _,
        files,
    ) in os.walk(root):
        for file in files:
            if verbose:
                print(path, file)
            try:
                with open(os.path.join(path, file)) as f:
                    for line in f:
                        yield line, file
            except:
                print("Error with {}/{}".format(path, file))


parser = argparse.ArgumentParser()
parser.add_argument("--max", "-m", action="store_true", help="find max")
parser.add_argument("--verbose", "-v", action="store_true")
parser.add_argument("root", type=str, nargs="?", default=".")

args = parser.parse_args()

stats = Counter()

stats.update(len(line) for line, _ in gen_lines(args.root))

if len(stats) == 0:
    print("No files.")
    exit()

pprint(sorted(stats.items()))

if args.max:
    print(max((len(line), line, file) for line, file in gen_lines(args.root)))

plot_counter_bar(stats)
