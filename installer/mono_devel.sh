#/bin/bash

# http://www.mono-project.com/download/stable/#download-lin

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF

if ! [ -f /etc/apt/sources.list.d/mono-official-stable.list ] ; then
    echo "deb https://download.mono-project.com/repo/ubuntu stable-xenial main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
fi

sudo apt-get install apt-transport-https
sudo apt-get update
sudo apt-get install mono-devel

