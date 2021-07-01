#!/usr/bin/env python

import sys
import re

x = sys.argv[1]

if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", x):
    ip = [int(d) for d in x.split(".")]
elif re.fullmatch(r"(IP-)?[0-9a-f]{8}", x, re.IGNORECASE):
    if x.lower().startswith("ip-"):
        x = x[3:]
    ip = [int(x[i : i + 2], 16) for i in range(0, 8, 2)]
else:
    print(f"Argument not understood: {x}")
    exit()

print(".".join(str(d) for d in ip))
print("IP-" + "".join(f"{d:02x}" for d in ip))
