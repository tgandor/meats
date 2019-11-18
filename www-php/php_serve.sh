#!/bin/bash

# The alternative for python -m http.server, which
# additionally allows for serving PHP...

if [ "$1" == "" ] ; then
    IP_PORT=0.0.0.0:8000
else
    IP_PORT=$1
fi

php -S $IP_PORT
