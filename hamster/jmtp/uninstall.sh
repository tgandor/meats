#!/bin/bash

for i in "$@"; do
	rm -v "mnt/Phone/com.hipipal.qpyplus/scripts/$i"
done
