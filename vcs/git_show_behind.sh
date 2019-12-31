#!/bin/bash

git fetch -p
git log HEAD..origin/HEAD | awk '/^commit/ { c += 1 } { print c " " $0 }'  | less
