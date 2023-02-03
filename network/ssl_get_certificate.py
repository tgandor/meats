#!/usr/bin/env python

# Based on excellent:
# https://stackoverflow.com/a/53556522/1338797

import argparse
import ssl
import socket
import json
from datetime import datetime
import OpenSSL


def get_certificate(host, port=443, timeout=10):
    context = ssl.create_default_context()
    conn = socket.create_connection((host, port))
    sock = context.wrap_socket(conn, server_hostname=host)
    sock.settimeout(timeout)
    try:
        der_cert = sock.getpeercert(True)
    finally:
        sock.close()
    return ssl.DER_cert_to_PEM_cert(der_cert)


def reformat_date(raw):
    return datetime.strptime(raw.decode(), "%Y%m%d%H%M%SZ").strftime("%Y-%m-%d")


parser = argparse.ArgumentParser()
parser.add_argument("hostname")
parser.add_argument("port", type=int, nargs="?", default=443)
parser.add_argument("--details", "-v", action="store_true")
args = parser.parse_args()

certificate = get_certificate(args.hostname, args.port)
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

