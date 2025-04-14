#!/bin/bash

sed -i 's/\xC2\xA0/ /g' "$@"
