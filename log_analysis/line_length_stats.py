#!/usr/bin/env python

import argparse
import os
from collections import Counter
from pprint import pprint


def plot_counter_bar(counter):
    import matplotlib.pyplot as plt
    items, counts = zip(*sorted(counter.items()))
    x = range(len(counter))
    plt.bar(x, counts, align='center')
    plt.xticks(x, items)
    plt.show()


parser = argparse.ArgumentParser()
parser.add_argument('--text', '-t', action='store_true')
args = parser.parse_args()

stats = Counter()

for _, __, files, in os.walk('.'):
    stats.update([len(line) for file in files for line in open(file)])


if len(stats) == 0:
    print('No files.')
    exit()

pprint(sorted(stats.items()))

plot_counter_bar(stats)
