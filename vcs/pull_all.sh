#!/bin/bash

shopt -s nullglob

function git_pull {
	pushd "$1" >/dev/null
	pwd
	git pull --ff-only
	echo ----------------------------------
	popd >/dev/null
}

if [ $# -eq 0 ] ; then
	for d in */.git ; do
		git_pull "$d/.."
	done
else
	for d in "$@" ; do
		git_pull "$d"
	done
fi

