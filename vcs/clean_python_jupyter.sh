#!/bin/bash

# to git-ignore them is one thing, but you may want other stuff
# (fdupes? find? counting?)

# further reading:
# https://unix.stackexchange.com/questions/164873/find-delete-does-not-delete-non-empty-directories

find -path '*/__pycache__*' -print -delete
find -path '*/.ipynb_checkpoints*' -print -delete
