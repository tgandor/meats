#!/bin/bash

# very desperate command, inspired by:
# https://askubuntu.com/questions/56761/force-apt-get-to-overwrite-file-installed-by-another-package#56764

sudo apt-get -o Dpkg::Options::="--force-overwrite" --fix-broken install
