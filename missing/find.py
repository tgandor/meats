#!/usr/bin/env python

import os

for directory, _, files in os.walk("."):
    for f in files:
        print(os.path.join(directory, f))
