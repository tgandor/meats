#!/bin/bash

confirm() {
    while true; do
        read -p "$1 [Y/N]: " response
        case "$response" in
            [Yy]) return 0 ;;
            [Nn]) return 1 ;;
            *) echo "Invalid response. Please enter Y or N." ;;
        esac
    done
}

tar cf pacman-`date --iso`.tar /var/cache/pacman/pkg /var/lib/pacman/sync
echo "Packages tarred into:" pacman-`date --iso`.tar
ls -lh pacman-`date --iso`.tar

if confirm "Do you want to run: ~/meats/system/pac/clean_cache.sh --all"; then
    ~/meats/system/pac/clean_cache.sh --all
    ls -lh pacman-`date --iso`.tar
else
    echo "Done."
fi
