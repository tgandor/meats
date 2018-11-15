#!/bin/bash

df -h /var/cache
sudo apt update
sudo apt-get -y autoremove
sudo apt-get clean
df -h /var/cache
