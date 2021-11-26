#!/bin/bash

docker run --runtime=nvidia --rm -it -v $(pwd)/:/work ffmpycu bash

