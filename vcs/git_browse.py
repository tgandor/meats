#!/usr/bin/env python

import os
import webbrowser

origin = os.popen("git remote -vv").read().split()[1]
print(origin)
webbrowser.open(origin)
