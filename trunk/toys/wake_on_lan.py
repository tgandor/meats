#!/usr/bin/env python
# wol.py
# Found somewhere on the Internet

import socket
import struct

def wake_on_lan(macaddress):
    """ Switches on remote computers using WOL. """

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')
 
    # Pad the synchronization stream.
    data = ''.join(['F'*12, macaddress * 20])

    # Split up the hex values and pack.
    send_data = ''.join([
        struct.pack('B', int(data[i:i+2], 16))
        for i in range(0, len(data), 2)  ])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 7))
    

if __name__ == '__main__':
    import sys
    # In case of exceptions - let them come
    wake_on_lan(sys.argv[1])
    
