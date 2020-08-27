#!/bin/bash

# In our case - we first create the configuration, then run the thing.

echo "Running runner configuration"
# https://docs.gitlab.com/runner/register/index.html#docker
docker run --rm -it -v gitlab-runner-config:/etc/gitlab-runner gitlab/gitlab-runner:latest register

echo "Spawning runner to background"
# https://docs.gitlab.com/runner/install/docker.html
docker run -d --name gitlab-runner --restart always -v gitlab-runner-config:/etc/gitlab-runner gitlab/gitlab-runner:latest

