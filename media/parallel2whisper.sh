#!/bin/bash

ngpu=`nvidia-smi -L | wc -l`
echo "Using $ngpu process slots."
pver=`parallel --version | awk 'NR==1 {print $NF}'`
if [ "$pver" -ge "20230922"] ; then
    echo "Using parallel $pver and --process-slot-var="
    time parallel --jobs $ngpu --process-slot-var=CUDA_VISIBLE_DEVICES whisper ::: "$@"
else
    echo "Using old parallel $pver and hacking through env and perl expr with slot()."
    time parallel --jobs $ngpu env 'CUDA_VISIBLE_DEVICES={= $_=slot()-1 =}' whisper ::: "$@"
fi
