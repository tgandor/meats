#!/bin/bash

# Add certifcate as trusted peer in Chom{e|ium} Linux
# http://superuser.com/a/598608/269542

if [ -z "$2" ]; then
	echo "Usage: $0 <certificate_nickname> <certificate_file>"
	echo "Use with caution"
	exit
fi

# -d <database-directory>
# -A Add certifcate to the database
# -t trustargs
#    P trusted peer

certutil -d sql:$HOME/.pki/nssdb -A -t P -n "$1" -i "$2"
