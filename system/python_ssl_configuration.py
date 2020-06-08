#!/usr/bin/env python

# Next time you need to trust some strange cert:
# https://stackoverflow.com/a/44649450/1338797

import ssl

print(ssl.get_default_verify_paths())

