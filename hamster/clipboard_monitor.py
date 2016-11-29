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


if not _a.checkWifiState().result:
    print('Not on WiFi, exiting.')
    exit()

download_queue = Queue()

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
            youtube_dl.main([url.split()[-1]])
            exit()
        os.wait()
        print('Download finished')
        _a.makeToast('Finished: {}...'.format(url[:10]))
        _a.vibrate(1000)
        os.system('df .')

print('Starting clipboard watcher...')
threading.Thread(target=clipboard_watcher, args=(download_queue,)).start()
os.chdir('/mnt/sdcard/Download')
os.system('df .')
print('Entering get/fork/download/wait loop...')
downloader(download_queue)
