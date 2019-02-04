#!/bin/bash

if [ -z "$1" ] ; then
    echo "Usage: $0 IP_ADDRESS [INTERFACE=eth0]"
    exit
fi

addr=$1
iface=$2
if [ -z "$iface" ] ; then
    iface=eth0
fi

for i in `seq 0 10`; do
    if ! grep $iface:$i /etc/network/interfaces ; then
	echo
        echo auto $iface:$i
	echo iface $iface:$i inet static
	echo "    address $addr"
	echo "    netmask 255.255.255.0"
	exit
    fi
done
