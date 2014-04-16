#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: $0 path [subdir]"
    exit
fi

if [ -z $2 ]; then
    name=`basename "$1"`
else
    name=$2
fi

target=`realpath "$1"`
echo "Want to serve: $target"
echo "as: $name"

pushd /var/www
if [ -e "$name" ]
then
    echo "$name exists..."
else
    ln -s "$target" "$name"
fi
popd

bd=`dirname $0`

$bd/localhost.py "$name"/ | xargs $bd/qr.sh
