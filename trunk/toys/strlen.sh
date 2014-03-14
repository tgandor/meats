#!/bin/bash
perl -mEncode -ne 's/\s+$//; print length(Encode::decode("utf8", $_))." $_\n";'
