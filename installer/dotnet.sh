#/bin/bash

# https://www.microsoft.com/net/download/linux-package-manager/ubuntu16-04/sdk-current

if ! [ -f /etc/apt/trusted.gpg.d/microsoft.gpg ] ; then
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /tmp/microsoft.gpg
    sudo mv /tmp/microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
fi

if ! [ -f /etc/apt/sources.list.d/dotnetdev.list ] ; then
    sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-xenial-prod xenial main" > /etc/apt/sources.list.d/dotnetdev.list'
fi

sudo apt-get install apt-transport-https
sudo apt-get update
sudo apt-get install dotnet-sdk-2.1.103
