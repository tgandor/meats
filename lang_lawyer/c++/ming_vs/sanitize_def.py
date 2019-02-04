# THIS IS DEFUNCT - dlltool produces bad .def-s
# With too much stuff wheh --export-all-symbol[s]
# and empty .def without.

import sys
import os
import shutil

arch = 'x64'
good = ['EXPORTS', 'max_div']
bad = ['DATA']

def test(lines):
    open(out_file, 'w').write(''.join(lines))

    if os.system('lib /machine:%s /def:%s' % (arch, out_file)) != 0:
        print 'LIB failed'
        return False
    if os.system('cl /Ferev_eng_prog.exe prog.cpp %s' % (out_file.replace('.def', '.lib'))) != 0:
        print 'CL failed'
        return False
    return True

in_file, out_file = sys.argv[1], sys.argv[2]

lines = [_.replace('@ ', '@')
    for _ in open(in_file).readlines()
    if not any(b in _ for b in bad)
        and not _.startswith('_')
    ]

print ''.join(lines)

initial = [line for line in lines if any(g in line for g in good)]
print initial

if test(initial):
    print 'Test OK'

shutil.copy('lib_orig.dll', out_file.replace('.def', '.dll'))
