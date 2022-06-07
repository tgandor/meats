#!/bin/bash

# Workaround for broken:
# $ pip install -e <args>
# See: https://github.com/pypa/setuptools/issues/3063

pip install --prefix=$(python -m site --user-base) --editable "$@"
