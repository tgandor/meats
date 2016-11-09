#!/bin/bash

shopt -s nullglob

for d in */.git ; do
	pushd $d/.. >/dev/null
	pwd
	git pull --ff-only
	echo ----------------------------------
	popd >/dev/null
done
