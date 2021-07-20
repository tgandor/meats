#!/usr/bin/env python

import argparse
import os

from PIL import Image
import matplotlib.pyplot as plt


def to_title(filename):
    name, _ = os.path.splitext(filename)
    name = os.path.basename(name)
    name = name.replace("_", " ")
    return name


parser = argparse.ArgumentParser()
parser.add_argument("image_files", nargs="+")
parser.add_argument("--scale", "-s", type=float, default=1)
parser.add_argument("--letters", "-l", action="store_true")
parser.add_argument("--verbose", "-v", action="store_true")
parser.add_argument("--output", "-o")
args = parser.parse_args()


N = len(args.image_files)
fig, axes = plt.subplots(1, N)
s = args.scale
fig.set_figheight(3 * s)
fig.set_figwidth(3 * N * s)

for i, filename in enumerate(args.image_files):
    axes[i].axis("off")
    v_img = Image.open(filename)
    axes[i].imshow(v_img)
    title = to_title(filename)
    if args.letters:
        title = chr(ord("A") + i) + ": " + title
    if args.verbose:
        print(title)
    axes[i].set_title(title, fontsize=10 * args.scale)

# bbox_inches='tight' is tight!
# fig.tight_layout()

if args.output:
    fig.savefig(args.output, bbox_inches="tight")
    if args.verbose:
        print('Saved output to:', args.output)

else:
    plt.show()
