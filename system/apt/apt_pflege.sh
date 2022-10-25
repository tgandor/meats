#!/bin/bash

df /var/cache
sudo apt update
sudo apt-get -y autoremove
sudo apt-get clean
df /var/cache
echo Listing upgradeable:
apt list --upgradable
