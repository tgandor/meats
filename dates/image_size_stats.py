#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

from collections import Counter
import argparse
import os
import datetime

JPG = ".jpg"
JPEGS = {JPG, ".jpeg"}

try:
    import piexif
except ImportError:
    print("Missing piexif")
    os.system("pip install piexif")
    exit()

try:
    import imagesize
except ImportError:
    print("Missing imagesize")
    os.system("pip install imagesize")
    exit()

parser = argparse.ArgumentParser()
parser.add_argument("directory", nargs="?", default=".")
parser.add_argument("--no-plot", "-n", action="store_true")
parser.add_argument(
    "--quantize", "-q", type=int, default=1, help="Truncate dimensions to multiples"
)
parser.add_argument(
    "--top", "-t", type=int, default=10, help="Number of most popular sizes to list"
)
parser.add_argument("--extension", "-x", default=".jpg")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

size_stats = Counter()
examples = {}
exif = 0
exif_mismatch = 0

start = datetime.datetime.now()

for path, directories, files in os.walk(args.directory):
    for basename in files:
        if basename.lower().endswith(args.extension):
            realname = os.path.join(path, basename)

            try:
                d = piexif.load(realname)

                try:
                    size = (
                        d["0th"][piexif.ImageIFD.ImageWidth],
                        d["0th"][piexif.ImageIFD.ImageLength],
                    )
                    exif += 1
                except KeyError:
                    # print('Error reading size from EXIF:', realname)
                    size = None
            except piexif.InvalidImageDataError:
                if args.extension in JPEGS:
                    print("Error reading EXIF (invalid file [type]?):", realname)
                size = None
            except Exception as e:
                print("Other error reading EXIF:", e, "in", realname)
                size = None

            size2 = imagesize.get(realname)

            if size is None:
                size = size2

            if size != size2:
                # imagesize seems to be right on the money
                exif_mismatch += 1
                print(
                    "Size differs for {}: {} vs {} ({})".format(
                        realname, size, size2, exif_mismatch
                    )
                )
                size = size2
            elif args.verbose:
                print(realname, "OK")

            if args.quantize > 1:
                size = tuple(x - x % args.quantize for x in size)

            size_stats[size] += 1
            if size not in examples:
                examples[size] = realname

total = sum(size_stats.values())

if total == 0:
    print("No images found. Sorry. Wall time:", datetime.datetime.now() - start)
    exit()

print(
    "Finished processing",
    total,
    "files,",
    exif,
    "had EXIF metadata, in",
    datetime.datetime.now() - start,
)

ordered_keys = sorted(size_stats.keys(), key=lambda x: (x[0] * x[1], x))

print(
    "Number of different sizes{}: {}".format(
        " (quantized)" if args.quantize > 1 else "", len(size_stats)
    )
)

# all sizes
for size in ordered_keys:
    count = size_stats[size]
    print(
        "{!r:12} {:4.2f} MPix, {:4d} files, {:5.1f} %, aspect: {:.2f}, example: {}".format(
            size,
            size[0] * size[1] / 1e6,
            count,
            100 * count / total,
            size[0] / size[1],
            examples[size],
        )
    )

if args.top > 0:
    print("Top sizes (up to {} most common):".format(args.top))
    top_total = 0

    for size, count in size_stats.most_common(args.top):
        print(
            "{!r:12} {:4.2f} MPix, {:4d} files, {:5.1f} %, aspect: {:.2f}, example: {}".format(
                size,
                size[0] * size[1] / 1e6,
                count,
                100 * count / total,
                size[0] / size[1],
                examples[size],
            )
        )
        top_total += count

    print(
        "These combined make up {:.1f} % ({:,} / {:,}) of all files.".format(
            100 * top_total / total, top_total, total
        )
    )

if args.no_plot:
    exit()

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Missing matplotlib. Plot will not be shown.\nConsider:")
    print("pip install matplotlib")
    exit()


def transpose(tuples):
    return list(zip(*tuples))


w, h, n = transpose(
    [(width, height, count) for (width, height), count in size_stats.items()]
)

plt.scatter(w, h, s=n)

# keep the visible aspect ratio -
# sorry, this doesn't work:
# plt.axis('equal')  # https://stackoverflow.com/a/2935000/1338797
# but this, does.
plt.axis("scaled")  # https://stackoverflow.com/a/35994245/1338797

# reset axes min to 0:
plt.xlim(left=0)
plt.ylim(bottom=0)

plt.show()
