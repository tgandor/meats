#!/usr/bin/env python

"""
Based on: https://andrewpwheeler.wordpress.com/2015/12/28/using-python-to-grab-google-street-view-imagery/

Still worked at time of writing.
"""

import os
import sys

try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve

key = ''  # "&key=" + "" #got banned after ~100 requests with no key


def get_street(address, target_folder):
    base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
    my_url = base + address + key
    fi = address + ".jpg"
    urlretrieve(my_url, os.path.join(target_folder, fi))


for addr in sys.argv[1:]:
    get_street(addr, '.')
