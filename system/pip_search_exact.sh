#!/bin/bash

pip search $1 | awk 'tolower($1) == tolower("'$1'")'

