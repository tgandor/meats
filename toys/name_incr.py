#!/usr/bin/env python

import os
import re
import shutil
import sys


def increment_ints(s):
    return re.sub(r"\d+", lambda s: str(int(s.group()) + 1), s)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        fpp = increment_ints(f)
        if not os.path.exists(fpp):
            print("{} -> {}".format(f, fpp))
            shutil.copy(f, fpp)
