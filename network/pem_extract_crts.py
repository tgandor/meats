#!/usr/bin/env python

import argparse

from cryptography import x509
from cryptography.hazmat.primitives import serialization


def get_cn(name):
    return name.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value


parser = argparse.ArgumentParser()
parser.add_argument("pem_file", help="PEM file to process")
parser.add_argument(
    "--write", "-w", action="store_true", help="saved extracted certificates to .crt-s"
)
args = parser.parse_args()

with open(args.pem_file, "rb") as pem_file:
    pem_data = pem_file.read()

certificates = list(x509.load_pem_x509_certificates(pem_data))

for i, cert in enumerate(certificates, 1):
    subject = cert.subject
    issuer = cert.issuer
    print(i)
    print(f"{get_cn(subject)=}")
    print(f"{get_cn(issuer)=}")
    if not args.write:
        continue
    out_file = get_cn(subject).replace(" ", "_") + ".crt"
    with open(out_file, "wb") as crt_file:
        crt_file.write(cert.public_bytes(serialization.Encoding.PEM))
    print(f"Saved to {out_file}")
