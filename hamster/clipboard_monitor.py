import androidhelper
import time

_a = androidhelper.Android()
get_clipboard = lambda: _a.getClipboard().result


old_clipboard = get_clipboard()

while True:
    time.sleep(1)
    new_clipboard = get_clipboard()
    if new_clipboard != old_clipboard:
        print('New data copied: ' + new_clipboard)
        _a.makeToast('Copied: ' + new_clipboard[:128])
        old_clipboard = new_clipboard
