#!/usr/bin/env python

import argparse
import os
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('--text', '-t', action='store_true')
args = parser.parse_args()

stats = Counter()

for _, __, files, in os.walk('.'):
    # print([(filename, os.path.splitext(filename)[0][-1]) for filename in files])
    stats.update([os.path.splitext(filename)[0][-1] for filename in files])


def plot_dict_bar(dictionary):
    # https://stackoverflow.com/questions/16010869/python-plot-a-bar-using-matplotlib-using-a-dictionary
    import matplotlib.pyplot as plt
    plt.bar(range(len(dictionary)), list(dictionary.values()), align='center')
    plt.xticks(range(len(dictionary)), list(dictionary.keys()))
    plt.show()


def plot_counter_bar(counter):
    import matplotlib.pyplot as plt
    items, counts = zip(*counter.most_common())
    x = range(len(counter))
    plt.bar(x, counts, align='center')
    plt.xticks(x, items)
    plt.show()


def plot_counter_console(counter):
    tops = counter.most_common()
    norm = tops[0][1]
    maxlen = max(len(key) for key in counter.keys())
    total = sum(counter.values())
    format = '{:%ds} {} ({}, {:.2f}%%)' % maxlen
    for item, count in tops:
        print(format.format(item, '=' * (100 * count // norm) or '.', count, 100. * count / total))


if len(stats) == 0:
    print('No files.')
    exit()

if args.text:
    plot_counter_console(stats)
    exit()

try:
    plot_counter_bar(stats)
except ImportError:
    plot_counter_console(stats)

