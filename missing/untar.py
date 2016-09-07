# for windows

import sys
import tarfile

if sys.version_info[0] == 2:
    input = raw_input


for f in sys.argv[1:]:
    tar = tarfile.open(f)
    tar.list(True)
    tar.extractall()

