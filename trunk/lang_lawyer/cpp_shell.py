#!/usr/bin/env python

import subprocess
import os
import readline
import atexit

histfile = os.path.expanduser("~/.cpp_history")
try:
    readline.read_history_file(histfile)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

code_template = """
#include <iostream>
%(headers)s

using namespace std;

int main()
{
    %(main)s
    return 0;
}
"""

TMPEXE = './cpp_shell_temp.exe'
TMPCPP = 'cpp_shell_temp.cpp'

headers = []
command = ['g++', '-o', TMPEXE]

while True:
    try:
        line = raw_input('c++> ')
    except EOFError:
        if os.path.exists(TMPCPP):
            os.unlink(TMPCPP)
        if os.path.exists(TMPEXE):
            os.unlink(TMPEXE)
        print
        break

    if line.startswith('+inc'):
        if len(line.split()) > 1:
            headers.append(line.split()[1])
        print 'Headers:', headers
        continue

    if line.startswith('-inc'):
        if len(line.split()) > 1:
            try:
                headers.remove(line.split()[1])
            except ValueError:
                print "Error: no such header '%s'" % line.split()[1]
        print 'Headers:', headers
        continue

    if line.startswith('+opt '):
        if len(line.split()) > 1:
            command.append(line.split()[1])
        print 'Compile command:', ' '.join(command)
        continue

    if line.startswith('-opt '):
        if len(line.split()) > 1:
            try:
                command.remove(line.split()[1])
            except ValueError:
                print "Error: no such option '%s'" % line.split()[1]
        print 'Compile command:', ' '.join(command)
        continue

    context = {
            'main': 'cout << (%s) << endl;' % line,
            'headers': '\n'.join('#include <%s>' % h for h in headers)
    }
    open(TMPCPP, 'w').write(code_template % context)
    if subprocess.call(command+[TMPCPP]) == 0:
        subprocess.call(TMPEXE)
