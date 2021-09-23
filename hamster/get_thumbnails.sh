#!/bin/bash

# usually gets WebP, but there is another way of getting JPGs
xargs -n1 youtube-dl --skip-download --write-thumbnail --output "%(id)s"

