#!/bin/bash

if ! which tcpdump ; then
    sudo apt-get install tcpdump
fi

sudo tcpdump udp port 123

