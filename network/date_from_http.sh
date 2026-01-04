#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 [-s] URL"
    exit
fi


if [ "$2" == "-s" ]; then
    # warm up sudo
    sudo pwd > /dev/null
    elevate=sudo
    switch="-u -s"
else
    elevate=""
    switch="-d"
fi

if ! wget -S --spider $1 2>/tmp/timestamp ; then
    echo "Error: no network?"
    rm /tmp/timestamp
    exit 1
fi

utcdate=`awk '/Date:/ { sub(" *Date: +", ""); print; exit }' /tmp/timestamp`

echo "Local: "`date`
$elevate date $switch "$utcdate"
rm /tmp/timestamp
