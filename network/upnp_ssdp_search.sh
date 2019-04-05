#!/bin/bash

if ! which gssdp-discover >/dev/null; then
    sudo apt install gupnp-tools
fi


ip link | awk '/docker/ {next} /LOOPBACK/ {next} /^[0-9]/{ gsub(/:/,""); print $2  }' | while read interface ; do
    echo "Scanning on $interface"
    gssdp-discover -i $interface
done
