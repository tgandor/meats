import socket
import struct
import sys

try:
    import dpkt, dpkt.dns
except ImportError:
    import os

    os.system('pip install dpkt')
    exit()

if __name__ == '__main__':
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5353
    MCAST_GRP = '224.0.0.251'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((UDP_IP, UDP_PORT))
        # join the multicast group
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        for host in sys.argv[1:]:
            # the string in the following statement is an empty query packet
            dns = dpkt.dns.DNS(b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01')
            dns.qd[0].name = host + ('' if host.endswith('.local') else '.local')
            sock.sendto(dns.pack(), (MCAST_GRP, UDP_PORT))

        sock.settimeout(5)

        for _ in range(100):
            try:
                m = sock.recvfrom(64 * 1024)
                # print('%r'%m[0], m[1])
                print('Packet from:', m[1])
                try:
                    dns = dpkt.dns.DNS(m[0])
                except dpkt.UnpackError:
                    print('ERROR UNPACKING RESPONSE: %r' % m[0])
                if len(dns.qd) > 0:
                    print(dns.__repr__(), dns.qd[0].name)
                if len(dns.an) > 0 and dns.an[0].type == dpkt.dns.DNS_A:
                    print('ANSWER:', dns.__repr__(), dns.an[0].name, socket.inet_ntoa(dns.an[0].rdata))
                else:
                    print('not understood: %r' % m[0])

            except socket.timeout:
                break
