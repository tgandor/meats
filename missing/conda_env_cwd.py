from __future__ import print_function
import os
import sys

if 'CONDA_PREFIX' not in os.environ:
    print('Not in a conda environment')
    exit()

target = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
target = os.path.abspath(target)

activate_d = os.path.join(os.environ['CONDA_PREFIX'], 'etc', 'conda', 'activate.d')

if not os.path.exists(activate_d):
    print('Creating:', activate_d)
    os.makedirs(activate_d)

hook = os.path.join(activate_d, 'setwd.bat')

if os.path.exists(hook):
    print('Already exists:', hook)
    with open(hook) as f:
        print(f.read())
    if input('replace? ') != 'y':
        exit()

template = """
@echo Opening {cwd}
@cd /D "{cwd}"
@pushd .
""".format(cwd=target)

print('Creating:', hook)

with open(hook, 'w') as f:
    f.write(template)
