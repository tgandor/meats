#!/bin/bash

ruby -ne 'puts $_.reverse.gsub(/(\d{3})(?=\d+\s|\d+$)/, "\\1,").reverse'
