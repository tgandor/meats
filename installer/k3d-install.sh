#!/bin/bash

function die() {
  echo "ERROR $*"
  exit
}

pip install -e . || die pip

# widgets nbextension now installs automatically
jupyter nbextension install --py --sys-prefix k3d || die install
jupyter nbextension enable --py --sys-prefix k3d || die enable
