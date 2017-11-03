# for windows
# deprecated since 3.4:
# python -m tarfile -e file.tar[.gz|.bz2|.xz]

import sys
import tarfile

for f in sys.argv[1:]:
    tar = tarfile.open(f)
    tar.list(True)
    tar.extractall()
    tar.close()

