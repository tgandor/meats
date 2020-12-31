#!/bin/bash

source /etc/os-release
echo "Current version codename: $VERSION_CODENAME"

# From: https://docs.couchdb.org/en/latest/install/unix.html#installation-using-the-apache-couchdb-convenience-binary-packages
sudo apt-get install -y gnupg ca-certificates
echo "deb https://apache.bintray.com/couchdb-deb $VERSION_CODENAME main" | sudo tee /etc/apt/sources.list.d/couchdb.list

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8756C4F765C9AC3CB6B85D62379CE192D401AB61

sudo apt update
sudo apt install -y couchdb

