#!/usr/bin/env python

import argparse
import os
import re
import socket
import sys
import time

import six.moves.urllib.error
import six.moves.urllib.parse
import six.moves.urllib.parse
import six.moves.urllib.request


user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"


def human(x):
    for sufix in ['', 'K', 'M', 'G', 'T']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024.0
    return "%.1f P" % x


def get(url):
    """Stubborn retrieve data."""
    if os.path.isfile(url):
        return open(url).read()

    while True:
        try:
            req = six.moves.urllib.request.Request(url, data=None, headers={"User-Agent": user_agent})
            resp = six.moves.urllib.request.urlopen(req)
            return resp.read()
        except socket.timeout:
            print("Timed out. Retrying.")
        except socket.error as e:
            print("Other socket error:", e)
            print("Retry in 5 seconds...")
            time.sleep(5)


def down(url):
    filename = os.path.basename(six.moves.urllib.parse.unquote(url))
    print('Downloading "{}" to "{}" file...'.format(url, filename))

    if os.path.exists(filename):
        print("skipped {}, '{}' (exists)".format(url, filename))
        return 0

    if not filename:
        print('Skipping "{}" (probably a directory)'.format(url))
        return 0

    print("getting", filename)
    start = time.time()
    data = get(url)
    size = len(data)
    elapsed = time.time() - start
    print("got %sB in %.1f s (%sB/s), saving" % (human(size), elapsed, human(size / elapsed)))
    open(filename, 'wb').write(data)
    return size


def folder_name(url):
    candidate = six.moves.urllib.parse.urlsplit(url).path.split('/')[-2]
    if not candidate:
        print('Could not find folder name, returning generic.')
        return 'new_folder'
    return candidate


def enter_folder(name):
    print("Trying to create '{0}', being in {1}...".format(name, os.getcwd()))
    if not os.path.exists(name):
        os.mkdir(name)
        new_name = name
    elif not os.path.isdir(name):
        print("Error: %s exists, but is not a directory")
        suffix = 1
        new_name = "%s_%d" % (name, suffix)
        while os.path.exists(new_name) and not os.path.isdir(new_name):
            suffix += 1
            new_name = "%s_%d" % (name, suffix)
        os.mkdir(new_name)
    else:
        new_name = name
    os.chdir(new_name)


def download_all(url, search='mp3$', attrib='href'):
    total = 0
    try:
        if os.path.exists(url):
            # even if last_content.html ;)
            with open(url, "rb") as f:
                content_bin = f.read()
        else:
            content_bin = get(url)
        content = content_bin.decode('utf-8')
        with open('last_content.html', 'wb') as dump:
            dump.write(content_bin)

        links = sorted(set([link
                            for link in re.findall(attrib + '=["\']([^"\']+)["\']', content, re.IGNORECASE)
                            if re.search(search, link)]))
        links = [six.moves.urllib.parse.urljoin(url, link)
                 if not link.startswith('http')
                 else link for link in links]
    except Exception as e:
        print("Error retrieving file list:", e)
        return
    print("Found:")
    print("\n".join(links))
    if not links:
        print("No URLs found to follow.")
        # print content
        return
    try:
        enter_folder(folder_name(url))
        for link in links:
            total += down(link)
    finally:
        print("Total downloaded: %sB" % human(total))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('search', nargs='?', default='mp3$')
    parser.add_argument('attrib', nargs='?', default='href')
    args = parser.parse_args()
    download_all(args.url, args.search, args.attrib)


if __name__ == '__main__':
    main()
