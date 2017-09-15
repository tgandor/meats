import argparse
import socket
import struct
import sys

try:
    import dpkt  # , dpkt.dns
except ImportError:
    import os
    os.system('pip install dpkt')
    exit()

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('names', nargs='+')

if __name__ == '__main__':
    args = parser.parse_args()
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5353
    MCAST_GRP = '224.0.0.251'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((UDP_IP, UDP_PORT))
        # join the multicast group
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        missing = set()
        for host in args.names:
            full_name = host + ('' if host.endswith('.local') else '.local')
            missing.add(full_name.lower())
            # the string in the following statement is an empty query packet
            dns = dpkt.dns.DNS(b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01')
            dns.qd[0].name = full_name
            sock.sendto(dns.pack(), (MCAST_GRP, UDP_PORT))

        sock.settimeout(5)

        for _ in range(100):
            try:
                m = sock.recvfrom(64 * 1024)
                # print('%r'%m[0], m[1])

                if args.verbose:
                    print('Packet from:', m[1])

                try:
                    dns = dpkt.dns.DNS(m[0])
                except dpkt.UnpackError:
                    print('ERROR UNPACKING RESPONSE: %r' % m[0])
                if len(dns.qd) > 0 and args.verbose:
                    print(dns.__repr__(), dns.qd[0].name)
                if len(dns.an) > 0 and dns.an[0].type == dpkt.dns.DNS_A:
                    if args.verbose:
                        print(dns.__repr__())
                    name = dns.an[0].name.lower()

                    if args.verbose or name in missing:
                        print('ANSWER:', name, socket.inet_ntoa(dns.an[0].rdata))

                    if name in missing:
                        missing.remove(name)
                        if len(missing) == 0:
                            if args.verbose:
                                print('Answers found, exiting.')
                            exit()
                elif args.verbose:
                    print('not understood: %r' % m[0])

            except socket.timeout:
                break
