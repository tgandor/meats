from __future__ import print_function

import androidhelper
import os
import time

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

import threading

_a = androidhelper.Android()
get_clipboard = lambda: _a.getClipboard().result


def clipboard_watcher(download_queue):
    old_clipboard = get_clipboard()

    while True:
        time.sleep(1)
        new_clipboard = get_clipboard()
        if new_clipboard != old_clipboard:
            print('New data copied: ' + new_clipboard)
            _a.makeToast('Copied: {}...'.format(new_clipboard[:16]))
            old_clipboard = new_clipboard
            download_queue.put(new_clipboard)


def downloader(download_queue):
    # importing locally, this takes forever, while script is silent
    import youtube_dl

    while True:
        url = download_queue.get(True)
        pid = os.fork()
        if not pid:
            print('Downloading... ({})'.format(url))
            youtube_dl.main(['--no-check-certificate', url.split()[-1]])
            exit()
        os.wait()
        print('Download finished')
        _a.makeToast('Finished: {}...'.format(url[:10]))
        _a.vibrate(1000)
        os.system('df .')


os.chdir(os.path.dirname(__file__) + '/../../Download')
os.system('df .')

if not _a.checkWifiState().result:
    print('Not on WiFi, exiting.')
    exit()
print('Starting clipboard watcher...')

_download_queue = Queue()
threading.Thread(target=clipboard_watcher, args=(_download_queue,)).start()

print('Entering get/fork/download/wait loop...')
downloader(_download_queue)
