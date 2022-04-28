#!/bin/bash

# Highlight: https://stackoverflow.com/questions/981601/colorized-grep-viewing-the-entire-file-with-highlighted-matches

LANG=C pacman -Qi "$@" | grep --color "Required By\|$"
echo "Try also: pamac info <package>"
