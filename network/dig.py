#!/usr/bin/env python

"""Query address using Future Processing DNSes."""

from __future__ import print_function

import argparse
import sys
import os


def ensure_resolver():
    try:
        import dns.resolver
    except ImportError:
        print('Missing dnspython')
        if sys.platform.startswith('linux'):
            if sys.version_info.major == 2:
                os.system('sudo apt-get install python-dnspython')
            else:
                os.system('sudo apt-get install python3-dnspython')
        else:
            print('pip install dnspython')
            os.system('pip install dnspython')
        exit()
    return dns.resolver

parser = argparse.ArgumentParser()
parser.add_argument('--ip', '-a', action='store_true', help='Only output IP address')
parser.add_argument('url', type=str, help='The name to look up')
args = parser.parse_args(sys.argv[1:])

conf = os.path.join(os.path.dirname(__file__), 'resolv.conf')

if os.path.exists(conf):
    res = ensure_resolver().Resolver(conf)
else:
    res = ensure_resolver().Resolver()

answers = res.query(args.url, 'A')

for rdata in answers:
    if args.ip:
        print(rdata)
    else:
        print(rdata, args.url)
 
