#!/usr/bin/env python

import re
import sys

sys.stdout.write('; '.join(re.findall('\S+@\S+', sys.stdin.read()))+'\n')

