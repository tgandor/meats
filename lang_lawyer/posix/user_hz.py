#!/usr/bin/env python
# http://stackoverflow.com/questions/4189123/python-how-to-get-number-of-mili-seconds-per-jiffy
import os
sysconf_id = os.sysconf_names['SC_CLK_TCK']
print(os.sysconf(sysconf_id))
