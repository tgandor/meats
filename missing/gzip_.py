# for windows

import gzip
import shutil
import sys

for f in sys.argv[1:]:
	input_ = open(f)
	output = gzip.open(f+'.gz', 'wb')
	shutil.copyfileobj(input_, output)
	input_.close()
	output.close()
	print('{0} -> {1}'.format(f, f+'.gz'))
