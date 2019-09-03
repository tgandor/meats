#!/bin/bash

# https://stackoverflow.com/questions/5442436/using-rot13-and-tr-command-for-having-an-encrypted-email-address

tr 'A-Za-z' 'N-ZA-Mn-za-m'

# alternatives:
# -------------

# Python:

# >>> import codecs
# >>> codecs.encode('lala', 'rot13')
# 'ynyn'

# Ruby: 
# $ ruby -ne 'print $_.tr( "A-Za-z", "N-ZA-Mn-za-m") ' file

# Bash, ROT13+ROT5:
# tr 'A-Za-z0-9' 'N-ZA-Mn-za-m5-90-4'

