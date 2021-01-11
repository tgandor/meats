#!/bin/bash

# see more:
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker

# docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
docker run --rm --gpus all nvidia/cuda nvidia-smi
