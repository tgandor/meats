#!/usr/bin/env python

import os


def main():
    cmd = 'git config --unset user.name'
    print(cmd)
    os.system(cmd)
    cmd = 'git config --unset user.email'
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
