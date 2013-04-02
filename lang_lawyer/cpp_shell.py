#!/usr/bin/env python

import subprocess

code_template = """
#include <iostream>

using namespace std;

int main()
{
    %(main)s
    return 0;
}
"""

while True:
    print 'c++>',
    try:
        line = raw_input()
    except EOFError:
        print
        break
    context = {'main': 'cout << (%s) << endl;' % line}
    open('cpp_shell_temp.cpp', 'w').write(code_template % context)
    if subprocess.call(['g++', 'cpp_shell_temp.cpp']) == 0:
        subprocess.call('./a.out')
