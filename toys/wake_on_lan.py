#!/usr/bin/env python
# wol.py
# Found somewhere on the Internet

import socket
import struct

def wake_on_lan(macaddress, ipaddress):
    """ Switches on remote computers using WOL. """

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')
	macaddress = macaddress.upper()
 
    # Pad the synchronization stream.
    data = ''.join(['F'*12, macaddress * 20])

    # Split up the hex values and pack.
    send_data = ''.join([
        struct.pack('B', int(data[i:i+2], 16))
        for i in range(0, len(data), 2)  ])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if ipaddress:
        sock.sendto(send_data, (ipaddress, 7))
    else:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, ('<broadcast>', 7))
    
def usage():
    import sys
    print "Usage: %s MACADDRESS [IPADDRESS]" % sys.argv[0]

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        usage()
    elif len(sys.argv) == 2:
        wake_on_lan(sys.argv[1])
    elif len(sys.argv) == 3:
        wake_on_lan(sys.argv[1], sys.argv[2])
    else:
        print "Excess arguments:", sys.argv[3:]
        usage()
    
