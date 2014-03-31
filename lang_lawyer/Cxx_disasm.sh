#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: $0 [options, like -O3] file.cpp"
    exit
fi

g++ -g -c -o /tmp/C_disasm.o "$@"
objdump -S /tmp/C_disasm.o
rm /tmp/C_disasm.o
