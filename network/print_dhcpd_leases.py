#!/usr/bin/env python

from isc_dhcp_leases import Lease, IscDhcpLeases

leases = IscDhcpLeases('/var/lib/dhcp/dhcpd.leases')
for lease in leases.get_current().values():
    print(lease)
