#!/bin/bash

cd `dirname $0`

[ $VIRTUAL_ENV ] || source ../venv36/bin/activate

pip install -e .

jupyter nbextension install --py --sys-prefix k3d
jupyter nbextension enable --py --sys-prefix k3d
