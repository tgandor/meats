#!/usr/bin/env python

import json
import urllib2
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print 'Usage: %s channel_id...' % (sys.argv[0],)
    exit()

def channel_info(channel_id):
    url = 'http://gdata.youtube.com/feeds/api/users/%s?v=2&prettyprint=true' % channel_id
    print url
    xml = urllib2.urlopen(url).read()
    # print xml

    et = ET.fromstring(xml)
    print 'Channel:', et.find('{http://www.w3.org/2005/Atom}title').text
    print 'User:', et.find('{http://gdata.youtube.com/schemas/2007}username').text
    print 'Total views:', et.find('{http://gdata.youtube.com/schemas/2007}statistics').attrib['totalUploadViews']
    print '-' * 50

    url = 'https://gdata.youtube.com/feeds/api/users/%s/playlists?v=2&alt=jsonc&prettyprint=true' % channel_id
    print url
    print 'Playlists:'
    try:
        playlists = json.loads(urllib2.urlopen(url).read())
        for playlist in sorted(playlists['data']['items'], key=lambda x: x['created']):
            print playlist['id'], ':', playlist['created'], ':', playlist['title']
    except:
        pass
    print '-' * 50

    url = 'http://gdata.youtube.com/feeds/api/users/%s/uploads?v=2&alt=jsonc&prettyprint=true' % channel_id
    print url
    print 'Uploads:'
    try:
        uploads = json.loads(urllib2.urlopen(url).read())
        for upload in uploads['data']['items']:
            print upload['id'], ':', upload['title']
    except:
        pass

for some_id in sys.argv[1:]:
    channel_info(some_id)
