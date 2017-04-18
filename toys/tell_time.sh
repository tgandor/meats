#!/bin/bash

LANG=C date +%I:%M,%p | espeak -s 120

LANG=C date +%I:%M,%p >> /tmp/last_times
