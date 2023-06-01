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

shopt -s nullglob

if [ "$1" == "" ] ; then
    echo "Usage: $0 pacman-<date>.tar"
    pattern="pacman-20??-??-??.tar"
    matches=($pattern)
    if [[ ${#matches[@]} -eq 1 ]]; then
        echo "Guessing: $matches" 
        tar_path=`realpath $matches`
    else
        echo "No files matched or more than one file matched: $matched"
        exit
    fi
else
    tar_path=`realpath $1`
fi

cd /
sudo tar xvf "$tar_path"
echo "Finished unpacking $tar_path"

if confirm "Do you want to run: ~/meats/system/pac/upgrade.sh"; then
    ~/meats/system/pac/upgrade.sh
    if confirm "~/meats/system/pac/clean_cache.sh --all"; then
        ~/meats/system/pac/clean_cache.sh --all
    fi
else
    echo "Done."
fi

