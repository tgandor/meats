#!/usr/bin/env python

from __future__ import print_function

# Kudos to: https://stackoverflow.com/a/35853322/1338797

import sys

try:
    import dns.resolver
except ImportError:
    import os
    print('Missing dnspython')
    os.system('pip install dnspython')
    exit()


if __name__ == '__main__':
    name = sys.argv[1]

    myRes = dns.resolver.Resolver()
    myRes.nameservers = ['224.0.0.251']  # mdns multicast address
    myRes.port = 5353  # mdns port
    myRes.source_port=5353  # resolver port
    a = myRes.query(name, 'A')
    # print(a[0].to_text())
    print(name, a)
