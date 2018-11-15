#!/bin/bash

# thanks to: https://stackoverflow.com/questions/46690571/npm-global-install-links-to-wrong-directory

if ! which npm ; then
    echo Install nodejs first
    exit
fi

NODE_PATH=/usr/lib/node_modules
sudo npm install -g markdown-pdf --unsafe-perm=true --allow-root
