
try:
    import colorama
    colorama.init()
except ImportError:
    pass

import sys

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green

for line in sys.stdin:
    line = line.rstrip()
    if line.startswith('-'):
        print(R+line+W)
    elif line.startswith('+'):
        print(G+line+W)
    else:
        print(line)

