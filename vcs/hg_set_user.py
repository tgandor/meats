#!/usr/bin/env python

import os
import sys


def main():
    status = os.system('hg config ui.username')

    if status == 0:
        print('Username already configured')
        return

    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
        target_dir = os.getcwd()
    else:
        source_dir = target_dir = os.getcwd()

    os.chdir(source_dir)
    last_commit = os.popen("hg log -l 1").readlines()
    author_line = next(line for line in last_commit if line.startswith('user:'))
    author = ' '.join(author_line.split()[1:])

    os.chdir(target_dir)
    config_line = '\n[ui]\nusername = {}\n'.format(author)
    print('Appending to .hg/hgrc:', config_line)

    with open('.hg/hgrc', 'a') as config:
        config.write(config_line)


if __name__ == '__main__':
    main()
