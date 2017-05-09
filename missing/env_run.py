import os
import sys
from collections import deque

args = deque(sys.argv[1:])
while True:
    if len(args) == 0:
        break
    arg = args.popleft()
    if '=' not in arg:
        args.appendleft(arg)
        break
    if arg == '--':
        break
    if '+=' in arg:
        name, add_value = arg.split('+=')
        if name in os.environ:
            value = ';'.join([elem for elem in os.environ[name].split(';') if elem.strip()] + [add_value])
        else:
            value = add_value
    else:
        name, value = arg.split('=')
    os.environ[name] = value
    print('SET {0}={1}'.format(name, value))

os.system(' '.join(args))
