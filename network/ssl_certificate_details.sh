#!/bin/bash

if [[ $1 == *.p7b ]]; then
  openssl pkcs7 -print_certs -in "$1"
else
  openssl x509 -in "$1" -text
fi

