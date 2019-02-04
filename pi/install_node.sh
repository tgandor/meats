#!/bin/bash

sudo apt-get update
sudo apt-get install -y npm

sudo npm cache clean -f
sudo npm install -g n
sudo n stable

stable=`ls /usr/local/n/versions/node/*/bin/node | tail -n1`
echo sudo ln -sf $stable /usr/bin/nodejs
sudo ln -sf $stable /usr/bin/nodejs
