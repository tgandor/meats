#!/usr/bin/env python

import subprocess
import webbrowser
from urllib.parse import urlparse

origin = subprocess.check_output(["git", "remote", "-vv"], stderr=subprocess.STDOUT).decode().split()[1]
origin = origin.replace(".git", "")
print(origin)

if origin.startswith("http"):
    # remove HTTP credentials if present
    parsed_url = urlparse(origin)
    origin = f"{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}"
    print(origin)

if origin.startswith("git@"):
    origin = origin.replace(":", "/")
    origin = origin.replace("git@", "https://")
    print(origin)

webbrowser.open(origin)
