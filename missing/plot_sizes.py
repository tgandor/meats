#!/usr/bin/env python

from __future__ import print_function

import glob
import sys
import os
from itertools import chain
import numpy as np
import matplotlib.pyplot as plt

files = list(chain.from_iterable(map(glob.glob, sys.argv[1:])))
files.sort(key=lambda x: (os.path.basename(x), len(x), x))

plt.rcdefaults()
fig, ax = plt.subplots()

y_pos = np.arange(len(files))
size = [os.path.getsize(x) for x in files]


ax.barh(y_pos, size, align='center', color='green', ecolor='black')
ax.set_yticks(y_pos)
ax.set_yticklabels(files)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('File sizes in B')
ax.set_title('Sizes plot')

plt.show()

