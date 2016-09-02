#!/bin/bash

cd `dirname $0`/..

echo 'Syncing...'
sync
echo 'Done.'

if grep `pwd`/mnt /proc/mounts ; then
    fusermount -u `pwd`/mnt && echo "Unmounted successfully" || echo "Error unmounting"
else
    echo "Not mounted, exiting"
fi
