#!/bin/bash

echo "Writable data:"
du -h /var/snap
echo "Snap images:"
ls -lhS /var/lib/snapd/snaps/
