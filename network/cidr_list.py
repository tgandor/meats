#!/usr/bin/env python

import argparse
import ipaddress

parser = argparse.ArgumentParser()
parser.add_argument("cidr")
args = parser.parse_args()

net = ipaddress.IPv4Network(args.cidr, strict=False)
print(net)
for ip in net:
    print(ip)
