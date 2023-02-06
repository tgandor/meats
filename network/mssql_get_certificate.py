#!/usr/bin/env python

import argparse
import json
import socket
import ssl
import struct
import sys
from time import sleep
from datetime import datetime

# Source: https://gist.github.com/lnattrass/a4a91dbf439fc1719d69f7865c1b1791

# Standard "HELLO" message for TDS
# fmt: off
prelogin_msg = bytearray([
    0x12, 0x01, 0x00, 0x2f, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x1a, 0x00, 0x06, 0x01, 0x00, 0x20,
    0x00, 0x01, 0x02, 0x00, 0x21, 0x00, 0x01, 0x03, 0x00, 0x22, 0x00, 0x04, 0x04, 0x00, 0x26, 0x00,
    0x01, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
])
# fmt: on

# Prep Header function
def prep_header(data):
    data_len = len(data)
    prelogin_head = bytearray([0x12, 0x01])
    header_len = 8
    total_len = header_len + data_len
    data_head = prelogin_head + total_len.to_bytes(2, "big")
    data_head += bytearray([0x00, 0x00, 0x01, 0x00])
    return data_head + data


def read_header(data):
    if len(data) != 8:
        raise ValueError("prelogin header is > 8-bytes", data)

    format = ">bbhhbb"
    sct = struct.Struct(format)
    unpacked = sct.unpack(data)
    return {
        "type": unpacked[0],
        "status": unpacked[1],
        "length": unpacked[2],
        "channel": unpacked[3],
        "packet": unpacked[4],
        "window": unpacked[5],
    }


tdspbuf = bytearray()


def recv_tdspacket(sock):
    global tdspbuf
    tdspacket = tdspbuf
    header = {}

    for i in range(0, 5):
        tdspacket += sock.recv(4096)
        print("\n# get_tdspacket: {}, tdspacket len: {} ".format(i, len(tdspacket)))
        if len(tdspacket) >= 8:
            header = read_header(tdspacket[:8])
            print("# Header: ", header)
            if len(tdspacket) >= header["length"]:
                tdspbuf = tdspacket[header["length"] :]
                print("# Remaining tdspbuf length: {}\n".format(len(tdspbuf)))
                return header, tdspacket[8 : header["length"]]

        sleep(0.05)


def reformat_date(raw):
    return datetime.strptime(raw.decode(), "%Y%m%d%H%M%SZ").strftime("%Y-%m-%d")


def cert_info(certificate):
    try:
        import OpenSSL
    except ImportError:
        print("WARNING: Please install pyOpenSSL for parsed information.")
        return False

    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

    result = {
        "subject": dict(map(bytes.decode, x) for x in x509.get_subject().get_components()),
        "issuer": dict(map(bytes.decode, x) for x in x509.get_issuer().get_components()),
        "serialNumber": x509.get_serial_number(),
        "version": x509.get_version(),
        "notBefore": reformat_date(x509.get_notBefore()),
        "notAfter": reformat_date(x509.get_notAfter()),
    }

    extensions = (x509.get_extension(i) for i in range(x509.get_extension_count()))
    extension_data = {e.get_short_name().decode(): str(e) for e in extensions}
    if args.details:
        result.update(extension_data)

    try:
        print(json.dumps(result, indent=2))
    except TypeError as e:
        print(e)
        print(result)

    return True


def save_cert_info(name_base, certificate):
    import OpenSSL
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

    result = {
        "subject": dict(map(bytes.decode, x) for x in x509.get_subject().get_components()),
        "issuer": dict(map(bytes.decode, x) for x in x509.get_issuer().get_components()),
        "serialNumber": x509.get_serial_number(),
        "version": x509.get_version(),
        "notBefore": reformat_date(x509.get_notBefore()),
        "notAfter": reformat_date(x509.get_notAfter()),
    }

    extensions = (x509.get_extension(i) for i in range(x509.get_extension_count()))
    extension_data = {e.get_short_name().decode(): str(e) for e in extensions}
    result.update(extension_data)

    try:
        with open(f"{name_base}.json", w) as jsf:
            print(json.dumps(result, indent=2), file=jsf)
        print(f"Saved info to: {name_base}.json")
    except TypeError as e:
        print(e)
        print(result)


parser = argparse.ArgumentParser()
parser.add_argument("hostname")
parser.add_argument("port", type=int, nargs="?", default=1433)
parser.add_argument("--details", "-v", action="store_true")
args = parser.parse_args()

hostname = args.hostname
port = args.port

# Setup SSL
if hasattr(ssl, "PROTOCOL_TLS"):
    sslProto = ssl.PROTOCOL_TLS
else:
    sslProto = ssl.PROTOCOL_SSLv23

sslctx = ssl.SSLContext(sslProto)
sslctx.check_hostname = False
tls_in_buf = ssl.MemoryBIO()
tls_out_buf = ssl.MemoryBIO()

# Create the SSLObj connected to the tls_in_buf and tls_out_buf
tlssock = sslctx.wrap_bio(tls_in_buf, tls_out_buf)

# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(0)
s.settimeout(1)

# Connect to the SQL Server
s.connect((hostname, port))

# Send the first TDS PRELOGIN message
s.send(prelogin_msg)

# Get the response and ignore. We will try to negotiate encryption anyway.
header, data = recv_tdspacket(s)
while header["status"] == 0:
    header, ext_data = recv_tdspacket(s)
    data += ext_data


print("# Starting TLS handshake loop..")
# Craft the packet
for i in range(0, 5):
    try:
        tlssock.do_handshake()
        print("# Handshake completed, dumping certificates")
        peercert = ssl.DER_cert_to_PEM_cert(tlssock.getpeercert(True))
        if not cert_info(peercert):
            print(peercert)
        else:
            save_cert_info(hostname, peercert)
        with open(f"{hostname}.pem", "w") as pem:
            print(peercert, file=pem)
        print(f"Certificate saved to: {hostname}.pem")
        sys.exit(0)
    except ssl.SSLWantReadError as err:
        # TLS wants to keep shaking hands, but because we're controlling the R/W buffers it throws an exception
        print("# Shaking ({}/5)".format(i))

    tls_data = tls_out_buf.read()
    s.sendall(prep_header(tls_data))
    # TDS Packets can be split over two frames, each with their own headers.
    # We have to concat these for TLS to handle nego properly
    header, data = recv_tdspacket(s)
    while header["status"] == 0:
        header, ext_data = recv_tdspacket(s)
        data += ext_data

    tls_in_buf.write(data)

print("# Handshake did not complete / exiting")
