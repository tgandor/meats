# for windows

import sys
import tarfile

for f in sys.argv[1:]:
    tar = tarfile.open(f)
    tar.list(True)
    tar.extractall()

