import os
import sys

if len(sys.argv) not in (1, 3):
    print('Usage: {0} [variable_name value]')
    exit()

if len(sys.argv) == 3:
    name, value = sys.argv[1:3]
else:
    name, value = 'myVariable', 'value'

print('Setting {0} to {1}'.format(name, value))
os.environ[name] = value

if sys.platform == 'win32':
    os.system('set {}'.format(name))
else:
    os.system('echo {0} == ${0}'.format(name))

