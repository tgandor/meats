#!/usr/bin/env python

import argparse
import os

from cryptography import x509
from cryptography.hazmat.primitives.serialization.pkcs12 import load_pkcs12

parser = argparse.ArgumentParser()
parser.add_argument("pfx_file")
parser.add_argument("password")
args = parser.parse_args()

password = (
    open(args.password, "rb").read()
    if os.path.exists(args.password)
    else args.password.encode()
)


with open(args.pfx_file, "rb") as f:
    pfx_data = f.read()

password = (
    open(args.password, "rb").read()
    if os.path.exists(args.password)
    else args.password.encode()
)

pfx = load_pkcs12(pfx_data, password)
cert_parsed = pfx.cert.certificate

cn = cert_parsed.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
expiry_date = cert_parsed.not_valid_after

print("CN:", cn)
print("Expiry Date:", expiry_date)
