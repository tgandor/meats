#!/bin/bash

tar cf pacman-`date --iso`.tar /var/cache/pacman/pkg /var/lib/pacman/sync
echo "Packages tarred into:" pacman-`date --iso`.tar
ls -lh pacman-`date --iso`.tar
echo "Clean cache e.g. with ~/meats/system/pac/clean_cache.sh --all"
