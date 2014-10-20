# for windows

import gzip
import os
import shutil
import sys

if sys.version_info[0] == 2:
    input = raw_input

for f in sys.argv[1:]:
    target_f = f+'.gz'
    if os.path.exists(target_f):
        if input('{0} :\n - file exists, overwrite (y/N)? '.format(target_f)) != 'y':
            continue
    input_ = open(f)
    output = gzip.open(target_f, 'wb')
    shutil.copyfileobj(input_, output)
    input_.close()
    output.close()
    print('{0} -> {1}'.format(f, target_f))
