#!/usr/bin/env python

from __future__ import print_function

import os
import pip


def main():
    packages = [line.split("==")[0] for line in os.popen("pip list --format=freeze")]
    for i, package in enumerate(packages):
        # way slower, at least on windows:
        # os.system('pip show {}'.format(package))
        pip.main(["show", package])
        print(i, "-" * 70)


if __name__ == "__main__":
    main()
