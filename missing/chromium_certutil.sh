#!/bin/bash

certutil -d sql:$HOME/.pki/nssdb "$@"
