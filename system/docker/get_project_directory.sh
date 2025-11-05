#!/bin/bash

if [[ "$1" == "" ]] ; then
    echo "Usage: $0 <container_id|container_name>..."
    exit
fi

docker inspect --format '{{ index .Config.Labels "com.docker.compose.project.working_dir" }}' "$@"
