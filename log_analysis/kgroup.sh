#!/bin/bash

ruby -ne 'puts $_.reverse.gsub(/(\d{3})(?=\d+\s)/, "\\1,").reverse'
