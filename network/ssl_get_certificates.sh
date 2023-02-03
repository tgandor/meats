#!/bin/bash

# Reference: https://www.cyberciti.biz/faq/test-ssl-certificates-diagnosis-ssl-certificate/

echo | openssl s_client -showcerts -connect $1
