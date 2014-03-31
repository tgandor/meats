#!/usr/bin/env python

# OK, the target platform has no 'env'...

import sys, urllib, os, re, time, socket, errno, urlparse

def human(x):
    for sufix in ['', 'K', 'M', 'G', 'T']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024.0
    return "%.1f P" % x

def get(URL):
    """Stubborn retrieve data."""
    while True:
        try:
            return urllib.urlopen(URL).read()
        except socket.timeout:
            print "Timed out. Retrying."
        except socket.error as e:
            print "Other socket error:", e
            print "Retry in 5 seconds..."
            time.sleep(5)

def down(URL):
  f = urllib.unquote(os.path.basename(URL))
  if os.path.exists(f):
      print  "skipped", f
      return 0
  print "getting", f
  start = time.time()
  data = get(URL)
  size = len(data)
  elap = time.time() - start
  print "got %sB in %.1f s (%sB/s), saving" % (human(size), elap, human(size/elap))
  open(f,"w").write(data)
  return size

def folder_name(URL):
    return urlparse.urlsplit(URL).path.split('/')[-2]
    
def download_all(URL, SEARCH = 'mp3$'):
    total = 0
    try:
        content = get(URL)
        links = sorted(set([link
                 for link in re.findall('href="([^"]+)"', content)
                 if re.search(SEARCH, link)]))
        links = [ urlparse.urljoin(URL, link)
                  if not link.startswith('http')
                  else link for link in links ]
    except:
        print "Error retrieving file list."
        return
    # print links
    if not links:
        print "No URLs found to follow."
        # print content
        return
    try:
        os.mkdir(folder_name(URL))
        os.chdir(folder_name(URL))
        for link in links:
            total += down(link)
    finally:
        print "Total downloaded: %sB" % human(total)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        download_all(sys.argv[1])
    elif len(sys.argv) == 3:
        download_all(sys.argv[1], sys.argv[2])
    else:
        print "trying to retrieve from clipboard"
        try:
            import androidhelper
        except:
            print "Error: couldn't find androidhelper"
            exit()
        try:
            os.chdir('/mnt/sdcard/external_sd/Music/')
        except:
            try:
                os.chdir('/mnt/sdcard/')
            except:
                pass
        URL = androidhelper.Android().getClipboard().result
        download_all(URL)
