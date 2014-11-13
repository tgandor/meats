#!/usr/bin/env python

import json
import urllib2
import sys

if len(sys.argv) < 2:
    print 'Usage: %s video_id...' % (sys.argv[0],)
    exit()

for video_id in sys.argv[1:]:
    json_info = urllib2.urlopen('http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=jsonc' % video_id).read()
    info = json.loads(json_info)
    print json.dumps(info, indent=2)
    print 'Specifically,'
    print 'Title: %s' % info['data']['title']
    print 'Description:\n%s' % info['data']['description']
