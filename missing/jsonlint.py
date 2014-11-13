#!/usr/bin/env python

import json
import sys

input_json = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
sys.stdout.write(json.dumps(json.loads(input_json), indent=2))
