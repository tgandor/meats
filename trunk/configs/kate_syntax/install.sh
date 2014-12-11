#!/bin/bash

pushd `dirname $0`
sudo cp *.xml /usr/share/kde4/apps/katepart/syntax/
popd

echo "Done."

