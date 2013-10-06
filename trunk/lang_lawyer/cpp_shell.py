#!/usr/bin/env python

import subprocess
import os

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

headers = []
command = ['g++', '-o', 'cpp_shell_temp.exe']

while True:
    print 'c++>',
    try:
        line = raw_input()
    except EOFError:
        os.unlink('cpp_shell_temp.cpp')
        os.unlink('cpp_shell_temp.exe')
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
    open('cpp_shell_temp.cpp', 'w').write(code_template % context)
    if subprocess.call(command+['cpp_shell_temp.cpp']) == 0:
        subprocess.call('./cpp_shell_temp.exe')
