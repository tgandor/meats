#!/bin/bash

./jmtp/mount.sh

for i in "$@"; do
	rm -v "mnt/Phone/com.hipipal.qpyplus/scripts/$i"
done

./jmtp/umount.sh
