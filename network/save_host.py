#!/usr/bin/env python

"""Add (if needed) the ip + host to /etc/hosts."""

from __future__ import print_function
import sys

current_config = open('/etc/hosts').read()
address = sys.argv[1]
hostname = sys.argv[2]
if address in current_config or hostname in current_config:
    print(address, hostname, '- name or IP already configured in /etc/hosts:')
    print('\n'.join(line for line in current_config.split('\n') if address in line or hostname in line))
    exit(1)
with open('/etc/hosts', 'a') as hosts:
    hosts.write('\n{} {}\n'.format(address, hostname))
    print(address, hostname, '- host saved')
