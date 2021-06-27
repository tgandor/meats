#!/bin/bash

echo "Try also: pamac info <package>"
pacman -Qi "$@"
