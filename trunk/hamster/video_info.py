#!/usr/bin/env python

import json
import urllib2
import sys

if len(sys.argv) < 2:
    print 'Usage: %s video_id...' % (sys.argv[0],)
    exit()

def video_info(video_id):
    json_info = urllib2.urlopen('http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=jsonc' % video_id).read()
    info = json.loads(json_info)
    print json.dumps(info, indent=2)
    print 'Specifically,'
    print 'Title: %s' % info['data']['title']
    print 'Description:\n%s' % info['data']['description']

def playlist_info(playlist_id):
    json_info = urllib2.urlopen('http://gdata.youtube.com/feeds/api/playlists/%s?v=2&alt=jsonc' % playlist_id).read()
    info = json.loads(json_info)
    print 'Playlist: "%s"' % info['data']['title']
    print info['data']['description']
    print 'Items:'
    for item in info['data']['items']:
        print '-'*50
        print 'Position:', item['position']
        print 'Title:', item['video']['title']
        print item['video']['description']

for some_id in sys.argv[1:]:
    if len(some_id) >= 16:
        playlist_info(some_id)
    else:
        video_info(some_id)
