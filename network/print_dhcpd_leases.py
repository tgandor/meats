#!/usr/bin/env python

from __future__ import print_function

import argparse
import datetime
import inspect
import json

from isc_dhcp_leases import IscDhcpLeases


def lease_as_dict(lease):
    data = vars(lease)

    for key, val in data.items():
        if isinstance(val, datetime.datetime):
            data[key] = val.isoformat(' ')

    return data


def get_leases(leases, args):
    if not args.all:
        return leases.get_current()

    latest = {}
    for lease in leases.get():
        latest[lease.ethernet] = lease

    return latest


parser = argparse.ArgumentParser()
parser.add_argument('leases_file', nargs='?', default='/var/lib/dhcp/dhcpd.leases')
parser.add_argument('--json', action='store_true', help='output JSON format')
parser.add_argument('--all', action='store_true', help='include some expired leases (latest for any MAC)')

args = parser.parse_args()
leases = IscDhcpLeases(args.leases_file)
lease_data = get_leases(leases, args)

if args.json:
    data = {}
    for key, lease in lease_data.items():
        data[key] = lease_as_dict(lease)
    print(json.dumps(data, indent=2))
else:
    for lease in lease_data.values():
        print(lease, lease.sets.get('vendor-class-identifier', ''))
