#!/bin/bash

jq -r .segments[].text "$@" | less
