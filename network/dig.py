#!/usr/bin/env python

"""Query address (possibly) using a custom resolv.conf file (custom DNSes)."""

from __future__ import print_function

import argparse
import sys
import os


def ensure_resolver():
    try:
        import dns.resolver
    except ImportError:
        print("Missing dnspython")
        if sys.platform.startswith("linux"):
            if sys.version_info.major == 2:
                if os.system("sudo apt-get install python-dnspython") != 0:
                    print("pip install dnspython")
                    os.system("pip install dnspython")
            else:
                if os.system("sudo apt-get install python3-dnspython") != 0:
                    print("pip install dnspython")
                    os.system("pip install dnspython")
        else:
            print("pip install dnspython")
            os.system("pip install dnspython")
        exit()
    return dns.resolver


parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-a", action="store_true", help="Only output IP address")
parser.add_argument(
    "--no-config",
    "-n",
    action="store_true",
    help="Don't use resolv.conf even if it exists.",
)
parser.add_argument(
    "--save",
    "-s",
    action="store_true",
    help="Save to /etc/hosts (needs writing access)",
)
parser.add_argument(
    "--reverse", "-r", action="store_true", help="Do a reverse DNS query"
)
parser.add_argument("url", type=str, help="The name to look up")
args = parser.parse_args(sys.argv[1:])

conf = os.path.join(os.path.dirname(__file__), "resolv.conf")

if os.path.exists(conf) and not args.no_config:
    res = ensure_resolver().Resolver(conf)
else:
    res = ensure_resolver().Resolver()

url = args.url
if url.startswith("http"):
    url = url.split("/")[2]

if args.reverse:
    import dns.reversename

    name = dns.reversename.from_address(url)
    answers = res.resolve(name, "PTR")
else:
    answers = res.resolve(url, "A")

for rdata in answers:
    if args.ip:
        print(rdata)
    else:
        print(rdata, url)

if args.save:
    current_config = open("/etc/hosts").read()
    address = str(answers[0])
    if address in current_config or url in current_config:
        print("Name or IP already configured in /etc/hosts")
        print(
            "\n".join(
                line
                for line in current_config.split("\n")
                if address in line or url in line
            )
        )
        exit(1)
    with open("/etc/hosts", "a") as hosts:
        hosts.write("\n{} {}\n".format(address, url))
        print("Host saved")
