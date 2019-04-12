#!/bin/bash

find -iname '*.jp*g' -exec `dirname $0`/date_jpg.py {} +
